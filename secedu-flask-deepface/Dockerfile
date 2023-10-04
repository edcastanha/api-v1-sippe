#base image
#FROM python:3.10
#FROM tensorflow/build:2.11-python3.10
FROM tensorflow/tensorflow:latest-gpu

# create required folder
RUN mkdir /app
RUN mkdir /app/deepface
# -----------------------------------
# Copy required files from repo into image
COPY ./deepface /app/deepface
COPY ./app/api /app/
COPY ./requirements.txt /app/
COPY ./setup.py /app/
COPY ./README.md /app/
# -----------------------------------
# switch to application directory
WORKDIR /app
# -----------------------------------
# update image os
RUN apt-get update
 
RUN apt-get install ffmpeg libsm6 libxext6 -y
# -----------------------------------
#RUN pip install --upgrade setuptools pip wheel

RUN pip install --upgrade pip


# -----------------------------------
# if you will use gpu, then you should install tensorflow-gpu package
#RUN pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host=files.pythonhosted.org tensorflow[and-cuda]

# -----------------------------------
# instalar o deepface a partir do código fonte (sempre atualizado)
#RUN pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host=files.pythonhosted.org -r requirements.txt

# -----------------------------------
# install deepface from source code (always up-to-date)
RUN pip install -e .

# -----------------------------------
#RUN pip install --trusted-host pypi.org --trusted-host pypi.ngc.nvidia.com nvidia-pyindex
#RUN pip install --trusted-host pypi.org --trusted-host pypi.ngc.nvidia.com nvidia-cuda-runtime-cu12
#RUN pip install tensorflow[and-cuda]

# environment variables
ENV PYTHONUNBUFFERED=1

# -----------------------------------
# run the app (re-configure port if necessary)
EXPOSE 5000

CMD ["gunicorn", "--workers=1", "--timeout=3600", "--bind=0.0.0.0:5000", "app:create_app()"]


# docker run --gpus all -it --rm tensorflow/tensorflow:latest-gpu python -c "import tensorflow as tf; print(tf.__version__)"
# docker run --gpus all -it --rm tensorflow/tensorflow:latest-gpu python -c "import tensorflow as tf; print(tf.config.list_physical_devices('GPU'))"