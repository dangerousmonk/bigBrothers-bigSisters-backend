from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from rest_framework_simplejwt import views as jwt_views

from bbbs.users.views import ProfileAPIView

from .routers import v1_router

urlpatterns = [
    path('api/v1/', include(v1_router.urls)),
    path('admin/', admin.site.urls),
    path('api/v1/profile/', ProfileAPIView.as_view(), name='profile'),
    path('api/v1/token/', jwt_views.TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('api/v1/token/refresh/', jwt_views.TokenRefreshView.as_view(),
         name='token_refresh'),
    path('api-auth/', include('rest_framework.urls')),
]


if settings.DEBUG:
    static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)