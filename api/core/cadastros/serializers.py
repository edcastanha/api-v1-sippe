# from django.contrib.auth.models import User, Group
from rest_framework import serializers
from core.cadastros.models import Contratos, Escolas, Pessoas, Fotos

class ContratosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contratos
        fields = ['protocolo', 'assinado_em', 'responsavel']

class EscolasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Escolas
        fields = ['nome', 'cnpj']

class PessoasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pessoas
        fields = ['nome', 'cpf', 'escola', 'sexo', 'perfil']   

class FotosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fotos
        fields = ['pessoa', 'foto']
