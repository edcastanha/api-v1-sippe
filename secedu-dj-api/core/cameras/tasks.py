from __future__ import absolute_import, unicode_literals
from celery import shared_task
from core.cameras.models import Cameras

@shared_task
def extract_cameras():
    print("Extracting cameras")
    cameras = Cameras.objects.all()
    for camera in cameras:
        print(camera.acesso)