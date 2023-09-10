from django.shortcuts import render

from .models import Contratos


def index(request):
    latest_question_list = Contratos.objects.order_by("-pub_date")[:5]
    context = {"latest_question_list": latest_question_list}
    return render(request, "cadastros/index.html", context)
