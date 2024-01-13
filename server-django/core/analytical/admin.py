from django.contrib import admin

# Register your models here.
from core.analytical.models import ImagensTratadas, FacesPrevisaoEmocional, FacesVerify

admin.site.register(ImagensTratadas)
admin.site.register(FacesPrevisaoEmocional)
admin.site.register(FacesVerify)

