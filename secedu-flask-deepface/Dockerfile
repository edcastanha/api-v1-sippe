#base image
#FROM python:3.10
#FROM tensorflow/build:2.11-python3.10
# FROM tensorflow/serving:2.13.1-gpu
FROM tensorflow/tensorflow:latest-gpu

# environment variables
ENV PYTHONUNBUFFERED=1

ENV PYTHONDONTWRITEBYTECODE=1

# switch to application directory
WORKDIR /app
# -----------------------------------
# Copy required files from repo into image

COPY ./app/api/deepface/ /app/deepface/
COPY ./app/api/ /app/
COPY ./app/api/requirements.txt /app/requirements.txt

# -----------------------------------
# update image os
RUN rm -rf /usr/lib/python3/dist-packages/blinker*

RUN apt-get update
 
RUN pip install --upgrade setuptools pip wheel

RUN pip install --upgrade pip

RUN apt-get install ffmpeg libsm6 libxext6 -y
#RUN apt-get install --fix-missing libsm6 -y
#RUN apt-get install --fix-missing libxext6 -y
#RUN apt-get install --fix-missing ffmpeg  -y
# -----------------------------------

RUN apt-get install -y libcairo2-dev pkg-config python3-dev libgirepository1.0-dev


# -----------------------------------
# instalar o deepface a partir do código fonte (sempre atualizado)
RUN pip install  -r requirements.txt

# -----------------------------------
# install deepface from source code (always up-to-date)
#RUN pip install -e .

# -----------------------------------
#RUN pip install --trusted-host pypi.org --trusted-host pypi.ngc.nvidia.com nvidia-pyindex
#RUN pip install --trusted-host pypi.org --trusted-host pypi.ngc.nvidia.com nvidia-cuda-runtime-cu12
#RUN pip install tensorflow[and-cuda]

RUN apt-get install libgl1-mesa-glx
RUN pip install async-timeout

RUN pip install mediapipe==0.9.*


EXPOSE 5000

CMD ["gunicorn", "--workers=1", "--timeout=3600", "--bind=0.0.0.0:5000", "app:create_app()"]

# -----------------------------------
# docker run --gpus all -it --rm tensorflow/tensorflow:latest-gpu python -c "import tensorflow as tf; print(tf.__version__)"
# docker run --gpus all -it --rm tensorflow/tensorflow:latest-gpu python -c "import tensorflow as tf; print(tf.config.list_physical_devices('GPU'))"