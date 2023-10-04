FROM python:3.11.4-alpine

WORKDIR /usr/src/app

# Impede o Python de escrever ficheiros pyc para o disco (equivalente à opção python -B)
ENV PYTHONDONTWRITEBYTECODE 1
# assegura que a saída Python é enviada diretamente para o terminal sem a colocar em buffer primeiro
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

COPY ./requirements.txt /usr/src/app/requirements.txt

RUN pip install -r requirements.txt

COPY ./entrypoint.sh /usr/src/app/entrypoint.sh

COPY . /usr/src/app/

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]