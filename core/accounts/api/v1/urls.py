from django.urls import path

from .views import RegistrationGenericAPIView, ObtainAuthToken, DiscardAuthToken


app_name = 'api-v1'


urlpatterns = [
    path('registration/', RegistrationGenericAPIView.as_view(), name='register'),
    path('token/login/', ObtainAuthToken.as_view(), name='token-login'),
    path('token/logout/', DiscardAuthToken.as_view(), name='token-logout')
]