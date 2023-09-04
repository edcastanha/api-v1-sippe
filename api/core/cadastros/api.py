from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from core.cadastros.models import Escolas, Pessoas, Presencas, Fotos
from core.cadastros.serializers import EscolasSerializer, PessoasSerializer, PresencasSerializer, FotosSerializer

class EscolasViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Escolas.objects.all()
    serializer_class = EscolasSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["get", "post", "patch", "delete"]



class PessoasViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Pessoas.objects.all()
    serializer_class = PessoasSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["get", "post", "patch", "delete"]


class PresencasViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Presencas.objects.all()
    serializer_class = PresencasSerializer
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
