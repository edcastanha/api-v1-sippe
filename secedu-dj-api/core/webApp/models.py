from django.db import models

class baseModel(models.Model):
    data_cadastro = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class dashboards(baseModel):
    nome = models.CharField(max_length=50)
    count = models.IntegerField()