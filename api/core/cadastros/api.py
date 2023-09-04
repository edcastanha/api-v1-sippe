from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from core.cadastros.models import Contratos, Escolas, Pessoas, Fotos
from core.cadastros.serializers import ContratosSerializer, EscolasSerializer, PessoasSerializer, FotosSerializer

class ContratosViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Contratos.objects.all()
    serializer_class = ContratosSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["get"]

class EscolasViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Escolas.objects.all()
    serializer_class = EscolasSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["get"]

class PessoasViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Pessoas.objects.all()
    serializer_class = PessoasSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["get"]

class FotosViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Fotos.objects.all()
    serializer_class = FotosSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["get", "post", "patch", "delete"]
