from django.urls import include, path
from core.webApp import views

name_app = 'webApp'
urlpatterns = [
    path('', views.index, name='index'),
    path('turmas/', views.listTurmas, name='listar_turmas'),
    path('alunos/', views.listAlunos, name='listar_alunos'),
    path('tests/', views.listFrequencia, name='listar_frequencias'),
    path('testAnalyze/', views.testAnalyze, name='test_Analyze'),
    path('testVerify/', views.testVerify, name='test_Verify'),
    path('get_image_and_analyze/', views.get_image_and_analyze, name='get_image_and_analyze'),
]
