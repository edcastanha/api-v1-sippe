from django.contrib import admin

# Register your models here.
from core.cameras.models import Cameras, Locais, Frequencias

admin.site.register(Cameras)
admin.site.register(Locais)
admin.site.register(Frequencias)



