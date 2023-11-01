from django.urls import include, path
from rest_framework import routers
from core.cadastros.api import ContratosViewSet, EscolasViewSet, TurmasViewSet, PessoasViewSet, FotosViewSet
router = routers.DefaultRouter()
router.register(r'contratos', ContratosViewSet, basename='contratos')
router.register(r'escolas', EscolasViewSet, basename='escolas')
router.register(r'turmas', TurmasViewSet, basename= 'turmas')
router.register(r'pessoas', PessoasViewSet, basename='pessoas')
router.register(r'fotos', FotosViewSet, basename='fotos')

from core.cadastros import views 

urlpatterns = [
    # API REST
    path('cadastros', include(router.urls)),

    # Frontend
    path('listar_pessoas/', views.listar_pessoas, name="listar_pessoas"),
    path('listar_alunos/', views.listar_alunos, name="listar_alunos"),
    # JSON
    path('pessoas/json/', views.pessoas_json, name="pessoas_json"),
]
