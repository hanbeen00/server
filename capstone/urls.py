from django.urls import path, include
from rest_framework import routers
from dot import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

router = routers.DefaultRouter()
router.register(r'posts', views.PostViewset)

urlpatterns = [
    path('admin/', admin.site.urls),  # 관리자 페이지 URL
    path('board/', views.PostViewset.as_view({'get': 'board_list'}), name='board_list'),  # 이미지 목록을 템플릿에 전달하는 URL 패턴
    path('', include(router.urls)),  # API 엔드포인트
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]

# 정적 파일 서빙을 위한 설정
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
