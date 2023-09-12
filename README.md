# Face Recognition SecEdu Project

## Anotacoes Importanetes
[image]:{}

### SOBRE CUDA - GPU

#      Versão	        | versão Python   |	Compilador  |	ferramentas de construção |	cuDNN |	CUDA
# tensorflow_gpu-2.10.0	| 3.7-3.10        |	MSVC 2019   |	Bazel 5.1.1               |	8.1	  | 11.2

Verificar se a GPU esta disponivel para o CUDA
'''
    nvidia-smi
'''
'''
    nvcc -V
'''

'''
    pip install torch torchvision  --index-url https://download.pytorch.org/whl/cu118
'''

Tambem tem o ''torchaudio'' e o ''torchtext''

### SOBRE O OPENCV

'''
    pip install opencv-python
'''

### SOBRE O DLIB

'''
    pip install dlib
'''

### SOBRE O FACE RECOGNITION

'''
    pip install face_recognition
'''

## Criando Virtual Env no Anaconda
conda create env --name ven1 python-3.XX

conda env list  ---> Lita todos ambientes 

conda activate env1  ------->>>>> nome do ambiente criar

conda list  ----->>>> Lista os pacotes do ambiente



conda create --name tensorflow-gpu python = 3.10

conda activate tensoflow-gpu

conda install -c conda-forge cudatoolkit=11.2 cudnn=8.1.0

pip install tensorflow==2.10

## Exporta requerimentos do projeto
conda env export > environment.yml


conda install -c conda-forge  ....

