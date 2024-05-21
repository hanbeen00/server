from django.urls import path, include
from rest_framework import routers
from dot import views  # 'dot'는 Django 앱 이름으로 가정합니다.
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

router = routers.DefaultRouter()
router.register(r'posts', views.PostViewset)  # PostViewSet을 'posts' 경로에 등록

urlpatterns = [
    path('admin/', admin.site.urls),  # 관리자 페이지 URL
    # PostViewSet 내의 board_list 액션 메서드를 직접 라우팅
    path('board/', views.PostViewset.as_view({'get': 'board_list'}), name='board_list'),
    path('', include(router.urls)),  # API 엔드포인트
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]

# 정적 파일과 미디어 파일 서빙을 위한 설정
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
