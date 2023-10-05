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

# Copy required files from repo into image
COPY ./app/api/deepface /app/deepface
COPY ./app/api/ /app/
COPY ./requirements.txt /app/
# -----------------------------------
# -----------------------------------
# update image os
#RUN apt-get update
 
#RUN apt-get install ffmpeg libsm6 libxext6 -y
# -----------------------------------
#RUN pip install --upgrade setuptools pip wheel

#RUN pip install --upgrade pip

# -----------------------------------
# instalar o deepface a partir do código fonte (sempre atualizado)
RUN pip install  -r requirements.txt

# -----------------------------------
# install deepface from source code (always up-to-date)
RUN pip install -e ./deepface/

# -----------------------------------
#RUN pip install --trusted-host pypi.org --trusted-host pypi.ngc.nvidia.com nvidia-pyindex
#RUN pip install --trusted-host pypi.org --trusted-host pypi.ngc.nvidia.com nvidia-cuda-runtime-cu12
#RUN pip install tensorflow[and-cuda]


EXPOSE 5000 8500 8501

CMD ["gunicorn", "--workers=1", "--timeout=3600", "--bind=0.0.0.0:5000", "app:create_app()"]

# -----------------------------------
# docker run --gpus all -it --rm tensorflow/tensorflow:latest-gpu python -c "import tensorflow as tf; print(tf.__version__)"
# docker run --gpus all -it --rm tensorflow/tensorflow:latest-gpu python -c "import tensorflow as tf; print(tf.config.list_physical_devices('GPU'))"