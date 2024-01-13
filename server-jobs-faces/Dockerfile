FROM tensorflow/tensorflow:latest-gpu

# environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# switch to application directory
WORKDIR /app

RUN mkdir -p /app/media/capturas && chmod -rx /app/media/capturas
RUN mkdir -p /app/media/dataset && chmod -rx /app/media/dataset
RUN mkdir -p /app/media/ftp && chmod -rx /app/media/ftp
RUN mkdir -p /app/media/logs && chmod -rx /app/media/logs

RUN mkdir -p /app/deepface/ && chmod -rx /app/deepface/

# -----------------------------------
COPY ./deepface/ /app/deepface/  
COPY ./requirements.txt /app/requirements.txt
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
RUN apt-get install libgl1-mesa-glx
RUN pip install async-timeout
RUN pip install deepface==0.0.79

# -----------------------------------

COPY . /app/
# install deepface from source code (always up-to-date)
#RUN pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host=files.pythonhosted.org -e .

#COPY ./consumer-extrair-faces-files.py /app/

#CMD ["python", "consumer-extrair-faces-files.py"]

