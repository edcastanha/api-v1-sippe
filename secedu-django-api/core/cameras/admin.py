from django.contrib import admin
from django.utils.html import format_html
from core.cameras.models import Cameras, Locais, FrequenciasEscolar, NotaFiscal, Tarefas, Processamentos, Faces

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
admin.site.register(FrequenciasEscolar)
admin.site.register(Tarefas)
#admin.site.register(Processamentos)
@admin.register(Processamentos)
class ProcessamentosAdmin(admin.ModelAdmin):
    list_filter = ('status',)


class FacesAdmin(admin.ModelAdmin):

    def foto_preview(self, obj):
        return format_html(
            f"<img src='{obj.path_face} style='border-radius: 50% 50%;'/>")


    readonly_fields = ['foto_preview']
    list_display = ('id', 'processamento', 'auditado', 'backend_detector')
    list_filter = ('auditado', 'backend_detector')
    search_fields = ('processamento__dia', 'processamento__horario')

admin.site.register(Faces, FacesAdmin)
#admin.site.register(Faces)


