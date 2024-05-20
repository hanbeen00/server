from django.http import HttpResponse, JsonResponse
from rest_framework import viewsets
from .models import ImageModel
from .serializers import ImageSerializer
import PIL
from ultralytics import YOLO
import json
import numpy as np
import torch
from BrailleToKorean.BrailleToKor import BrailleToKor
from braille2kor.run_model import parse_xywh_and_class, convert_to_braille_unicode
from django.http import HttpResponseRedirect

from django.shortcuts import render
from django.core.paginator import Paginator

class PostViewset(viewsets.ModelViewSet):
    queryset = ImageModel.objects.all()
    serializer_class = ImageSerializer
        
    def create(self, request, *args, **kwargs):
        # 이미지 파일이 request에 포함되어 있는지 확인
        file = request.FILES.get('image', None)

        # request.data에서 다른 필드 값들을 읽어옵니다.
        address = request.data.get('address', '')
        text = request.data.get('text', '')
        report = request.data.get('report', '')
        information = request.data.get('information', '')
        time = request.data.get('time','')

        # ImageModel 인스턴스 생성
        image_instance = ImageModel(
            image=file if file else None,  # 이미지가 없는 경우 None을 지정
            address=address,
            text=text,
            report=report,
            time=time,
            information=information,
            result=''  # result 필드 초기화
        )

        image_instance.save()  # 이미지 인스턴스 저장

        # 이미지가 있을 경우에만 YOLO 모델과 점자 번역 로직 수행
        if file:
            image_path = image_instance.image.path
            #print("Image saved at:", image_path)

            image = PIL.Image.open(image_path)
            model = YOLO("./models/yolov8_braille.pt")
            res = model.predict(image, save=True, save_txt=True, exist_ok=True, conf=0.15)
            boxes = res[0].boxes
            if len(boxes) == 0:  # 감지된 박스가 없으면 점자가 아님
                image_instance.result = "점자 이미지가 아닙니다"
            else:
                list_boxes = parse_xywh_and_class(boxes)

                result = ""
                for box_line in list_boxes:
                    str_left_to_right = ""
                    box_classes = box_line[:, -1]
                    for each_class in box_classes:
                        str_left_to_right += convert_to_braille_unicode(model.names[int(each_class)], "./utils/braille_map.json")
                    result += str_left_to_right + "\n"

                b = BrailleToKor()
                translated_result = b.translation(result)

                # 번역 결과를 result 필드에 저장
                image_instance.result = translated_result
            image_instance.save()

        # 성공적으로 처리되었다는 응답 반환
        return HttpResponseRedirect(request.build_absolute_uri())

    def board_list(self, request):
        # 이미지 목록 가져오기
        queryset = self.queryset.all()
        paginator = Paginator(queryset, 5)

        page_number = request.GET.get('page','1')
        page_obj = paginator.get_page(page_number)


        serializer = self.serializer_class(queryset, many=True)
        return render(request, 'board_list.html', {'image_list': serializer.data, 'page_obj': page_obj})
    
    