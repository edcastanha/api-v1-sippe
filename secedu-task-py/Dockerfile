FROM nvcr.io/nvidia/tensorflow:23.08-tf2-py3

ENV PYTHONUNBUFFERED=1

WORKDIR /app
EXPOSE 8888
COPY ./task/ /app/
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6 -y
RUN pip install cmake==3.24.1.1
RUN pip install dlib==19.20.0
RUN pip install lightgbm==2.3.1
RUN pip install -e ./lib/
RUN pip install -r requirements.txt
#CMD ["python", "consumer-extrair-faces-files.py" ]

CMD ["bash", "echo 'Serve Play!'"]
