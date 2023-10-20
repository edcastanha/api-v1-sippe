from rest_framework import permissions, viewsets
from core.cameras.models import NotaFiscal, Cameras, Locais, FrequenciasEscolar, Tarefas, Processamentos
from core.cameras.serializers import NotaFiscalSerializer, CamerasSerializer, LocaisSerializer, FrequenciasEscolarSerializer, TarefasSerializer, ProcessamentosSerializer

class NotaFiscalViewSet(viewsets.ModelViewSet):
    queryset = NotaFiscal.objects.all()
    serializer_class = NotaFiscalSerializer
    #permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get']

class CamerasViewSet(viewsets.ModelViewSet):
    queryset = Cameras.objects.all()
    serializer_class = CamerasSerializer
    #permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', ]
    #http_method_names = ['get', 'post', 'put', 'delete']

class LocaisViewSet(viewsets.ModelViewSet):
    queryset = Locais.objects.all()
    serializer_class = LocaisSerializer
    #permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', ]
    #http_method_names = ['get', 'post', 'put', 'delete']


class FrequenciasViewSet(viewsets.ModelViewSet):
    queryset = FrequenciasEscolar.objects.all()
    serializer_class = FrequenciasEscolarSerializer
    #permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["get"]

class TarefasViewSet(viewsets.ModelViewSet):
    queryset = Tarefas.objects.all()
    serializer_class = TarefasSerializer
    #permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["get",]
    
class ProssecamentosViewSet(viewsets.ModelViewSet):
    queryset = Processamentos.objects.all()
    serializer_class = ProcessamentosSerializer
    #permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["get",]