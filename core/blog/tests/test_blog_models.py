# from django.test import TestCase
# from django.contrib.auth import get_user_model
# from datetime import datetime
#
# from ..models import Post, Category
# from accounts.models import Profile
#
# User = get_user_model()
#
#
# class TestBlogModels(TestCase):
#     def setUp(self) -> None:
#         self.user_obj = User.objects.create(
#             email='test@test.com',
#             password='test_password'
#         )
#
#         self.profile_obj = Profile.objects.create(
#             user=self.user_obj,
#             first_name='test_first_name',
#             last_name='test_last_name',
#             description='test_description'
#         )
#
#         self.category_obj = Category.objects.create(
#             name='test_category'
#         )
#
#     def test_blog_post_create(self):
#
#         post_obj = Post.objects.create(
#             title='test_title',
#             author=self.profile_obj,
#             content='test_content',
#             category=self.category_obj,
#             status=True,
#             published_date=datetime.now()
#         )
#         self.assertTrue(Post.objects.filter(pk=post_obj.id).exists())
#         self.assertTrue(post_obj.title, 'test_title')
