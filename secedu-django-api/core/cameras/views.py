from django.shortcuts import render
from django.contrib.auth.decorators import login_required # Login required to access private pagas
from django.views.decorators.cache import cache_control # Prevent back button (destroy the last section)

#Utils function Django
from django.db.models import Count
from django.db.models.functions import TruncDate
from django.db.models import Sum


# Models
from core.cameras.models import Cameras, Processamentos, Faces
from core.cadastros.models import Aluno


# Frontend
def frontend(request):
    return render(request, "frontend.html")


# Backend
@login_required(login_url="login")
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def backend(request):
    return render(request, "app/backend.html")

def total_processamentos_por_dia(request):
    # Obter o total de processamentos por dia
    total_processamentos_por_dia = Processamentos.objects.values('dia').annotate(total=Count('id')).order_by('dia')
    
def total_faces_por_dia(request):
    # Obter o total de faces por dia
    total_faces_por_dia = Faces.objects.select_related('processamento').values('processamento__dia').annotate(total_faces=Count('id')).order_by('processamento__dia')
    
    
    context = {
        'total_processamentos_por_dia': total_processamentos_por_dia,
        'total_faces_por_dia': total_faces_por_dia
    }