from django.shortcuts import render
from django.contrib.auth.decorators import login_required # Login required to access private pagas
from django.views.decorators.cache import cache_control # Prevent back button (destroy the last section)

# Models
from core.cameras.models import Cameras
from core.cadastros.models import Aluno


def home(request):
    alunos_list = Aluno.objects.all()

    content = {
        'alunos': alunos_list
    }

    return render(request, "home.html", content)


# Frontend
def frontend(request):
    return render(request, "frontend.html")

# Backend
@login_required(login_url="login")
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def backend(request):
    return render(request, "backend.html")