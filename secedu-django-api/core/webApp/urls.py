from django.urls import include, path
from core.webApp import views

name_app = 'webApp'
urlpatterns = [
    path('', views.index, name='index'),
    
    path('turmas/', views.listTurmas, name='listar_turmas'),
    path('alunos/', views.listAlunos, name='listar_alunos'),



    # FREQUENCIAS ALUNOS
    path('frequencias/alunos/', views.listFrequencia, name='listar_frequencias'),
    path('frequencias/aluno/<int:aluno_id>/', views.frequenciaIndividual, name='frequencia_individual_aluno'),
    # SEMANAL ALUNO
    path('frequencias/semana/atual/<int:aluno_id>/', views.frequenciaSemanaAtual, name='frequencia_semana_atual_aluno'),
    path('frequencias/semana/anterior/<int:aluno_id>/', views.frequenciasSemanaAnterior, name='frequencia_semana_anterior_aluno'),

    # GERAL
    path('frequencias/atuais/', views.frequenciaAtuais, name='frequencias_mes_atual'),
    path('frequencias/anteriores/', views.frequenciasAnteriores, name='frequencias_mes_anterior'),




    path('testAnalyze/', views.testAnalyze, name='test_Analyze'),
    path('testVerify/', views.testVerify, name='test_Verify'),
    path('get_image_and_analyze/', views.get_image_and_analyze, name='get_image_and_analyze'),
]
