from django.db import models
from core.cadastros.models import Pessoas, Aluno
from core.cameras.models import Faces

class baseModel(models.Model):
    data_cadastro = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ImagensTratadas(baseModel):
    face = models.ForeignKey(Faces, on_delete=models.CASCADE)
    auditado = models.BooleanField(default=False)
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Imagens Tratadas"
        verbose_name = "Imagem Tratada"
        ordering = ['id', 'auditado', 'status',]
    
    def __str__(self):
        return f"{self.id} :: {self.face.id} - {self.auditado}"

class FacesVerify(baseModel):
    CHOICE_STATUS = (
        ('0', 'Analisada'),
        ('1', 'Auditada'),
        ('2', 'Rejeitada'),
    )

    face = models.ForeignKey(Faces, on_delete=models.CASCADE)
    verify = models.BooleanField(default=False)
    distance = models.FloatField(default=0.0)
    auditado = models.BooleanField(default=False)
    pessoa = models.ForeignKey(Pessoas, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=1, choices=CHOICE_STATUS, default='0')
    class Meta:
        verbose_name_plural = "Faces Verificadas"
        verbose_name = "Face Verifica"

    def __str__(self):
        return f"{self.id} - {self.status} - {self.verify} - {self.auditado}"

class FacesPrevisaoEmocional(baseModel):
    CHOICE_EMOTION = (
        ('angry', 'Zangada'),
        ('disgust', 'Repulsa'),
        ('fear', 'Medo'),
        ('happy', 'Feliz'),
        ('neutral', 'Neutra'),
        ('sad', 'Triste'),
        ('surprise', 'Surpresa')
    )

    auditado = models.BooleanField(default=False, null=True, blank=True)
    predominante = models.CharField(max_length=10, choices=CHOICE_EMOTION, default='neutral')
    zangado = models.FloatField(default=0)
    repulsa = models.FloatField(default=0)
    medo = models.FloatField(default=0)
    feliz = models.FloatField(default=0)
    neutro = models.FloatField(default=0)
    triste = models.FloatField(default=0)
    surpresa = models.FloatField(default=0)
    
    
    class Meta:
        verbose_name_plural = "Faces Previsão Emocional"
        verbose_name = "Face Previsão Emocional"
        ordering = ['id', 'auditado',]

    def __str__(self):
        return f"{self.id} - {self.auditado} :: {self.predominante}"