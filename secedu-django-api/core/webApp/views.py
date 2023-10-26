from itertools import count
from django.shortcuts import render
from django.http import Http404
from django.conf import settings
from core.cadastros.models import Turmas,  Aluno
from core.cameras.models import Faces, FrequenciasEscolar
import os
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from core.loggingMe import logger

from datetime import date, timedelta
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.db.models import Count



capture_path = settings.MEDIA_ROOT + '/capturas/'
#logger.debug(f'Path de capturas: {capture_path}')

def index(request):
    alunos_list = Aluno.objects.all()
    context = {"alunos": alunos_list}
    template_html = 'index.html'
    
    return render(request, template_html, context)

def listTurmas(request):
    try:
        data = []
        turmas_list = Turmas.objects.prefetch_related('aluno_set').all()
        for turma in turmas_list:
            alunos_count = turma.aluno_set.count()
            data.append({'turma': turma.nome, 'periodo': turma.periodo , 'atualizado': turma.data_atualizacao , 'count': alunos_count})
        context = {"turmas": data}
    except Turmas.DoesNotExist:
        raise Http404("Nao encontramos nenhuma turma com essa descricao")
    
    return render(request, "turmas/listar_turmas.html", context)

def detalhesTurma(request, turma_id):
    try:
        queryObject = Turmas.objects.get(pk=turma_id)
        context = {"turma": queryObject}
    except Turmas.DoesNotExist:
        raise Http404("Nao encontramos nenhum turma com essa descricao")
    return render(request, "turmas/listar_turmas.html", context)

#ALUNOS
def listAlunos(request):
    # Use annotate para contar o número de alunos associados a cada pessoa
    try:
        alunos_list = Aluno.objects.all()
    except Aluno.DoesNotExist:
        raise Http404("Nao encontramos nenhum aluno com essa descricao")
    
    context = {"alunos": alunos_list}
    return render(request, "alunos/listar_alunos.html", context)

def listFrequencia(request):
    try:
        data = []
        frequencias_list = FrequenciasEscolar.objects.all()
        for frequencia in frequencias_list:
            data.append(
                {'aluno': frequencia.aluno, 
                 'matricula': frequencia.aluno.matricula, 
                 'turma': frequencia.aluno.turma.nome,
                 'local': frequencia.camera.descricao , 
                 'data': frequencia.data, 
                 'presente': 'Sim'
                 })
        context = {"results": data}
    except FrequenciasEscolar.DoesNotExist:
        raise Http404("Nao encontramos nenhuma frequencia com essa descricao")
    
    return render(request, "frequencias/listar_frequencias.html", context)

def frequenciaIndividual(request, aluno_id):
    try:
        data = []
        aluno = get_object_or_404(Aluno, pk=aluno_id)
        
        # Contagem de registros relacionados a um aluno específico
        frequencia_aluno = FrequenciasEscolar.objects.filter(aluno=aluno).count()
        
        data.append({
            'id': aluno_id,  # ID do aluno
            'nome': aluno.pessoa.nome,
            'matricula': aluno.matricula,
            'turma': aluno.turma.nome,
            'total_registros': frequencia_aluno,  # Número total de registros relacionados a este aluno
        })

        context = {"results": data}
    except Aluno.DoesNotExist:
        raise Http404("Aluno não encontrado")
    
    return render(request, "frequencias/frequencia_individual_aluno.html", context)


## Frequencias da mesna SEMANA
def frequenciaAtuais(request):
    try:
        data = []
        today = date.today()
        #next_monday = today + timedelta(days=(7 - today.weekday())) #Semana Atual
        #next_monday = today - timedelta(days=today.weekday() + 7) #Semana Anterior
        # Se hoje for domingo, obtenha a data da segunda-feira da semana anterior
        if today.weekday() == 6:  # 6 representa domingo
            last_monday = today - timedelta(days=6) - timedelta(weeks=1)
        else:
            # Caso contrário, obtenha a data da segunda-feira da semana atual
            last_monday = today - timedelta(days=today.weekday())
        
        alunos = Aluno.objects.all()
        for aluno in alunos:
            frequencia_aluno = FrequenciasEscolar.objects.filter(
                aluno=aluno,
                data__gte=last_monday,
                data__lte=last_monday + timedelta(days=4)
            ).order_by('data')
            
            if frequencia_aluno:
                for freq in frequencia_aluno:
                    data.append({
                        'aluno': aluno,
                        'matricula': aluno.matricula,
                        'turma': aluno.turma.nome,
                        'local': freq.camera.descricao,
                        'data': freq.data,
                        
                    })
            else:
                for day in range(5):
                    data.append({
                        'aluno': aluno,
                        'matricula': aluno.matricula,
                        'turma': aluno.turma.nome,
                        'local': '- - -',
                        'data': last_monday + timedelta(days=day),
                        'presente': 'Não'
                    })
        
        context = {"results": data}
    except Aluno.DoesNotExist:
        raise Http404("Aluno não encontrado")
    
    return render(request, "alunos/listar_frequencias.html", context)

