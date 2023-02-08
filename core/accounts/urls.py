from django.urls import path, include
from .views import send_email, test_mock_server


app_name = 'accounts'


urlpatterns = [
    path('', include('django.contrib.auth.urls')),

    path('send-email/', send_email, name='send-email'),
    path(
        'test-mock-server/', test_mock_server, name='test-mock-server'
    ),

    path('api/v1/', include('accounts.api.v1.urls')),
    path('api/v2/', include('djoser.urls')),
    path('api/v2/', include('djoser.urls.jwt')),
]
