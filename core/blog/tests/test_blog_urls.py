# from django.test import TestCase
# from django.urls import reverse, resolve
#
# from ..views import (
#     IndexTemplateView, PostListView, PostDetailView
# )
#
# # Create your tests here.
#
# class TestBlogUrls(TestCase):
#
#     def test_blog_index_url_resolver(self):
#         url = reverse('blog:index')
#         self.assertEquals(
#             resolve(url).func.view_class,
#             IndexTemplateView
#         )
#
#     def test_blog_post_list_url_resolver(self):
#         url = reverse('blog:post-list')
#         self.assertEquals(
#             resolve(url).func.view_class,
#             PostListView
#         )
#
#     def test_blog_post_detail_resolver(self):
#         url = reverse('blog:post-detail', kwargs={'post_id': 1})
#         self.assertEquals(
#             resolve(url).func.view_class,
#             PostDetailView
#         )