# Frequencias da SEMANA ANTERIOR
def frequenciasAnteriores(request):
    try:
        data = []
        today = date.today()

        # Se hoje for domingo, obtenha a data da segunda-feira da semana anterior
        if today.weekday() == 6:  # 6 representa domingo
            last_monday = today - timedelta(days=6)
            last_friday = today - timedelta(days=2)
        else:
            # Caso contrário, obtenha a data da segunda-feira da semana atual
            last_monday = today - timedelta(days=today.weekday())
            last_friday = today - timedelta(days=today.weekday() - 4)
        
        alunos = Aluno.objects.all()
        for aluno in alunos:
            frequencia_aluno = FrequenciasEscolar.objects.filter(
                aluno=aluno,
                data__gte=last_monday,
                data__lte=last_friday
            ).order_by('data')
            
            if frequencia_aluno:
                for freq in frequencia_aluno:
                    data.append({
                        'aluno': aluno,
                        'matricula': aluno.matricula,
                        'turma': aluno.turma.nome,
                        'local': freq.camera.descricao,
                        'data': freq.data,
                        'presente': 'Sim',
                    })
            else:
                for day in range(5):
                    data.append({
                        'aluno': aluno,
                        'matricula': aluno.matricula,
                        'turma': aluno.turma.nome,
                        'local': '- - -',
                        'data': last_monday + timedelta(days=day),
                        'presente': 'Não'
                    })
        
        context = {"results": data}
    except Aluno.DoesNotExist:
        raise Http404("Aluno não encontrado")
    
    return render(request, "alunos/listar_frequencias.html", context)

def frequenciaSemanaAtual(request, aluno_id):
    try:
        data = []
        aluno = get_object_or_404(Aluno, pk=aluno_id)
        today = date.today()

        if today.weekday() == 6:
            last_monday = today - timedelta(days=6) - timedelta(weeks=1)
        else:
            last_monday = today - timedelta(days=today.weekday())
        
        frequencia_aluno = FrequenciasEscolar.objects.filter(
            aluno=aluno,
            data__gte=last_monday,
            data__lte=last_monday + timedelta(days=4)
        ).order_by('data')
        
        if frequencia_aluno:
            for freq in frequencia_aluno:
                data.append({
                    'aluno': aluno,
                    'matricula': aluno.matricula,
                    'turma': aluno.turma.nome,
                    'local': freq.camera.descricao,
                    'data': freq.data,
                    'presente': 'Sim',
                })
        else:
            for day in range(5):
                data.append({
                    'aluno': aluno,
                    'matricula': aluno.matricula,
                    'turma': aluno.turma.nome,
                    'local': '- - -',
                    'data': last_monday + timedelta(days=day),
                    'presente': 'Não'
                })
        
        context = {"results": data}
    except Aluno.DoesNotExist:
        raise Http404("Aluno não encontrado")
    
    return render(request, "frequencias/frequencias_semana_atual_aluno.html", context)

def frequenciasSemanaAnterior(request, aluno_id):
    try:
        data = []
        aluno = get_object_or_404(Aluno, pk=aluno_id)
        today = date.today()
        
        # Defina as datas de segunda-feira e sexta-feira da semana anterior (de 16 a 20)
        last_monday = today - timedelta(days=today.weekday() + 7)
        last_friday = last_monday + timedelta(days=4)

        frequencia_aluno = FrequenciasEscolar.objects.filter(
            aluno=aluno,
            data__gte=last_monday,
            data__lte=last_friday
        ).order_by('data')
        
        if frequencia_aluno:
            for freq in frequencia_aluno:
                data.append({
                    'aluno': aluno,
                    'matricula': aluno.matricula,
                    'turma': aluno.turma.nome,
                    'local': freq.camera.descricao,
                    'data': freq.data,
                    'presente': 'Sim',
                })
        else:
            for day in range(5):
                data.append({
                    'aluno': aluno,
                    'matricula': aluno.matricula,
                    'turma': aluno.turma.nome,
                    'local': '- - -',
                    'data': last_monday + timedelta(days=day),
                    'presente': 'Não'
                })
                
        context = {"results": data}
    except Aluno.DoesNotExist:
        raise Http404("Aluno não encontrado")
    
    return render(request, "frequencias/frequencias_semana_anterior_aluno.html", context)


# ANALISES EMOÇÕES
def analiseMensal(request):
    faces = Faces.objects.all()




## API DeepFace Network
def testAnalyze(request):
    return render(request, "dashboards/testAnalyze.html")

def testVerify(request):
    return render(request, "dashboards/testVerify.html")

@csrf_exempt  # Use apenas se você desativou o CSRF para essa view
def get_image_and_analyze(request):
    if request.method == 'POST':
        # Receba a imagem enviada no corpo da solicitação
        image_file = request.FILES.get('image')
        #logger.debug('Recebida solicitação de análise de imagem.')
        # Verifique se o arquivo é uma imagem
        if image_file and image_file.name.endswith(('.jpg', '.jpeg', '.png')):
            # Salve a imagem em 'capturas'
            #logger.debug(f'Salvando imagem em capturas: {capture_path}')
            image_path = os.path.join(capture_path, image_file.name)
            img_url = os.path.join('media/capturas/', image_file.name)
            #logger.debug(f'Imagem salva em: {image_path}')
            #logger.debug(f'URL da imagem: {img_url}')
            with open(image_path, 'wb') as destination:
                for chunk in image_file.chunks():
                    destination.write(chunk)

            # Faça uma solicitação para 'localhost:5000/analyze'
            analyze_url = 'http://secedu-face:5000/analyze_mediapipe'
            #logger.debug(f'Enviando API externa: {analyze_url}')
            
            response = requests.post(analyze_url, json={'img_path': img_url, 'actions': ['emotion',] })

            #logger.debug(f'Delete de : {image_path}')
            if response.status_code == 200:
                data = response.json()
                # Deletar a imagem após a análise
                os.remove(image_path)
                logger.debug(f'Retorno Analisada=> {data}')
                return JsonResponse(data, status=200, safe=False) # Retorne os dados da análise como JSON
            else:
                return JsonResponse({'error': 'Erro na solicitação à API externa'}, status=500)
        else:
            return JsonResponse({'error': 'Arquivo inválido. Envie uma imagem JPG ou PNG.'}, status=400)

    return JsonResponse({'error': 'Método não suportado.'}, status=405)