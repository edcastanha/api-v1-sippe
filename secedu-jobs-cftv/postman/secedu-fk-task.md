# deepface

<div align="center">


</div>

O Deepface é um produto leve [face recognition](https://sefiks.com/2018/08/06/deep-face-recognition-with-keras/) e análise de atributos faciais ([age](https://sefiks.com/2019/02/13/apparent-age-and-gender-prediction-in-keras/), [gender](https://sefiks.com/2019/02/13/apparent-age-and-gender-prediction-in-keras/), [emotion](https://sefiks.com/2018/01/01/facial-expression-recognition-with-keras/) and [race](https://sefiks.com/2019/11/11/race-and-ethnicity-prediction-in-keras/)) para python. Trata-se de uma estrutura híbrida de reconhecimento facial que envolve modelos do **estado da arte**:
* [`VGG-Face`](https://sefiks.com/2018/08/06/deep-face-recognition-with-keras/)
* [`Google FaceNet`](https://sefiks.com/2018/09/03/face-recognition-with-facenet-in-keras/)
* [`OpenFace`](https://sefiks.com/2019/07/21/face-recognition-with-openface-in-keras/)
* [`Facebook DeepFace`](https://sefiks.com/2020/02/17/face-recognition-with-facebook-deepface-in-keras/)
* [`DeepID`](https://sefiks.com/2020/06/16/face-recognition-with-deepid-in-keras/)
* [`ArcFace`](https://sefiks.com/2020/12/14/deep-face-recognition-with-arcface-in-keras-and-python/)
* [`Dlib`](https://sefiks.com/2020/07/11/face-recognition-with-dlib-in-python/) 
* `SFace`.

As experiências mostram que os seres humanos têm uma exatidão de 97,53% nas tarefas de reconhecimento facial, enquanto estes modelos já atingiram e ultrapassaram esse nível de exatidão.

## Installation [![PyPI](https://img.shields.io/pypi/v/deepface.svg)](https://pypi.org/project/deepface/) [![Conda](https://img.shields.io/conda/vn/conda-forge/deepface.svg)](https://anaconda.org/conda-forge/deepface)

O método mais fácil de instalar deepface é descarregá-lo a partir de [`PyPI`](https://pypi.org/project/deepface/). Vai instalar a própria biblioteca e os seus pré-requisitos também.

```shell
$ pip install deepface
```

Em segundo lugar, o DeepFace também está disponível em [`Conda`](https://anaconda.org/conda-forge/deepface). Em alternativa, pode instalar o pacote através do conda.

```shell
$ conda install -c conda-forge deepface
```

Em terceiro lugar, pode instalar o deepface a partir do seu código fonte.

```shell
$ git clone https://github.com/serengil/deepface.git
$ cd deepface
$ pip install -e .
```

Em seguida, poderá importar a biblioteca e utilizar as suas funcionalidades.

```python
from deepface import DeepFace
```

**Facial Recognition** - [`Demo`](https://youtu.be/WnUVYQP4h44)

Um moderno [**Pipeline de reconhecimento facial**](https://sefiks.com/2020/05/01/a-gentle-introduction-to-face-recognition-in-deep-learning/) consiste em 5 fases comuns: 
* [detect](https://sefiks.com/2020/08/25/deep-face-detection-with-opencv-in-python/), 
* [align](https://sefiks.com/2020/02/23/face-alignment-for-face-recognition-in-python-within-opencv/), 
* [normalize](https://sefiks.com/2020/11/20/facial-landmarks-for-face-recognition-with-dlib/), 
* [represent](https://sefiks.com/2018/08/06/deep-face-recognition-with-keras/)
* [verify](https://sefiks.com/2020/05/22/fine-tuning-the-threshold-in-face-recognition/). 

Embora o Deepface trate de todas estas fases comuns em segundo plano, não é necessário adquirir conhecimentos aprofundados sobre todos os processos que lhe estão subjacentes. Pode simplesmente chamar a sua função de verificação, localização ou análise com uma única linha de código.

**Face Verification** - [`Demo`](https://youtu.be/KRCvkNCOphE)

Esta função verifica se os pares de rostos são da mesma pessoa ou de pessoas diferentes. Ela espera caminhos exatos de imagens como entrada. Passar imagens codificadas em numpy ou base64 também é bem-vindo. Depois, vai devolver um dicionário e deve verificar apenas a sua chave verificada.

```python
result = DeepFace.verify(img1_path = "img1.jpg", img2_path = "img2.jpg")
```

<p align="center"><img src="https://raw.githubusercontent.com/serengil/deepface/master/icon/stock-1.jpg" width="95%" height="95%"></p>

A função de verificação também pode lidar com muitas faces nos pares de faces. Neste caso, serão comparadas as faces mais semelhantes.

<p align="center"><img src="https://raw.githubusercontent.com/serengil/deepface/master/icon/verify-many-faces.jpg" width="95%" height="95%"></p>

**Face recognition** - [`Demo`](https://youtu.be/Hrjp-EStM_s)

[Face recognition](https://sefiks.com/2020/05/25/large-scale-face-recognition-for-deep-learning/) requer a aplicação da verificação da face muitas vezes. Neste caso, o deepface tem uma função find pronta a usar para lidar com esta ação. Vai procurar a identidade da imagem de entrada no caminho da base de dados e devolverá uma lista de quadros de dados pandas como saída. Entretanto, os embeddings faciais da base de dados faciais são armazenados num ficheiro pickle para serem pesquisados mais rapidamente na próxima vez. O resultado será o tamanho dos rostos que aparecem na imagem de origem. Além disso, as imagens de destino na base de dados também podem ter muitos rostos.


```python
dfs = DeepFace.find(img_path = "img1.jpg", db_path = "C:/workspace/my_db")
```

<p align="center"><img src="https://raw.githubusercontent.com/serengil/deepface/master/icon/stock-6-v2.jpg" width="95%" height="95%"></p>

**Embeddings**

Os modelos de reconhecimento facial representam basicamente as imagens faciais como vectores multidimensionais. Por vezes, é necessário utilizar esses vectores de incorporação diretamente. O DeepFace vem com uma função de representação dedicada. A função Representar devolve uma lista de incorporação. O resultado será o tamanho dos rostos que aparecem no caminho da imagem.

```python
embedding_objs = DeepFace.represent(img_path = "img.jpg")
```

Esta função devolve uma matriz como incorporação. O tamanho da matriz de incorporação seria diferente com base no nome do modelo. Por exemplo, VGG-Face é o modelo predefinido e representa imagens faciais como 2622 vectores dimensionais.

```python
embedding = embedding_objs[0]["embedding"]
assert isinstance(embedding, list)
assert model_name = "VGG-Face" and len(embedding) == 2622
```

Aqui, a incorporação também é [plotted](https://sefiks.com/2020/05/01/a-gentle-introduction-to-face-recognition-in-deep-learning/) com 2622 ranhuras na horizontal. Cada ranhura corresponde a um valor de dimensão no vetor de incorporação e o valor da dimensão é explicado na barra de cores à direita. À semelhança dos códigos de barras 2D, a dimensão vertical não armazena qualquer informação na ilustração.

<p align="center"><img src="https://raw.githubusercontent.com/serengil/deepface/master/icon/embedding.jpg" width="95%" height="95%"></p>

**Face recognition models** - [`Demo`](https://youtu.be/i_MOwvhbLdI)

Deepface é um pacote **híbrido** de reconhecimento facial. Atualmente, inclui muitos modelos de reconhecimento facial do **estado da arte**: 
* [`VGG-Face`](https://sefiks.com/2018/08/06/deep-face-recognition-with-keras/)
* [`Google FaceNet`](https://sefiks.com/2018/09/03/face-recognition-with-facenet-in-keras/)
* [`OpenFace`](https://sefiks.com/2019/07/21/face-recognition-with-openface-in-keras/)
* [`Facebook DeepFace`](https://sefiks.com/2020/02/17/face-recognition-with-facebook-deepface-in-keras/)
* [`DeepID`](https://sefiks.com/2020/06/16/face-recognition-with-deepid-in-keras/)
* [`ArcFace`](https://sefiks.com/2020/12/14/deep-face-recognition-with-arcface-in-keras-and-python/)
* [`Dlib`](https://sefiks.com/2020/07/11/face-recognition-with-dlib-in-python/)
* `SFace`. A configuração predefinida utiliza o modelo VGG-Face.

```python
models = [
  "VGG-Face", 
  "Facenet", 
  "Facenet512", 
  "OpenFace", 
  "DeepFace", 
  "DeepID", 
  "ArcFace", 
  "Dlib", 
  "SFace",
]

#face verification
result = DeepFace.verify(img1_path = "img1.jpg", 
      img2_path = "img2.jpg", 
      model_name = models[0]
)

#face recognition
dfs = DeepFace.find(img_path = "img1.jpg",
      db_path = "C:/workspace/my_db", 
      model_name = models[1]
)

#embeddings
embedding_objs = DeepFace.represent(img_path = "img.jpg", 
      model_name = models[2]
)
```

<p align="center"><img src="https://raw.githubusercontent.com/serengil/deepface/master/icon/model-portfolio-v8.jpg" width="95%" height="95%"></p>

FaceNet, VGG-Face, ArcFace e Dlib are [overperforming](https://youtu.be/i_MOwvhbLdI) modelos baseados em experiências. Pode encontrar as pontuações desses modelos abaixo em ambos [Labeled Faces in the Wild](https://sefiks.com/2020/08/27/labeled-faces-in-the-wild-for-face-recognition/) e os conjuntos de dados do YouTube Faces in the Wild declarados pelos seus criadores.

| Model | LFW Score | YTF Score |
| ---   | --- | --- |
| Facenet512 | 99.65% | - |
| SFace | 99.60% | - |
| ArcFace | 99.41% | - |
| Dlib | 99.38 % | - |
| Facenet | 99.20% | - |
| VGG-Face | 98.78% | 97.40% |
| *Human-beings* | *97.53%* | - |
| OpenFace | 93.80% | - |
| DeepID | - | 97.05% |

**Similarity**

Face recognition models são regulares [convolutional neural networks](https://sefiks.com/2018/03/23/convolutional-autoencoder-clustering-images-with-neural-networks/) e são responsáveis por representar as faces como vectores. Esperamos que um par de faces da mesma pessoa seja [more similar](https://sefiks.com/2020/05/22/fine-tuning-the-threshold-in-face-recognition/) do que um par de rostos de pessoas diferentes.

A semelhança pode ser calculada através de diferentes métricas, tais como [Cosine Similarity](https://sefiks.com/2018/08/13/cosine-similarity-in-machine-learning/), Distância Euclidiana e forma L2. A configuração predefinida utiliza a semelhança de cosseno.

```python
metrics = ["cosine", "euclidean", "euclidean_l2"]

#face verification
result = DeepFace.verify(img1_path = "img1.jpg", 
          img2_path = "img2.jpg", 
          distance_metric = metrics[1]
)

#face recognition
dfs = DeepFace.find(img_path = "img1.jpg", 
          db_path = "C:/workspace/my_db", 
          distance_metric = metrics[2]
)
```

Euclidean L2 forma [seems](https://youtu.be/i_MOwvhbLdI) mais estável do que o cosseno e a distância euclidiana regular com base em experiências.

**Facial Attribute Analysis** - [`Demo`](https://youtu.be/GT2UeN85BdA)

Deepface inclui também um módulo de análise de atributos faciais que inclui:
* [`age`](https://sefiks.com/2019/02/13/apparent-age-and-gender-prediction-in-keras/)
* [`gender`](https://sefiks.com/2019/02/13/apparent-age-and-gender-prediction-in-keras/)
* [`facial expression`](https://sefiks.com/2018/01/01/facial-expression-recognition-with-keras/) 
(including angry, fear, neutral, sad, disgust, happy and surprise)
* [`race`](https://sefiks.com/2019/11/11/race-and-ethnicity-prediction-in-keras/) 
(including asian, white, middle eastern, indian, latino and black) predictions.
 O resultado será o tamanho dos rostos que aparecem na imagem de origem.

```python
objs = DeepFace.analyze(img_path = "img4.jpg", 
        actions = ['age', 'gender', 'race', 'emotion']
)
```

<p align="center"><img src="https://raw.githubusercontent.com/serengil/deepface/master/icon/stock-2.jpg" width="95%" height="95%"></p>

O modelo relativo à idade obteve ± 4,65 MAE; o modelo relativo ao género obteve 97,44% de exatidão, 96,29% de precisão e 95,05% de recuperação, tal como mencionado no seu [tutorial](https://sefiks.com/2019/02/13/apparent-age-and-gender-prediction-in-keras/).


**Face Detectors** - [`Demo`](https://youtu.be/GZ2p2hj2H5k)

A deteção e o alinhamento de rostos são fases iniciais importantes de uma cadeia de reconhecimento de rostos moderna. As experiências mostram que o simples alinhamento aumenta a precisão do reconhecimento facial em quase 1%. 
* [`OpenCV`](https://sefiks.com/2020/02/23/face-alignment-for-face-recognition-in-python-within-opencv/)
* [`SSD`](https://sefiks.com/2020/08/25/deep-face-detection-with-opencv-in-python/)
* [`Dlib`](https://sefiks.com/2020/07/11/face-recognition-with-dlib-in-python/)
* [`MTCNN`](https://sefiks.com/2020/09/09/deep-face-detection-with-mtcnn-in-python/)
* [`RetinaFace`](https://sefiks.com/2021/04/27/deep-face-detection-with-retinaface-in-python/)
* [`MediaPipe`](https://sefiks.com/2022/01/14/deep-face-detection-with-mediapipe/)
* [`YOLOv8 Face`](https://github.com/derronqi/yolov8-face)
* [`YuNet`](https://github.com/ShiqiYu/libfacedetection) 
os detectores estão envolvidos em deepface.

<p align="center"><img src="https://raw.githubusercontent.com/serengil/deepface/master/icon/detector-portfolio-v5.jpg" width="95%" height="95%"></p>

Todas as funções deepface aceitam um argumento opcional de entrada do backend do detetor. É possível alternar entre esses detectores com esse argumento. 
OpenCV é o detetor padrão.

```python
backends = [
  'opencv', 
  'ssd', 
  'dlib', 
  'mtcnn', 
  'retinaface', 
  'mediapipe',
  'yolov8',
  'yunet',
]

#face verification
obj = DeepFace.verify(img1_path = "img1.jpg", 
        img2_path = "img2.jpg", 
        detector_backend = backends[0]
)

#face recognition
dfs = DeepFace.find(img_path = "img.jpg", 
        db_path = "my_db", 
        detector_backend = backends[1]
)

#embeddings
embedding_objs = DeepFace.represent(img_path = "img.jpg", 
        detector_backend = backends[2]
)

#facial analysis
demographies = DeepFace.analyze(img_path = "img4.jpg", 
        detector_backend = backends[3]
)

#face detection and alignment
face_objs = DeepFace.extract_faces(img_path = "img.jpg", 
        target_size = (224, 224), 
        detector_backend = backends[4]
)
```

Os modelos de reconhecimento facial são, na verdade, modelos CNN e esperam entradas de tamanho padrão. 
Assim, o redimensionamento é necessário antes da representação. Para evitar a deformação, o deepface adiciona pixéis pretos de preenchimento de acordo com o argumento do tamanho alvo após a deteção e o alinhamento.

<p align="center"><img src="https://raw.githubusercontent.com/serengil/deepface/master/icon/deepface-detectors-v3.jpg" width="90%" height="90%"></p>

[RetinaFace](https://sefiks.com/2021/04/27/deep-face-detection-with-retinaface-in-python/) e [MTCNN](https://sefiks.com/2020/09/09/deep-face-detection-with-mtcnn-in-python/) parecem ter um desempenho superior nas fases de deteção e alinhamento, mas são muito mais lentos. Se a velocidade do seu pipeline for mais importante, então deve utilizar o opencv ou o ssd. Por outro lado, se considerar a precisão, deve utilizar o retinaface ou o mtcnn.

O desempenho do RetinaFace é muito satisfatório, mesmo no meio da multidão, como se pode ver na ilustração seguinte. 
Além disso, apresenta um desempenho incrível na deteção de pontos de referência faciais. Os pontos vermelhos realçados mostram alguns pontos de referência faciais, como os olhos, o nariz e a boca. Por isso, a pontuação de alinhamento do RetinaFace também é elevada.

<p align="center"><img src="https://raw.githubusercontent.com/serengil/deepface/master/icon/retinaface-results.jpeg" width="90%" height="90%">
<br><em>Os Anjos Amarelos - Fenerbahçe Vôlei feminino</em>
</p>

Pode obter mais informações sobre o RetinaFace nesta [repo](https://github.com/serengil/retinaface).

**Real Time Analysis** - [`Demo`](https://youtu.be/-c9sSJcx6wI)

Também é possível executar o deepface para vídeos em tempo real. A função Stream acede à webcam e aplica o reconhecimento facial e a análise de atributos faciais. A função começa a analisar um fotograma se conseguir focar um rosto sequencialmente em 5 fotogramas. Depois, mostra os resultados em 5 segundos.

```python
DeepFace.stream(db_path = "C:/localhost/database")
```

<p align="center"><img src="https://raw.githubusercontent.com/serengil/deepface/master/icon/stock-3.jpg" width="90%" height="90%"></p>

Embora o reconhecimento facial se baseie na aprendizagem de uma imagem, também pode utilizar várias imagens de rosto de uma pessoa. Deve reorganizar a sua estrutura de directórios como ilustrado abaixo.

```bash
user
├── database
│   ├── Alice
│   │   ├── Alice1.jpg
│   │   ├── Alice2.jpg
│   ├── Bob
│   │   ├── Bob.jpg
```

**API** - [`Demo`](https://youtu.be/HeKCQ6U9XmI)

O DeepFace também serve uma API. Pode clonar [`/api`](https://github.com/serengil/deepface/tree/master/api) e executar a api através de gunicorn servidor. Isto irá ativar um serviço de repouso. Desta forma, pode chamar o deepface a partir de um sistema externo, como uma aplicação móvel ou web.
        
```shell
cd scripts
./service.sh
```

<p align="center"><img src="https://raw.githubusercontent.com/serengil/deepface/master/icon/deepface-api.jpg" width="90%" height="90%"></p>

As funções de reconhecimento facial, análise de atributos faciais e representação vetorial são abrangidas pela API. Espera-se que chame estas funções como métodos http post.
 Os pontos de extremidade de serviço predefinidos serão `http://localhost:5000/verify` para reconhecimento facial, `http://localhost:5000/analyze` para análise de atributos faciais, e `http://localhost:5000/represent` para representação vetorial. Pode passar imagens de entrada como caminhos de imagem exactos no seu ambiente, cadeias de caracteres codificadas em base64 ou imagens na Web. [Here](https://github.com/serengil/deepface/tree/master/api), pode encontrar um projeto postman para saber como estes métodos devem ser chamados.

**Dockerized Service**

Você pode implantar a API do deepface em um cluster kubernetes com o docker. O seguinte [shell script](https://github.com/serengil/deepface/blob/master/scripts/dockerize.sh) servirá o deepface em `localhost:5000`. É necessário reconfigurar o [Dockerfile](https://github.com/serengil/deepface/blob/master/Dockerfile) se você quiser mudar a porta. Então, mesmo que você não tenha um ambiente de desenvolvimento, você poderá consumir serviços do deepface como verify e analyze. Você também pode acessar o interior da imagem do docker para executar comandos relacionados ao deepface. Por favor, siga as instruções na página [shell script](https://github.com/serengil/deepface/blob/master/scripts/dockerize.sh).

```shell
cd scripts
./dockerize.sh
```

<p align="center"><img src="https://raw.githubusercontent.com/serengil/deepface/master/icon/deepface-dockerized-v2.jpg" width="50%" height="50%"></p>

**Command Line Interface**

O DeepFace também dispõe de uma interface de linha de comandos. É possível aceder às suas funções na linha de comandos, como se mostra abaixo. O comando deepface espera o nome da função como primeiro argumento e os argumentos da função em seguida.

```shell
#face verification
$ deepface verify -img1_path tests/dataset/img1.jpg -img2_path tests/dataset/img2.jpg

#facial analysis
$ deepface analyze -img_path tests/dataset/img1.jpg
```

Você também pode executar esses comandos se estiver executando o deepface com o docker. Por favor, siga as instruções no [shell script](https://github.com/serengil/deepface/blob/master/scripts/dockerize.sh#L17).

## Contribution [![Tests](https://github.com/serengil/deepface/actions/workflows/tests.yml/badge.svg)](https://github.com/serengil/deepface/actions/workflows/tests.yml)

Pedidos de pull são mais do que bem-vindos! Você deve executar os testes unitários localmente, executando [`test/unit_tests.py`](https://github.com/serengil/deepface/blob/master/tests/unit_tests.py) antes de criar um PR. Assim que um PR for enviado, o fluxo de trabalho de teste do GitHub será executado automaticamente e os resultados do teste unitário estarão disponíveis em [GitHub actions](https://github.com/serengil/deepface/actions) antes da aprovação. Além disso, o fluxo de trabalho também avaliará o código com o pylint.

## Support

There are many ways to support a project - starring⭐️ the GitHub repo is just one 🙏

You can also support this work on [Patreon](https://www.patreon.com/serengil?repo=deepface) or [GitHub Sponsors](https://github.com/sponsors/serengil).

<a href="https://www.patreon.com/serengil?repo=deepface">
<img src="https://raw.githubusercontent.com/serengil/deepface/master/icon/patreon.png" width="30%" height="30%">
</a>

## Citation

Por favor, cite a deepface nas suas publicações, se isso ajudar a sua investigação. Aqui estão as suas entradas no BibTex:

Se utilizar o deepface para fins de reconhecimento facial, por favor cite esta publicação.


 Se utilizar o deepface para fins de análise de atributos faciais, como a previsão de idade, sexo, emoção ou etnia, ou para fins de deteção facial, cite esta publicação.

Além disso, se você usa o deepface em seus projetos do GitHub, por favor adicione `deepface` no `requirements.txt`.

## Licence

Deepface está licenciado sob a Licença MIT - veja [`LICENSE`](https://github.com/serengil/deepface/blob/master/LICENSE) para mais pormenores. No entanto, a biblioteca inclui alguns modelos externos de reconhecimento facial:
 [VGG-Face](http://www.robots.ox.ac.uk/~vgg/software/vgg_face/)
 [Facenet](https://github.com/davidsandberg/facenet/blob/master/LICENSE.md)
 [OpenFace](https://github.com/iwantooxxoox/Keras-OpenFace/blob/master/LICENSE)
 [DeepFace](https://github.com/swghosh/DeepFace)
 [DeepID](https://github.com/Ruoyiran/DeepID/blob/master/LICENSE.md)
 [ArcFace](https://github.com/leondgarse/Keras_insightface/blob/master/LICENSE)
 [Dlib](https://github.com/davisking/dlib/blob/master/dlib/LICENSE.txt)
 [SFace](https://github.com/opencv/opencv_zoo/blob/master/models/face_recognition_sface/LICENSE).
  Além disso, os modelos de idade, género e raça/etnia são baseados no VGG-Face. Os tipos de licença serão herdados se utilizar esses modelos. Para efeitos de produção, verifique os tipos de licença desses modelos.

Deepface [logo](https://thenounproject.com/term/face-recognition/2965879/) is created by [Adrien Coquet](https://thenounproject.com/coquet_adrien/) e está licenciado sob [Creative Commons: By Attribution 3.0 License](https://creativecommons.org/licenses/by/3.0/).
