from rest_framework import permissions, viewsets
from core.cameras.models import Cameras, Locais
from core.cameras.serializers import CamerasSerializer, LocaisSerializer

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
