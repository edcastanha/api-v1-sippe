from django.urls import include, path
from rest_framework import routers
from core.cadastros.api import EscolasViewSet, PessoasViewSet, PresencasViewSet

router = routers.DefaultRouter()
router.register(r'escolas', EscolasViewSet, basename='escolas')
router.register(r'pessoas', PessoasViewSet, basename='pessoas')
router.register(r'presencas', PresencasViewSet, basename='presencas')


urlpatterns = [
    path('', include(router.urls)),
]
