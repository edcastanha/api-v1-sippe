# tasks.py
from celery import shared_task
import requests
core.loggingMe import logger

@shared_task(name="make_api_dataset")
def make_api_dataset():
    # Realize a chamada à API
    api_url = "http://localhost:5000/dataset"
    try:
        response = requests.post(api_url, data={'action': 'delete', 'photo_id': photo_id})
        logger.debug(f'Resposta da API: {response}')
    except requests.exceptions.RequestException as e:
        # Tratar erros de solicitação
        logger.error(f'Erro de solicitação: {e}')
