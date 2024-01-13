import requests
import json
from datetime import datetime, timedelta
import re

# URL da API REST que fornece as informações
api_url = 'https://exemplo.com/api/cameras'

# Expressão regular para o padrão AAAA-MM-DD
date_pattern = re.compile(r'\d{4}-\d{2}-\d{2}')

# Função para converter uma data no formato AAAA-MM-DD para um objeto datetime
def parse_date(date_str):
    return datetime.strptime(date_str, '%Y-%m-%d')

# Função para verificar se a data atual é maior do que a data da última verificação
def is_current_date_greater(last_verification_date):
    current_date = datetime.now().date()
    return current_date > last_verification_date

# Função para verificar se o dia da semana é entre segunda-feira (0) e sexta-feira (4)
def is_weekday(date):
    return date.weekday() < 5  # 0 a 4 representam segunda a sexta-feira

def get_ftp_urls():
    try:
        response = requests.get(api_url)
        data = response.json()

        for item in data:
            date_capture = item.get('last_verification_date')

            if date_capture and date_pattern.match(date_capture):
                last_verification_date = parse_date(date_capture)

                if is_current_date_greater(last_verification_date) and is_weekday(datetime.now()):
                    ftp_url = item.get('ftp_url')
                    # Faça algo com a ftp_url, por exemplo, adicioná-la a uma lista ou processá-la de alguma forma.
                    print(f'FTP URL: {ftp_url}')
    except Exception as e:
        print(f'Erro ao consultar a API: {e}')

if __name__ == '__main__':
    get_ftp_urls()
