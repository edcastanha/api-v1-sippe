# SecEdu - SIPPE

### SOBRE CUDA - GPU

#      Versão	        | versão Python   |	Compilador  |	ferramentas de construção |	cuDNN |	CUDA
# tensorflow_gpu-2.10.0	| 3.7-3.10        |	MSVC 2019   |	Bazel 5.1.1               |	8.1	  | 11.2

# Escolha o número de réplicas conforme necessário


## Relacionamento Reverso:
prefetch_related('nome do related_name da relacao):

Ex: pessoas = Pessoas.objects.all()
for pessoa in pessoas:
    turma = pessoa.turma.all()


## COMMAND Celery:
python -m celery -A core worker -l info

celery -A core beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler

## Tensorflow-gpu-jupter:::
docker run -it --rm tensorflow/tensorflow:latest-gpu-jupyter python -c "import tensorflow as tf; print(tf.reduce_sum(tf.random.normal([1000, 1000])))"

  


# DOCKER TensorFlow

docker pull tensorflow/tensorflow:devel-gpu
docker pull tensorflow/tensorflow:latest-gpu

## TEST de Docker

docker run --gpus all -it --rm tensorflow/tensorflow:latest-gpu python -c "import tensorflow as tf; print(tf.reduce_sum(tf.random.normal([1000, 1000])))"
docker run --runtime=nvidia -it --rm tensorflow/tensorflow:latest-gpu python -c "import tensorflow as tf; print(tf.reduce_sum(tf.random.normal([1000, 1000])))"




