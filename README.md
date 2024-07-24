# PoC para testes de sistema distribuido para Visão Computacional

Autor: Edson Lourenço Bezerra Filho
email: edcastanha@gmail
Fortaleza / CE - Brasil


## Descrição
Criado sistema distribuido usando TensorFlow com suporte a GPU (CUDA) para realizar detecção e reconhecimento de faces em imagens, filas de mensageria e tarefas agendadas com a integração com Celery para tarefas assíncronas e o uso de Docker para facilitar a implantação.

## Requisitos do Sistema
- **CUDA-GPU Version**: 8.1
- **TensorFlow Version**: 2.10.0
- **Python Version**: 3.7-3.10
- **Compilador**: MSVC 2019
- **Ferramentas de Construção**: Bazel 5.1.1
- **cuDNN Version**: 11.2

## Configuração de Ambiente
Certifique-se de ter o ambiente configurado corretamente para aproveitar a aceleração da GPU.

## Instruções de Uso
1. Clone o repositório.
2. cd secedu-system-face-recognition/servies
3. Execute docker-compose up -d

## Uso de TensorFlow GPU com Docker
Para testar o ambiente TensorFlow GPU com Docker, execute o seguinte comando:

```bash
docker run --gpus all -it --rm tensorflow/tensorflow:latest-gpu python -c "import tensorflow as tf; print(tf.reduce_sum(tf.random.normal([1000, 1000])))"
```

Lembre-se de ajustar as configurações conforme necessário para o seu ambiente.

# Imformações entre em contato;
