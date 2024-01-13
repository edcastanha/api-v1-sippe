# from django.contrib.auth.models import User, Group
from rest_framework import serializers
from core.cadastros.models import Aluno, Escalas
from core.cameras.models import NotaFiscal, Cameras, Locais, FrequenciasEscolar, Tarefas, Processamentos

class AlunoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aluno
        fields = '__all__'
    


class NotaFiscalSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotaFiscal
        fields = '__all__'

class CamerasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cameras
        fields = '__all__'

class LocaisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Locais
        fields = '__all__'
class FrequenciasEscolarSerializer(serializers.ModelSerializer):
    #aluno = serializers.PrimaryKeyRelatedField(many=True, queryset=Aluno.objects.all())
    class Meta:
        model = FrequenciasEscolar
        fields = '__all__'

class EscalasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Escalas
        fields = '__all__'

class TarefasSerializer(serializers.ModelSerializer):
    escalas = EscalasSerializer()
    cameras = CamerasSerializer()

    class Meta:
        model = Tarefas
        fields = '__all__'


class ProcessamentosSerializer(serializers.ModelSerializer):

    class Meta:
        model = Processamentos
        fields = '__all__'
