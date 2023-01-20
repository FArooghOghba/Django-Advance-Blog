# from django.test import TestCase
# from datetime import datetime
#
# from ..models import Category
# from ..forms import PostForm
#
#
# class TestBlogForms(TestCase):
#
#     def test_post_form_valid_data(self):
#         category_obj = Category.objects.create(
#             name='test_category'
#         )
#
#         post_form = PostForm(
#             data={
#                 'title': 'test_title',
#                 'content': 'test_content',
#                 'category': category_obj,
#                 'status': True,
#                 'published_date': datetime.now()
#             }
#         )
#         self.assertTrue(post_form.is_valid())
#
#     def test_post_form_invalid_data(self):
#         post_form = PostForm(data={})
#         self.assertFalse(post_form.is_valid())
