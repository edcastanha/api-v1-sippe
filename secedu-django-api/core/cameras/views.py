from django.shortcuts import render
from django.contrib.auth.decorators import login_required 
from django.views.decorators.cache import cache_control 
#Utils function Django
from django.http import JsonResponse

# Function Querys personalizadas
from django.db.models import F, Subquery, OuterRef

# ======== Models ========
from core.cameras.models import Cameras, Processamentos

# Frontend
def frontend(request):
    return render(request, "frontend.html")


# Backend
@login_required(login_url="login")
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def backend(request):
    return render(request, "app/backend.html")


# ============ JSON ============
@login_required(login_url="login")
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def get_cameras(request):
    cameras = Cameras.objects.all()
    data = []
    for camera in cameras:
        data.append(camera.get_data())
        
    return JsonResponse(data, safe=False)

@login_required(login_url="login")
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def get_images_path(request):
   # SELECT CAMERAS QUE ESTÃO ATIVAS
    cameras = Cameras.objects.filter(status=True)

    data = []

    for camera in cameras:
        ultimos_registros = Processamentos.objects.filter(camera=camera, status='Processado').order_by('-id')[:3]
        
        for registro in ultimos_registros:
            data.append(registro.get_data())

    response = {"path": data}
    return JsonResponse(response, safe=False)