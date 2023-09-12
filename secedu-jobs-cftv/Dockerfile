#base image
FROM python:3.10
# -----------------------------------
# switch to application directory
WORKDIR /app
# -----------------------------------
# create required folder
#RUN mkdir /app
# -----------------------------------
# Copy required files from repo into image

COPY ./ /app/

# -----------------------------------
# update image os
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6 -y
# -----------------------------------
# se vai usar gpu, então deve instalar o pacote tensorflow-gpu
RUN pip install tensorflow-gpu>2.11
#RUN pip install torch torchvision  --index-url https://download.pytorch.org/whl/cu118
# -----------------------------------
# instalar o deepface a partir do lançamento do pypi (pode estar desatualizado)
RUN pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host=files.pythonhosted.org retina-face
# -----------------------------------
#      Versão	        | versão Python   |	Compilador  |	ferramentas de construção |	cuDNN |	CUDA
# tensorflow_gpu-2.10.0	| 3.7-3.10        |	MSVC 2019   |	Bazel 5.1.1               |	8.1	  | 11.2
# install deepface from source code (always up-to-date)
#RUN pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host=files.pythonhosted.org -e .
# -----------------------------------
# alguns pacotes são opcionais no deepface. active se a sua tarefa depender de um deles.
 RUN pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host=files.pythonhosted.org cmake==3.24.1.1
 RUN pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host=files.pythonhosted.org dlib==19.20.0
 RUN pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host=files.pythonhosted.org lightgbm==2.3.1
# -----------------------------------
# environment variables
ENV PYTHONUNBUFFERED=1

# -----------------------------------
# run the app (re-configure port if necessary)
EXPOSE 5000

CMD ["python", "Publisher.py"]
