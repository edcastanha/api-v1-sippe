from __future__ import absolute_import, unicode_literals
from celery import shared_task
from core.cadastros.models import Aluno
from core.loggingMe import logger

@shared_task
def exibi_matriculas_aluno():
    estudantes = Aluno.objects.all()
    for estudante in estudantes:
        logger('django').info(estudante.matricula)