from django.urls import path, include
from .views import (IndexTemplateView, MaktabRedirectView,
                    PostListView, PostDetailView, PostCreateView,
                    PostUpdateView, PostDeleteView)


app_name = 'blog'


urlpatterns = [
    path('', IndexTemplateView.as_view(), name='index'),
    path('go-to-maktab/', MaktabRedirectView.as_view(), name='go-to-maktab'),

    path(
        'post/',
        PostListView.as_view(),
        name='post-list'
    ),
    path(
        'post/detail/<int:post_id>/',
        PostDetailView.as_view(),
        name='post-detail'
    ),
    path(
        'post/create/',
        PostCreateView.as_view(),
        name='post-create'
    ),
    path(
        'post/<int:post_id>/edit/',
        PostUpdateView.as_view(),
        name='post-edit'
    ),
    path(
        'post/<int:post_id>/delete/',
        PostDeleteView.as_view(),
        name='post-delete'
    ),

    path('api/v1/', include('blog.api.v1.urls')),
]
