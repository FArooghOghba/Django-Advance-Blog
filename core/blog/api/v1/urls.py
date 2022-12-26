from rest_framework.routers import DefaultRouter

from .views import PostModelViewSet, CategoryModelViewSet


app_name = 'api-v1'

router = DefaultRouter()
router.register('post', PostModelViewSet, basename='post')
router.register('category', CategoryModelViewSet, basename='category')

urlpatterns = router.urls


'''
urlpatterns = [
    # path('post/', post_list_view, name='post-list'),
    # path('post/', PostListView.as_view(), name='post-list'),

    # path('post/<int:post_id>/', post_detail_view, name='post-detail'),
    # path('post/<int:post_id>/', PostDetailView.as_view(), name='post-detail'),
]
'''
