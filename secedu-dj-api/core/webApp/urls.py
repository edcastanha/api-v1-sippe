from django.urls import include, path
from core.webApp import views

urlpatterns = [
    path('home', views.index, name='index' ), #API REST
]
