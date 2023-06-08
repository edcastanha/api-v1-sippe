# from django.contrib.auth.models import User, Group
from rest_framework import serializers
from core.cameras.models import Cameras, Locais


class CamerasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cameras
        fields = ['id', 'descricao', 'ip', 'modelo', 'usuario', 'senha']

class LocaisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Locais
        fields = ['id', 'nome', 'descricao', 'camera']
    
