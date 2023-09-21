from django.db import models
from core.cadastros.models import Escolas, Aluno

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
        return f" {self.usuario} -  {self.senha} - {self.descricao} - {self.modelo} - {self.acesso}"

class Locais(baseModel):
    contrato = models.ForeignKey(Escolas, on_delete=models.CASCADE)
    camera = models.ForeignKey(Cameras, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    descricao = models.CharField(max_length=100)


    class Meta:
        verbose_name_plural = "Locais"
        verbose_name = "Local"

    def __str__(self):
        return f"{self.nome} - {self.contrato} - {self.descricao} - {self.camera.acesso}@{self.camera.usuario}:{self.camera.senha}"

class FrequenciasEscolar(baseModel):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE,  null=True)
    local = models.ForeignKey(Locais, on_delete=models.CASCADE)
    data = models.DateField()

    class Meta:
        verbose_name_plural = "Frequências Escolar"
        verbose_name = "Frequência Escolar"

    def __str__(self):
        return f"{self.aluno.pessoa.nome} - {self.local.nome} - {self.data} - {self.aluno.turma.nome}"
