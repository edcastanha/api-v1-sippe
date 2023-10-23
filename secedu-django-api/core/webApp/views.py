from django.shortcuts import render
from django.http import Http404
from django.conf import settings
from core.cadastros.models import Turmas,  Aluno
from core.cameras.models import FrequenciasEscolar
import os
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from core.loggingMe import logger

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
    
    return render(request, "turmas/listaTurmas.html", context)

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
            logger.debug(f'Frequencias: {frequencia}')
            data.append({'aluno': frequencia.aluno, 'matricula': frequencia.aluno.matricula, 'local': frequencia.camera.descricao , 'data': frequencia.data})
        context = {"results": data}
    except FrequenciasEscolar.DoesNotExist:
        raise Http404("Nao encontramos nenhuma frequencia com essa descricao")
    
    return render(request, "alunos/listar_frequencias.html", context)
    
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