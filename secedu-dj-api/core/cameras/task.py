from __future__ import absolute_import, unicode_literals

from celery import shared_task

from .models import Cameras, Escalas, Escolas, Locais

@shared_task
def extract_cameras():
    print("Extracting cameras")
    cameras = Cameras.objects.all()
    for camera in cameras:
        print(camera.acesso)