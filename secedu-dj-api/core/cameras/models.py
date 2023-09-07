from django.db import models
from core.cadastros.models import Escolas, Pessoas

class baseModel(models.Model):
    data_cadastro = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class NotaFiscal(baseModel):
    numero = models.CharField(max_length=100)
    data = models.DateTimeField()

    class Meta:
        verbose_name_plural = "Notas Fiscais"
        verbose_name = "Nota Fiscal"

    def __str__(self):
        return f"{self.numero} - {self.data}"

class Cameras(baseModel):
    nf = models.ForeignKey(NotaFiscal, on_delete=models.CASCADE)
    descricao = models.CharField(max_length=100)
    acesso = models.CharField(max_length=100)
    modelo = models.CharField(max_length=50)
    usuario = models.CharField(max_length=100)
    senha = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Câmeras"
        verbose_name = "Câmera"

    def __str__(self):
        return f"{self.descricao} - {self.acesso}"

class Locais(baseModel):
    ponto = models.ForeignKey(Escolas, on_delete=models.CASCADE)
    camera = models.ForeignKey(Cameras, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    descricao = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Locais"
        verbose_name = "Local"

    def __str__(self):
        return f"{self.nome} - {self.ponto} - {self.descricao} - {self.camera.descricao}"

class Frequencias(baseModel):
    pessoa = models.ForeignKey(Pessoas, on_delete=models.CASCADE)
    local = models.ForeignKey(Locais, on_delete=models.CASCADE)
    data = models.DateField()
    hora = models.TimeField()

    class Meta:
        verbose_name_plural = "Frequências"
        verbose_name = "Frequência"

    def __str__(self):
        return f"{self.pessoa.nome} - {self.local.nome} - {self.data} - {self.hora}"
