import requests

from django.http import HttpResponse, JsonResponse
from django.core.cache import cache
from django.views.decorators.cache import cache_page

from .tasks import task_send_email

# Create your views here.


def send_email(request):
    task_send_email.delay()
    return HttpResponse('<h1>Done sending</h1>')

@cache_page(timeout=60 * 3)
def test_mock_server(request):
    mock_server_url = 'https://aa02dcd4-6b71-4c0f-9da3-fad520be54ec.mock.pstmn.io/test/delay/5'
    response = requests.get(url=mock_server_url)

    return JsonResponse(response.json())
