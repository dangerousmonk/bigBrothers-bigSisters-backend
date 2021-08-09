from django.conf.urls import include
from django.contrib import admin
from django.urls import path

from rest_framework_simplejwt import views as jwt_views

from .routers import v1_router
from bbbs.users.views import ProfileViewSet, RequestPasswordReset, PasswordResetCheck, SetNewPasswordAPIView

urlpatterns = [
    path('api/v1/', include(v1_router.urls)),
    path('admin/', admin.site.urls),
    path('api/v1/profile/', ProfileViewSet.as_view(), name='profile'),
    path('api/v1/request-password-reset/', RequestPasswordReset.as_view, name='request-password-reset'),
    path('api/v1/password-reset/<uidb64>/<token>/', PasswordResetCheck.as_view, name='password-reset-check'),
    path('api/v1/password-reset-complete/', SetNewPasswordAPIView.as_view, name='password-reset-complete'),
    path('api/v1/token/', jwt_views.TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('api/v1/token/refresh/', jwt_views.TokenRefreshView.as_view(),
         name='token_refresh'),
    path('api-auth/', include('rest_framework.urls')),
]
