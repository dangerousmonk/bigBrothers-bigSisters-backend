from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from .routers import v1_router
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('api/v1/', include(v1_router.urls)),
    path('admin/', admin.site.urls),
    path('api/v1/token/', jwt_views.TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('api/v1/token/refresh/', jwt_views.TokenRefreshView.as_view(),
         name='token_refresh'),
    path('api-auth/', include('rest_framework.urls')),
]
