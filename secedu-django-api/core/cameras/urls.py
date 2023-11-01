from django.urls import include, path
from rest_framework import routers
from core.cameras.api import NotaFiscalViewSet, CamerasViewSet, LocaisViewSet, FrequenciasViewSet, TarefasViewSet, ProssecamentosViewSet
# URLs DE API
router = routers.DefaultRouter()
router.register(r'notasfiscais', NotaFiscalViewSet, basename='notasfiscais')
router.register(r'cameras', CamerasViewSet, basename='cameras')
router.register(r'locais', LocaisViewSet, basename='locais')
router.register(r'frequencias', FrequenciasViewSet, basename='frequencias')
router.register(r'tarefas', TarefasViewSet, basename='tarefas')
router.register(r'processamentos', ProssecamentosViewSet, basename='processamentos')

#WEB APP
from core.cameras import views

urlpatterns = [
    # Frontend
    path('', views.frontend, name="frontend"),
    # Login/Logout
    path('login/', include('django.contrib.auth.urls')),

    # Backend
    path('backend/', views.backend, name="backend"),
]
