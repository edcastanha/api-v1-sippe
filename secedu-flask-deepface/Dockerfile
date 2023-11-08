FROM tensorflow/tensorflow:latest-gpu

# environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# switch to application directory
WORKDIR /app

RUN mkdir -p /app/capturas && chmod -rx /app/capturas
RUN mkdir -p /app/dataset && chmod -rx /app/dataset
RUN mkdir -p /app/ftp && chmod -rx /app/ftp

# -----------------------------------
COPY ./app/api/deepface/ /app/deepface/
COPY ./app/api/ /app/
COPY ./app/api/requirements.txt /app/requirements.txt
# -----------------------------------
RUN rm -rf /usr/lib/python3/dist-packages/blinker*
RUN apt-get update
RUN pip install --upgrade setuptools pip wheel
RUN pip install --upgrade pip
RUN apt-get install ffmpeg libsm6 libxext6 -y
RUN apt-get install -y libcairo2-dev pkg-config python3-dev libgirepository1.0-dev
# -----------------------------------


RUN pip install  -r requirements.txt

# -----------------------------------
# install deepface from source code (always up-to-date)
#RUN pip install -e .

# -----------------------------------
RUN apt-get install libgl1-mesa-glx
RUN pip install async-timeout
RUN pip install deepface==0.0.79

EXPOSE 5000

CMD ["gunicorn", "--workers=1", "--timeout=3600", "--bind=0.0.0.0:5000", "app:create_app()"]