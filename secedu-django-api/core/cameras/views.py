from django.shortcuts import render
from django.contrib.auth.decorators import login_required 
from django.views.decorators.cache import cache_control 
#Utils function Django
from django.http import JsonResponse

# Function Querys personalizadas
from django.db.models import Max, Min
from django.db.models import Count

# ======== Models ========
from core.cameras.models import Cameras, Processamentos, Faces
from core.analytical.models import FacesPrevisaoEmocional

# Frontend
def frontend(request):
    return render(request, "frontend.html")


# Backend
@login_required(login_url="login")
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def backend(request):

    # Consulta para obter todos os registros e ordená-los por dia em ordem decrescente
    registros_ordenados = Processamentos.objects.values('dia').annotate(registros=Count('id')).order_by('-dia')

    # Pegue os 5 últimos registros
    registros_ultimos_dia = registros_ordenados[:5]

    # Resultados
    media_registros = Processamentos.objects.all().count() / len(registros_ordenados)
    print(registros_ordenados)
    print(registros_ultimos_dia)
    #for item in registros_por_dia:
    #    print(f"No dia {item['dia']}: Quantidade de registros - {item['registros']}")
    
    # ---- Emotions
     # Lista de campos de emoção que você deseja analisar
    campos_emocao = ['zangado', 'repulsa', 'medo', 'feliz', 'neutro', 'triste', 'surpresa']

    # Inicialize um dicionário para armazenar os resultados
    results = {}

    # Crie uma consulta para cada campo de emoção e obtenha os valores máximos e mínimos
    for campo in campos_emocao:
        max_value = FacesPrevisaoEmocional.objects.aggregate(Max(campo))[f'{campo}__max']
        min_value = FacesPrevisaoEmocional.objects.aggregate(Min(campo))[f'{campo}__min']
        results[campo] = [min_value, max_value]

    faces = Faces.objects.all().order_by('-id')[:10]

    context = {
        'faces': faces,
        'results': results,
        'media_registros': int(media_registros),
        'registros_ultimos_dia': registros_ultimos_dia,
    }

    return render(request, "app/backend.html", context)


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