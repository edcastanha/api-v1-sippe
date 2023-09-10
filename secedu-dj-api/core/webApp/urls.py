from django.urls import include, path
from core.webApp import views

urlpatterns = [
    path('', views.index, name='index' ), #API REST
]
