from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from datetime import datetime

from ..models import Post, Category
from accounts.models import Profile


User = get_user_model()


class TestBlogViews(TestCase):

    def setUp(self) -> None:
        self.client = Client()

        self.user_obj = User.objects.create(
            email='test@test.com',
            password='test_password'
        )

        self.profile_obj = Profile.objects.create(
            user=self.user_obj,
            first_name='test_first_name',
            last_name='test_last_name',
            description='test_description'
        )

        self.category_obj = Category.objects.create(
            name='test_category'
        )

        self.post_obj = Post.objects.create(
            title='test_title',
            author=self.profile_obj,
            content='test_content',
            category=self.category_obj,
            status=True,
            published_date=datetime.now()
        )

    def test_blog_view_successful_response(self):
        url = reverse('blog:index')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTrue(str(response.content).find('index'))
        self.assertTemplateUsed(response, template_name='index.html')

    def test_blog_post_detail_anonymous_request(self):
        url = reverse(
            'blog:post-detail',
            kwargs={'post_id': self.post_obj.id}
        )
        response = self.client.get(url)
        self.assertTrue(response.status_code, 302)

    def test_blog_post_detail_authenticated_request(self):
        self.client.force_login(self.user_obj)
        url = reverse(
            'blog:post-detail',
            kwargs={'post_id': self.post_obj.id}
        )
        response = self.client.get(url)
        self.assertTrue(response.status_code, 200)
