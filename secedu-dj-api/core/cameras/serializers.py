# from django.contrib.auth.models import User, Group
from rest_framework import serializers
from core.cameras.models import NotaFiscal, Cameras, Locais, FrequenciasEscolar, Tarefas

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

class FrequenciasEscolarSerializer(serializers.ModelSerializer):
    class Meta:
        model = FrequenciasEscolar
        fields = ['aluno', 'local' ,'data', 'turma', ] 

class TarefasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tarefas
        fields = ['id', 'nome', 'descricao', 'status', 'escalas']
