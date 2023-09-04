from django.urls import include, path
from django.contrib import admin
from rest_framework import routers
from core.cadastros.api import EscolasViewSet, PessoasViewSet, PresencasViewSet
from core.cameras.api import CamerasViewSet, LocaisViewSet

router = routers.DefaultRouter()

router.register(r'escolas', EscolasViewSet, basename='escolas')
router.register(r'pessoas', PessoasViewSet, basename='pessoas')
router.register(r'presencas', PresencasViewSet, basename='presencas')
router.register(r'cameras', CamerasViewSet, basename='cameras')
router.register(r'locais', LocaisViewSet, basename='locais')

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
]
