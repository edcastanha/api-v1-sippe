FROM nvcr.io/nvidia/tensorflow:23.08-tf2-py3
#FROM nvidia/cuda:11.6.2-base-ubuntu20.04
#FROM tensorflow/tensorflow:latest-gpu

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV NVIDIA_VISIBLE_DEVICES all
ENV NVIDIA_DRIVER_CAPABILITIES compute,utility

WORKDIR /app
EXPOSE 8888

COPY ./task/ /app/
COPY ./task/requirements.txt /app/requirements.txt
RUN apt-get update
RUN python -m pip install --upgrade pip
RUN apt-get install ffmpeg libsm6 libxext6 libgl1-mesa-glx -y

#RUN pip install cmake==3.24.1.1
#RUN pip install dlib==19.20.0
RUN pip install lightgbm==2.3.1
RUN pip install nvidia-cudnn-cu11==8.6.0.163
RUN pip install -e ./lib/
RUN pip install -r requirements.txt
#CMD ["python", "consumer-extrair-faces-files.py" ]
