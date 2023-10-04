from django.contrib import admin

# Register your models here.
from core.cameras.models import Cameras, Locais, FrequenciasEscolar, NotaFiscal, Tarefas

admin.site.register(NotaFiscal)
admin.site.register(Cameras)
admin.site.register(Locais)
admin.site.register(FrequenciasEscolar)
admin.site.register(Tarefas)
