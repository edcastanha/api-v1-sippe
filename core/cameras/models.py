from django.db import models

class baseModel(models.Model):
    data_cadastro = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Cameras(baseModel):
    descricao = models.CharField(max_length=100)
    ip = models.CharField(max_length=15)
    modelo = models.CharField(max_length=100)
    usuario = models.CharField(max_length=100)
    senha = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.descricao} - {self.ip}"

class Locais(baseModel):
    nome = models.CharField(max_length=100)
    descricao = models.CharField(max_length=100)
    camera = models.ForeignKey(Cameras, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nome} - {self.descricao} - {self.camera.descricao}"
