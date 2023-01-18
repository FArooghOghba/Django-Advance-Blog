import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient
from datetime import datetime


User = get_user_model()

@pytest.fixture()
def test_user():
    user = User.objects.create(
        email='test@test.com',
        password='far121269'
    )
    return user


@pytest.mark.django_db
class TestBlogPostAPI:
    client = APIClient()
    post_data = {
            'title': 'test_title',
            'content': 'test_content',
            'status': True,
            'published_date': datetime.now()
        }

    def test_get_post_list_response_ok_200_status(self):
        url = reverse('blog:api-v1:post-list')
        response = self.client.get(path=url)
        assert response.status_code == 200

    def test_create_post_response_401_unauthorized_status(self):
        url = reverse('blog:api-v1:post-list')
        data = self.post_data
        response = self.client.post(
            path=url, data=data
        )
        assert response.status_code == 401

    def test_create_post_response_201_created_status(self, test_user):
        url = reverse('blog:api-v1:post-list')
        data = self.post_data
        self.client.force_authenticate(user=test_user)
        response = self.client.post(
            path=url, data=data
        )
        assert response.status_code == 201

    def test_create_post_response_400_bad_request_status(self, test_user):
        url = reverse('blog:api-v1:post-list')
        data = {}
        self.client.force_authenticate(user=test_user)
        response = self.client.post(
            path=url, data=data
        )
        assert response.status_code == 400
