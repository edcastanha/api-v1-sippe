from django.http import HttpResponse
from .tasks import send_email


def index(request):
    send_email.delay()
    return HttpResponse("Mail request sent")