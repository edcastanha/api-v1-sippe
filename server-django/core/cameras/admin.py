from django.contrib import admin
from django.conf import settings
from django.utils.html import format_html
from core.cameras.models import Cameras, Locais, FrequenciasEscolar, NotaFiscal, Tarefas, Processamentos, Faces
from django.utils.safestring import mark_safe

# Primeiro, tenta desregistrar o modelo, se já estiver registrado
if admin.site.is_registered(FrequenciasEscolar):
    admin.site.unregister(FrequenciasEscolar)

class FrequenciasEscolarAdmin(admin.ModelAdmin):
    readonly_fields = ['exibir_file_dataset', 'exibir_caminho_do_face']

    def exibir_file_dataset(self, obj):
        if obj.file_dataset:
            return mark_safe(f'<img src="{obj.file_dataset}" style="max-width: 200px; max-height: 200px;" />')
        else:
            return 'Nenhuma imagem disponível'

    exibir_file_dataset.short_description = 'Imagem Face Dataset'

    def exibir_caminho_do_face(self, obj):
        if obj.caminho_do_face:
            print(f"{BASE_URL}/{obj.caminho_do_face}")

            return mark_safe(f'<img src="{obj.caminho_do_face}" style="max-width: 200px; max-height: 200px;" />')
        else:
            return 'Nenhuma imagem disponível'

    exibir_caminho_do_face.short_description = 'Imagem Face Detectada'

admin.site.register(FrequenciasEscolar, FrequenciasEscolarAdmin)

# class CamerasAdmin(admin.ModelAdmin):
#     list_display = ('data_cadastro', 'data_atualizacao', 'descricao', 'acesso', 'modelo', )
#     list_filter = ('data_cadastro', 'modelo', 'status')
#     search_fields = ('descricao',  'modelo', 'usuario')

#from django.utils.html import format_html
#class FacesAdmin(admin.ModelAdmin):
#    list_display = ('exibir_imagem', 'processamento', 'auditado')
#    list_filter = ('auditado',)  # Filtros para a coluna "auditado"
    #def exibir_imagem(self, obj):
        # Substitua 'media' pelo caminho correto para a pasta de mídia onde as imagens estão armazenadas
    #    return format_html('<img src="{}" style="max-width:224px; max-height:224px" width=224  />', obj.path_face)
    #exibir_imagem.allow_tags = True
    #exibir_imagem.short_description = 'Imagem'

admin.site.register(Cameras)
admin.site.register(NotaFiscal)
admin.site.register(Locais)
#admin.site.register(FrequenciasEscolar)
admin.site.register(Tarefas)
#admin.site.register(Processamentos)

@admin.register(Processamentos)
class ProcessamentosAdmin(admin.ModelAdmin):
    list_filter = ('status',)


class FacesAdmin(admin.ModelAdmin):

    def foto_preview(self, obj):
        print(f"{BASE_URL}/{obj.path_face}")
        return format_html(f"<img src='{BASE_URL}/{obj.path_face}' style='border-radius: 50% 50%;'/>")


    readonly_fields = ['foto_preview']
    list_display = ('id', 'processamento', 'auditado', 'backend_detector')
    list_filter = ('status',)
    search_fields = ('processamento__dia', 'processamento__horario',)

admin.site.register(Faces, FacesAdmin)
#admin.site.register(Faces)


