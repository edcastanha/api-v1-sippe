from django.shortcuts import render
from django.http import Http404
from core.cadastros.models import Turmas,  Pessoas
from core.cameras.models import FrequenciasEscolar

def index(request):
    template_html = 'cadastros/index.html'
    return render(request, template_html)

#def listAlunos(request):
#   data = []
#    turmas_list = Turmas.objects.prefetch_related('pessoas').all()
#    for turma in turmas_list:
#        alunos_count = len(turma.pessoas.all())
#        data.append({'turma': turma.nome, 'periodo': turma.periodo ,'count': alunos_count})
#
#    context = {"turmas": data}
#    return render(request, "cadastros/listaTurmas.html", context)

def listTurmas(request):
    data = []
    turmas_list = Turmas.objects.prefetch_related('aluno_set').all()
    for turma in turmas_list:
        alunos_count = turma.aluno_set.count()
        data.append({'turma': turma.nome, 'periodo': turma.periodo ,'count': alunos_count})

    context = {"turmas": data}
    return render(request, "cadastros/listaTurmas.html", context)


def detalhesTurma(request, turma_id):
    try:
        queryObject = Turmas.objects.get(pk=turma_id)
    except Turmas.DoesNotExist:
        raise Http404("Nao encontramos nenhum turma com essa descricao")
    return render(request, "cadastros/detalhesTurma.html", {"turma": queryObject})
