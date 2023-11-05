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
    face = models.ForeignKey(Faces, on_delete=models.CASCADE)
    verify = models.BooleanField(default=False)
    distance = models.FloatField(default=0.0)
    pessoa = models.ForeignKey(Pessoas, on_delete=models.CASCADE)
    auditado = models.BooleanField(default=False)
    
    class Meta:
        verbose_name_plural = "FAces Auditadas"
        verbose_name = "Face Auditada"

    def __str__(self):
        return f"{self.id} - {self.pessoa.nome} - {self.pessoa.nome} - {self.auditado}"


class FacesPrevisaoEmocional(baseModel):
    face = models.ForeignKey(Faces, on_delete=models.CASCADE)
    pessoa = models.ForeignKey(Pessoas, on_delete=models.CASCADE, blank=True)
    previsao = models.JSONField
    auditado = models.BooleanField(default=False)
    
    class Meta:
        verbose_name_plural = "Faces Previsão Emocional"
        verbose_name = "Face Previsão Emocional"
        ordering = ['id', 'auditado',]

    def __str__(self):
        return f"{self.id} - {self.face.id} - {self.auditado}"