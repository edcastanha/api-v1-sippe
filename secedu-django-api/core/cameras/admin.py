from django.contrib import admin
from core.cameras.models import Cameras, Locais, FrequenciasEscolar, NotaFiscal, Tarefas, Processamentos

# class CamerasAdmin(admin.ModelAdmin):
#     list_display = ('data_cadastro', 'data_atualizacao', 'descricao', 'acesso', 'modelo', )
#     list_filter = ('data_cadastro', 'modelo', 'status')
#     search_fields = ('descricao',  'modelo', 'usuario')

admin.site.register(Cameras)
admin.site.register(Processamentos)
admin.site.register(NotaFiscal)
admin.site.register(Locais)
admin.site.register(FrequenciasEscolar)
admin.site.register(Tarefas)
