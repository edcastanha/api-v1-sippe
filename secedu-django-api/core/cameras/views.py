from django.shortcuts import render
from django.contrib.auth.decorators import login_required 
from django.views.decorators.cache import cache_control 
#Utils function Django
from django.http import JsonResponse

# Function Querys personalizadas
from django.db.models import Max, Min, Avg, Count

# ======== Models ========
from core.cameras.models import Cameras, Processamentos, Faces, FrequenciasEscolar
from core.analytical.models import FacesPrevisaoEmocional

# Frontend
def frontend(request):
    return render(request, "frontend.html")


# Backend
@login_required(login_url="login")
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def backend(request):
    registros_ordenados = 0
    registros_ultimos_dia = 0
    media_registros = 0
    campos_emocao = ['zangado', 'repulsa', 'medo', 'feliz', 'neutro', 'triste', 'surpresa']
    results = {}
    min_value = 0
    media_value = 0
    max_value = 0
    pessoas_com_registros = None
    faces = None
    frequencias_values = []

    faces_ordenados = 0
    faces_ultimos_dia = 0
    media_faces = 0


    
    try:
        # Consulta para obter todos os registros e ordená-los por dia em ordem decrescente
        registros_ordenados = Processamentos.objects.values('dia').annotate(registros=Count('id')).order_by('-dia')
        # Pegue os 5 últimos registros
        registros_ultimos_dia = registros_ordenados[:5]
        # Resultados - # Média de registros por dia ou media_registros igual a zero
        media_registros = Processamentos.objects.all().count() / len(registros_ordenados)
    except Exception as e:
        print(f"Não há registros de processamento ou {e}.")


    # Consulta por ordem de dia todas as faces detectadas
    try:
        faces_ordenados = Faces.objects.values('processamento__dia').annotate(faces=Count('id')).order_by('-processamento__dia')
        # Pegue os 5 últimos registros
        faces_ultimos_dia = faces_ordenados[:5]
        # Resultados - # Média de faces por dia ou media_faces igual a zero
        media_faces = Faces.objects.all().count() / len(faces_ordenados)
        #print(f"Faces: {faces_ordenados} - {faces_ultimos_dia} - {media_faces}")
    except Exception as e:

        print(f"Não há registros de faces detectadas ou {e}.")


    # ---- Emotions
    try:
        for campo in campos_emocao:
            #min_value = FacesPrevisaoEmocional.objects.filter(**{f'{campo}__gt': 10}).aggregate(Min(campo))[f'{campo}__min']
            min_value = FacesPrevisaoEmocional.objects.aggregate(Min(campo))[f'{campo}__min']
            media_value = FacesPrevisaoEmocional.objects.filter(**{f'{campo}__gte': 5, f'{campo}__lte': 20}).aggregate(Avg(campo))[f'{campo}__avg']
            max_value = FacesPrevisaoEmocional.objects.aggregate(Max(campo))[f'{campo}__max']
            media_value = FacesPrevisaoEmocional.objects.aggregate(Avg(campo))[f'{campo}__avg']

            results[campo] = [min_value, max_value, media_value]
    except Exception as e:
        print(f"Não há registros de emoções ou {e}.")


    # Consulta para obter a lista de pessoas que têm registros e seus nomes
    try:
        pessoas_com_registros = FrequenciasEscolar.objects.values('pessoa__id', 'pessoa__nome').annotate(contagem=Count('pessoa')).filter(contagem__gt=0)

        # O resultado será um queryset contendo o ID da pessoa, o nome e a contagem de registros
        for pessoa in pessoas_com_registros:
            pessoa_id = pessoa['pessoa__id']
            nome = pessoa['pessoa__nome']
            contagem = pessoa['contagem']
            frequencias_values.append({'id': pessoa_id, 'nome': nome, 'contagem': contagem})
            print(f'Pessoa com ID {pessoa_id} (Nome: {nome}) tem {contagem} registros.')
    except Exception as e:
        print(f"Não há registros de frequência escolar ou {e}.")

    try:
        # Consulta para obter as 3 últimas faces detectadas
        faces = Faces.objects.all().order_by('-id')
    except Exception as e:
        print(f"Não há registros de faces detectadas ou {e}.")
        
    context = {
        'faces': faces,
        'results': results,
        'media_registros': int(media_registros),
        'registros_ultimos_dia': registros_ultimos_dia,
        'media_faces': int(media_faces),
        'faces_ultimos_dia': faces_ultimos_dia,
        'frequencias_values': frequencias_values,
    }

    return render(request, "app/backend.html", context)


# Backend
@login_required(login_url="login")
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def frequencia_view(request,  id):
    # Consulta para obter registros de FrequenciasEscolar relacionados à pessoa com o ID específico
    registros = FrequenciasEscolar.objects.filter(pessoa_id=id)
    print(f"Registros: {registros}")
    context = {
        'registros': registros,
    }

    return render(request, "app/pages/frequencia_view.html", context)










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