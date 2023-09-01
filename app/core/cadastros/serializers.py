# from django.contrib.auth.models import User, Group
from rest_framework import serializers
from core.cadastros.models import Escolas, Pessoas, Presencas, Fotos


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

class FotosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fotos
        fields = ['pessoa', 'foto1', 'foto2', 'foto3']
