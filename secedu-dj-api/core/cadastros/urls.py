from django.urls import include, path
from rest_framework import routers
from core.cadastros.api import ContratosViewSet, EscolasViewSet, PessoasViewSet, FotosViewSet

router = routers.DefaultRouter()
router.register(r'contratos', ContratosViewSet, basename='contratos')
router.register(r'escolas', EscolasViewSet, basename='escolas')
router.register(r'pessoas', PessoasViewSet, basename='pessoas')
router.register(r'fotos', FotosViewSet, basename='fotos')

urlpatterns = [
    path('', include(router.urls)),
]
