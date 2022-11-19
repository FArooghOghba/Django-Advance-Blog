from django.urls import path
from .views import post_list_view


app_name = 'api-v1'


urlpatterns = [
    path('post/', post_list_view, name='post-list')
]
