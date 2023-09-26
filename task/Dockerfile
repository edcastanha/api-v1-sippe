FROM nvcr.io/nvidia/tensorflow:23.08-tf2-py3

# environment variables
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update

RUN apt-get install ffmpeg libsm6 libxext6 -y

COPY ./ /app/

RUN pip install -r requirements.txt

RUN pip install -e ./lib/

CMD ["python", "consumer-extrair-faces-files.py" ]