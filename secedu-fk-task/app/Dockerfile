#base image
FROM python:3.8
LABEL org.opencontainers.image.source https://github.com/serengil/deepface
# -----------------------------------
# create required folder
RUN mkdir /app
RUN mkdir /app/deepface
EXPOSE 5000
# -----------------------------------
# Copy required files from repo into image
COPY ./deepface /app/deepface
COPY ./api/app.py /app/
COPY ./api/api.py /app/
COPY ./api/routes.py /app/
COPY ./api/service.py /app/
COPY ./requirements.txt /app/
#COPY ./setup.py /app/
COPY ./README.md /app/
# -----------------------------------
# switch to application directory
WORKDIR /app
# -----------------------------------
# update image os
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6 -y
# -----------------------------------
# if you will use gpu, then you should install tensorflow-gpu package
RUN pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host=files.pythonhosted.org tensorflow
# -----------------------------------
# install deepface from pypi release (might be out-of-the-date)
# RUN pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host=files.pythonhosted.org deepface
# -----------------------------------
# instalar o deepface a partir do código fonte (sempre atualizado)
RUN pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host=files.pythonhosted.org -r requirements.txt
# -----------------------------------
# alguns pacotes são opcionais no deepface. active se a sua tarefa depender de um deles.
# RUN pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host=files.pythonhosted.org cmake==3.24.1.1
# RUN pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host=files.pythonhosted.org dlib==19.20.0
# RUN pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host=files.pythonhosted.org lightgbm==2.3.1
# -----------------------------------
# environment variables
ENV PYTHONUNBUFFERED=1
# -----------------------------------
# run the app (re-configure port if necessary)

CMD ["gunicorn", "--workers=1", "--timeout=3600", "--bind=0.0.0.0:5000", "app:create_app()"]
