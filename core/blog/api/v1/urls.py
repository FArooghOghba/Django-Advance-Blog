from django.urls import path
from .views import *


app_name = 'api-v1'


urlpatterns = [
    # path('post/', post_list_view, name='post-list'),
    path('post/', PostListView.as_view(), name='post-list'),

    path('post/<int:post_id>/', post_detail_view, name='post-detail'),
]
