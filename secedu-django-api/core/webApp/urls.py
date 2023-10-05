from django.urls import include, path
from core.webApp import views

name_app = 'webApp'
urlpatterns = [
    path('', views.index, name='index'),
    path('turmas/', views.listTurmas, name='listar_turmas'),
    path('alunos/', views.listAlunos, name='listar_alunos'),
    path('send/', views.send, name='send'),
]
