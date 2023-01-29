from django.shortcuts import HttpResponse
from .tasks import task_send_email

# Create your views here.


def send_email(request):
    task_send_email.delay()
    return HttpResponse('<h1>Done sending</h1>')