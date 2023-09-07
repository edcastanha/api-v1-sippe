# from django.contrib.auth.models import User, Group
from rest_framework import serializers
from core.cameras.models import NotaFiscal, Cameras, Locais, Frequencias

class NotaFiscalSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotaFiscal
        fields = ['id', 'numero', 'data']

class CamerasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cameras
        fields = ['id', 'nf', 'descricao', 'acesso', 'modelo']

class LocaisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Locais
        fields = ['id', 'nome', 'descricao', 'camera', 'ponto']

class FrequenciasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Frequencias
        fields = ['pessoa', 'local' ,'data', 'hora'] 
