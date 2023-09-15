FROM nvcr.io/nvidia/tensorflow:23.08-tf2-py3

# environment variables
ENV PYTHONUNBUFFERED=1

WORKDIR /app

EXPOSE 8888

RUN mkdir /app/capturas/
RUN mkdir /app/dataset/
RUN mkdir /app/ftp/

RUN apt-get update

RUN apt-get install ffmpeg libsm6 libxext6 -y

COPY ./ /app/

RUN pip install -r requirements.txt

RUN pip install -e ./lib/

#CMD ["python", "consumer-extrair-faces-files.py" ]

CMD ["bash", "echo 'Serve Play!'"]
