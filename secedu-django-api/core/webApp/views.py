from django.shortcuts import render
from django.http import Http404
from core.cadastros.models import Turmas,  Aluno
from core.cameras.models import FrequenciasEscolar

def index(request):
    alunos_list = Aluno.objects.all()
    context = {"alunos": alunos_list}
    template_html = 'cadastros/index.html'
    
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
    
    return render(request, "cadastros/turmas/listaTurmas.html", context)

def detalhesTurma(request, turma_id):
    try:
        queryObject = Turmas.objects.get(pk=turma_id)
        context = {"turma": queryObject}
    except Turmas.DoesNotExist:
        raise Http404("Nao encontramos nenhum turma com essa descricao")
    return render(request, "cadastros/turmas/listaTurmas.html", context)

#ALUNOS
def listAlunos(request):
    # Use annotate para contar o número de alunos associados a cada pessoa
    try:
        alunos_list = Aluno.objects.all()
    except Aluno.DoesNotExist:
        raise Http404("Nao encontramos nenhum aluno com essa descricao")
    
    context = {"alunos": alunos_list}
    return render(request, "cadastros/alunos/listaAlunos.html", context)