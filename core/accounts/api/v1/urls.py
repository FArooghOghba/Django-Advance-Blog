from django.urls import path

from .views import RegistrationGenericAPIView


app_name = 'api-v1'


urlpatterns = [
    path('registration/', RegistrationGenericAPIView.as_view(), name='register')
]