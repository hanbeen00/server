from django.contrib import admin

from .models import ImageModel

# ImageModel을 관리자 페이지에 등록
@admin.register(ImageModel)
class ImageModelAdmin(admin.ModelAdmin):
    # 관리자 페이지에서 표시할 필드 설정
    list_display = ('id', 'address', 'text', 'image', 'result', 'report', 'information', 'time')  # 리스트 페이지에서 보이는 필드들
    search_fields = ('address', 'text', 'result', 'report', 'information', 'time')  # 검색 가능한 필드들
    list_filter = ('time',)  # 필터링 가능한 필드들
    fields = ('report',)  # 수정 가능한 필드들

# 또는 간단하게 등록만 할 수도 있습니다.
# admin.site.register(ImageModel)
