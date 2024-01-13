
from django.shortcuts import render
from django.contrib.auth.decorators import login_required # Login required to access private pagas
from django.views.decorators.cache import cache_control # Prevent back button (destroy the last section)

#Utils function Django
from django.db.models import Count
from django.db.models.functions import TruncDate
from django.db.models import Sum
from django.http import JsonResponse


# ======== Models ========
from core.cameras.models import Cameras, Processamentos, Faces
from core.cadastros.models import Aluno, Pessoas

# ======== Frontend ========
# Listar Pessoas
@login_required(login_url="login")
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def listar_pessoas(request):
    return render(request, 'app/pages/listar-pessoas.html')


# Alunos
@login_required(login_url="login")
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def listar_alunos(request):
    objs = Aluno.objects.all()
    data = [obj.get_data() for obj in objs]
    response = {'alunos':data}
    return render(request, 'app/pages/listar-alunos.html', response)

# ============ JSON ============

@login_required(login_url="login")
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def pessoas_json(request):
    objs = Aluno.objects.all()
    data = [obj.get_data() for obj in objs]
    response = {'data':data}
    return JsonResponse(response)