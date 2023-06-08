# from django.contrib.auth.models import User, Group
from rest_framework import serializers
from core.cadastros.models import Escolas, Pessoas, Presencas


class EscolasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Escolas
        fields = ['nome', 'cnpj']

class PessoasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pessoas
        fields = ['nome', 'cpf', 'escola', 'sexo', 'perfil']

class PresencasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Presencas
        fields = ['pessoa', 'data', 'hora', 'local']    
