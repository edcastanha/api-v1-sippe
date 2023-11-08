from django.db import models
from core.cadastros.models import Escolas, Aluno, Escalas, Pessoas

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
    
    def get_data(self):
        return {
            'id': self.id,
            'descricao': self.descricao,
            'acesso': self.acesso,
            'modelo': self.modelo,
            'status': self.status,
        }

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
    
    def get_data(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'ponto': self.ponto.nome,
            'descricao': self.descricao,
            'camera': self.camera.modelo,
        }

    def __str__(self):
        return f"{self.nome} - {self.ponto} - {self.descricao} - {self.camera.acesso}"

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
        ('Processado', 'Processado'),
        ('Error', 'Error'),
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
        ordering = ['status',]
    
    def __str__(self):
        return f"{self.status} | {self.camera.modelo} - {self.dia} as {self.horario}"
    
    def get_data(self):
        return {
            'camera': self.camera.modelo,
            'dia': self.dia,
            'horario': self.horario,
            'path': self.path,
            'status': self.status,
        } 

class Faces(baseModel):
    CHOICE_STATUS = (
        ('Criado', 'Criado'),
        ('Processado', 'Processado'),
        ('Error', 'Error'),
    )
    processamento = models.ForeignKey(Processamentos, on_delete=models.CASCADE)
    path_face = models.CharField(max_length=250, unique=True)
    backend_detector = models.CharField(max_length=20, default='retinaface')
    auditado = models.BooleanField(default=False)
    status = models.CharField(choices=CHOICE_STATUS, max_length=20, default='Criado', null=True, blank=True)

    class Meta:
        verbose_name_plural = "Faces Detectadas"
        verbose_name = "Face Detectada"
        ordering = ['status', 'auditado',]
    
    def __str__(self):
        return f"{self.status} :: {self.processamento.dia} as {self.processamento.horario} - {self.auditado}"

class FrequenciasEscolar(baseModel):
    pessoa = models.ForeignKey(Pessoas, on_delete=models.CASCADE,  null=True)
    camera = models.ForeignKey(Cameras, on_delete=models.CASCADE, null=True)
    data = models.DateField()

    class Meta:
        verbose_name_plural = "Frequências Escolar"
        verbose_name = "Frequência Escolar"

    def __str__(self):
        return f"{self.pessoa} - {self.data} :: {self.camera} - {self.data}"

