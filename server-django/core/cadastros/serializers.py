# from django.contrib.auth.models import User, Group
from rest_framework import serializers
from core.cadastros.models import Contratos, Escolas, Turmas, Pessoas, Fotos

class ContratosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contratos
        fields = '__all__'

class EscolasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Escolas
        fields = '__all__'

class TurmasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Turmas
        fields = '__all__'

class PessoasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pessoas
        fields = '__all__'

class FotosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fotos
        fields = '__all__'
