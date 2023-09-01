from django.contrib import admin

# Register your models here.
from core.cameras.models import Cameras, Locais

admin.site.register(Cameras)
admin.site.register(Locais)


