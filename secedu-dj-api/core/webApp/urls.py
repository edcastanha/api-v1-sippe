from django.urls import include, path
from core.webApp import views

name_app = 'webApp'
urlpatterns = [
    path('', views.index, name='index'),
    path('turmas/', views.listTurmas, name='listTurmas' ),
    path('alunos/', views.listTurmas, name='listAlunos' ),

   
]
