from rest_framework import serializers
from .models import ImageModel

class ImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True, required=False, allow_null=True)
    class Meta:
        model = ImageModel
        # 'result' 필드를 fields 리스트에 추가하여 serializer가 처리하도록 합니다.
        fields = ('id', 'address', 'text', 'image', 'result', 'report', 'information', 'time')