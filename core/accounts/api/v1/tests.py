from time import sleep

import pytest

from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
)


User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
class TestAccountsAPIRegistrations:
    @pytest.mark.parametrize(
        "email, password, password_confirm, status_code",
        [
            ("test_email@test.com", "123", "123", HTTP_400_BAD_REQUEST),
            ("test_email@test.com", "far!@#$%", "wpass", HTTP_400_BAD_REQUEST),
            ("wrong_email", "far!@#$%", "far!@#$%", HTTP_400_BAD_REQUEST),
            ("test_email@test.com", "far!@#$%", "far!@#$%", HTTP_201_CREATED),
        ],
    )
    def test_accounts_api_register_view(
            self, api_client, email, password, password_confirm,
            status_code, mailoutbox
    ):
        url = reverse("accounts:api-v1:register")
        data = {
            "email": email,
            "password": password,
            "confirm_password": password_confirm,
        }
        response = api_client.post(path=url, data=data)
        response_code = response.status_code

        sleep(1)
        assert response_code == status_code

        if response_code == HTTP_201_CREATED:
            print(mailoutbox)
            assert len(mailoutbox) == 1
