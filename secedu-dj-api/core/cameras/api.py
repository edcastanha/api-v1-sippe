from rest_framework import permissions, viewsets
from core.cameras.models import NotaFiscal, Cameras, Locais, Frequencias
from core.cameras.serializers import NotaFiscalSerializer, CamerasSerializer, LocaisSerializer, FrequenciasSerializer

class NotaFiscalViewSet(viewsets.ModelViewSet):
    queryset = NotaFiscal.objects.all()
    serializer_class = NotaFiscalSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get']

class CamerasViewSet(viewsets.ModelViewSet):
    queryset = Cameras.objects.all()
    serializer_class = CamerasSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'post', 'put', 'delete']

class LocaisViewSet(viewsets.ModelViewSet):
    queryset = Locais.objects.all()
    serializer_class = LocaisSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'post', 'put', 'delete']

class FrequenciasViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Frequencias.objects.all()
    serializer_class = FrequenciasSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["get"]
