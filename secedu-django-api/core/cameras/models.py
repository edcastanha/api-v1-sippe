from django.db import models
from core.cadastros.models import Escolas, Aluno, Escalas

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
    status = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Câmeras"
        verbose_name = "Câmera"

    def __str__(self):
        return f"EM:{self.data_cadastro} - {self.descricao} - {self.modelo} - {self.status}"

class Locais(baseModel):
    ponto = models.ForeignKey(Escolas, on_delete=models.CASCADE)
    camera = models.ForeignKey(Cameras, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    descricao = models.CharField(max_length=100)


    class Meta:
        verbose_name_plural = "Locais"
        verbose_name = "Local"

    def __str__(self):
        return f"{self.nome} - {self.ponto} - {self.descricao} - {self.camera.acesso}"

class FrequenciasEscolar(baseModel):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE,  null=True)
    camera = models.ForeignKey(Cameras, on_delete=models.CASCADE, null=True)
    data = models.DateField()

    class Meta:
        verbose_name_plural = "Frequências Escolar"
        verbose_name = "Frequência Escolar"

    def __str__(self):
        return f"{self.aluno.pessoa.nome} - {self.camera.descricao} - {self.data} - {self.aluno.turma.nome}"

class Tarefas(baseModel):

    CHOICE_STATUS = (
        ('Pendente', 'Pendente'),
        ('Cancelado', 'Cancelado'),
        ('Erro', 'Erro'),
        ('Finalizado', 'Finalizado'),
    )
    descricao = models.CharField(max_length=100)
    escalas = models.ForeignKey(Escalas, on_delete=models.CASCADE)
    cameras = models.ForeignKey(Cameras, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=CHOICE_STATUS, default='Pendente')

    class Meta:
        verbose_name_plural = "Tarefas"
        verbose_name = "Tarefa"
        ordering = ['id']

    def __str__(self):
        return f"{self.descricao} - {self.escalas.horario_inicio}::{self.escalas.horario_fim} - {self.status} - {self.data_atualizacao}"
    
class Processamentos(baseModel):
    CHOICE_STATUS = (
        ('Criado', 'Criado'),
        ('Cancelado', 'Cancelado'),
        ('Pendente', 'Pendente'),
        ('Erro', 'Erro'),
        ('Processado', 'Processado'),
    )
    camera = models.ForeignKey(Cameras, on_delete=models.CASCADE)
    dia = models.CharField(max_length=10)
    horario = models.CharField(null=True, blank=True, max_length=10)
    path = models.CharField(max_length=250, unique=True)
    status = models.CharField(max_length=20, choices=CHOICE_STATUS, default='Criado')
    retry = models.IntegerField(default=0)


    class Meta:
        verbose_name_plural = "Processamentos"
        verbose_name = "Processamento"
        ordering = ['id']
    
    def __str__(self):
        return f"{self.camera.descricao} - {self.dia} as {self.horario} - {self.path}"

class Faces(baseModel):
    processamento = models.ForeignKey(Processamentos, on_delete=models.CASCADE)
    path = models.CharField(max_length=250, unique=True)
    retry = models.IntegerField(default=0)
    backend_detector = models.CharField(max_length=20, default='mtcnn')
    model_detector = models.CharField(max_length=20, default='hog')
    auditado = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Faces Detectadas"
        verbose_name = "Face Detectada"
        ordering = ['id']
    
    def __str__(self):
        return f"{self.processamento.camera.descricao} - {self.processamento.dia} as {self.processamento.horario} - {self.path} - {self.status}"