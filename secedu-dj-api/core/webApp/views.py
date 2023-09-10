from django.shortcuts import render
from django.http import Http404

from core.cadastros.models import Contratos, Pessoas


def index(request):
    latest_contratos_list = Contratos.objects
    context = {"latest_contratos_list": latest_contratos_list}
    return render(request, "cadastros/index.html", context)


# ...
def detail(request, pessoa_id):
    try:
        queryObject = Pessoas.objects.get(pk=question_id)
    except Pessoas.DoesNotExist:
        raise Http404("Pessoas does not exist")
    return render(request, "cadastros/detail.html", {"pessoas": queryObject})
