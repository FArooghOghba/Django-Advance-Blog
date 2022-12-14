from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView, TokenVerifyView
)

from ..views import (
    RegistrationGenericAPIView, ObtainAuthToken, DiscardAuthToken,
    CustomTokenObtainPairView, ChangePasswordUpdateAPIView,
    ActivationConfirmGenericAPIView, ActivationResendGenericAPIView
)



urlpatterns = [
    # registration
    path('registration/', RegistrationGenericAPIView.as_view(), name='register'),

    path('activation/confirm/<str:token>/', ActivationConfirmGenericAPIView.as_view(), name='activation-confirm'),
    path('activation/resend/', ActivationResendGenericAPIView.as_view(), name='activation-resend'),

    # change password
    path('change-password/', ChangePasswordUpdateAPIView.as_view(), name='change-password'),

    # login token
    path('token/login/', ObtainAuthToken.as_view(), name='token-login'),
    path('token/logout/', DiscardAuthToken.as_view(), name='token-logout'),

    # login jwt
    path('jwt/create/', CustomTokenObtainPairView.as_view(), name='jwt-create'),
    path('jwt/refresh/', TokenRefreshView.as_view(), name='jwt-refresh'),
    path('jwt/verify/', TokenVerifyView.as_view(), name='jwt_verify'),
]