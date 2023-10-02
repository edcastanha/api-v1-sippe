from django.shortcuts import render
from celery import shared_task

# Create your views here.
@shared_task(name='start_consumer_path',bind=True, max_retries=3, default_retry_delay=10)
def IndexView(request):
    return render(request, 'index.html')
