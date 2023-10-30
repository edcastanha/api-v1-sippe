from django.urls import include, path
from rest_framework import routers
from core.cameras.api import NotaFiscalViewSet, CamerasViewSet, LocaisViewSet, FrequenciasViewSet, TarefasViewSet, ProssecamentosViewSet
# URLs DE API
router = routers.DefaultRouter()
router.register(r'notasfiscais', NotaFiscalViewSet, basename='notasfiscais')
router.register(r'cameras', CamerasViewSet, basename='cameras')
router.register(r'locais', LocaisViewSet, basename='locais')
router.register(r'frequencias', FrequenciasViewSet, basename='frequencias')
router.register(r'tarefas', TarefasViewSet, basename='tarefas')
router.register(r'processamentos', ProssecamentosViewSet, basename='processamentos')

#WEB APP
from core.cameras import views

urlpatterns = [
    path('', views.home, name='home'),
    
    #path('turmas/', views.listTurmas, name='listar_turmas'),
    #path('alunos/', views.listAlunos, name='listar_alunos'),



    # FREQUENCIAS ALUNOS
    #path('frequencias/alunos/', views.listFrequencia, name='listar_frequencias'),
    #path('frequencias/aluno/<int:aluno_id>/', views.frequenciaIndividual, name='frequencia_individual_aluno'),
    
    # SEMANAL ALUNO
    #path('frequencias/semana/atual/<int:aluno_id>/', views.frequenciaSemanaAtual, name='frequencia_semana_atual_aluno'),
    #path('frequencias/semana/anterior/<int:aluno_id>/', views.frequenciasSemanaAnterior, name='frequencia_semana_anterior_aluno'),

    # MES ALUNO
    #path('frequencias/atuais/', views.frequenciaAtuais, name='frequencias_mes_atual'),
    #path('frequencias/anteriores/', views.frequenciasAnteriores, name='frequencias_mes_anterior'),


    #path('analises/mensal', views.analiseMensal, name='listar_analise_mensal'),


    #path('testAnalyze/', views.testAnalyze, name='test_Analyze'),
    #path('testVerify/', views.testVerify, name='test_Verify'),
    #path('get_image_and_analyze/', views.get_image_and_analyze, name='get_image_and_analyze'),
]
 