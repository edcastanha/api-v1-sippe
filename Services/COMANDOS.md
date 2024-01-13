#Script para makemigrations e migrate do Django
# Autor: Edson Lourenço
# Data: 07/09/2023

# DJANGO COMAND

python manage.py startapp _NAME_ ./

python manage.py makemigrations --noinput 
python manage.py migrate --noinput 

python manage.py collectstatic --noinput 

## Criar app no Django
python manage.py start

gunicorn --workers=1 --timeout=3600 --bind=0.0.0.0:9000 core.wsgi

# COMANDO DE BACKUP LOAD de dados JSON::
python manage.py dumpdata cadastros > backup-models/cadastros/cadastros.json

python manage.py loaddata backup-models/cadastros/cadastros.json

## CAMERAS APP
python manage.py dumpdata cameras.NotaFiscal > backup-models/cameras/cameras_NotaFiscal.json
python manage.py dumpdata cameras.Cameras > backup-models/cameras/cameras_Cameras.json
python manage.py dumpdata cameras.Locais > backup-models/cameras/cameras_Locais.json
python manage.py dumpdata cameras.FrequenciasEscolar > backup-models/cameras/cameras_FrequenciasEscolar.json
python manage.py dumpdata cameras.Tarefas > backup-models/cameras/cameras_Tarefas.json
python manage.py dumpdata cameras.Processamentos > backup-models/cameras/cameras_Processamentos.json
## LOAD DATA::
python manage.py loaddata backup-models/cameras/cameras_NotaFiscal.json
python manage.py loaddata backup-models/cameras/cameras_Cameras.json
python manage.py loaddata backup-models/cameras/cameras_Locais.json
python manage.py loaddata backup-models/cameras/cameras_FrequenciasEscolar.json
python manage.py loaddata backup-models/cameras/cameras_Tarefas.json
python manage.py loaddata backup-models/cameras/cameras_Processamentos.json




# QUERYS:
select_related('nome do campo que recebe a ForeignKey):
(JOIN) Objetivo e realizar uma unica query de moduls relacionado


# Relacionamento Reverso:
prefetch_related('nome do related_name da relacao):
Ex: pessoas = Pessoas.objects.all()
for pessoa in pessoas:
    turma = pessoa.turma.all()


# COMMAND Celery:

### CELERY BACKUP E LOAD JSON
python manage.py dumpdata django_celery_results > backup-models/celery/django_celery_results.json
python manage.py dumpdata django_celery_beat > backup-models/celery/django_celery_beat.json

## Execute Scripts
python -m celery -A core worker -l info
celery -A core beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler

# Tensorflow-gpu-jupter:::
docker run -it --rm tensorflow/tensorflow:latest-gpu python -c "import tensorflow as tf; print(tf.reduce_sum(tf.random.normal([1000, 1000])))"
docker run -it --rm apiv1sippe:tf-deepface 
docker run -it --rm tensorflow/tensorflow:latest-gpu-jupyter python -c "import tensorflow as tf; print(tf.reduce_sum(tf.random.normal([1000, 1000])))"


