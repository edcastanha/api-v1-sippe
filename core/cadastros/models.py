from django.db import models
from core.cameras.models import Locais

class baseModel(models.Model):
    data_cadastro = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Escolas(baseModel):
    nome = models.CharField(max_length=100)
    cnpj = models.CharField(max_length=14)

    class Meta:
        verbose_name_plural = "Escolas"

    def __str__(self):
        return self.nome



class Pessoas(baseModel):
    CHOICE_SEXO = (
        ('M', 'Masculino'),
        ('F', 'Feminino'),
        ('O', 'Outros'),
    )

    CHOICE_PERFIL = (
        ('T', 'Tutor'),
        ('C', 'Colaborador'),
        ('E', 'Estudante'),
    )

    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=11)
    escola = models.ForeignKey(Escolas, on_delete=models.CASCADE)
    sexo = models.CharField(max_length=1, choices=CHOICE_SEXO)
    perfil = models.CharField(max_length=1, choices=CHOICE_PERFIL)

    class Meta:
        verbose_name_plural = "Pessoas"

    def __str__(self):
        return f"{self.nome} - {self.escola.nome}"


class Presencas(baseModel):
    pessoa = models.ForeignKey(Pessoas, on_delete=models.CASCADE)
    data = models.DateField()
    hora = models.TimeField()
    local = models.ForeignKey(Locais, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Presencas"

    def __str__(self):
        return f"{self.pessoa.nome} - {self.data} - {self.hora} - {self.local.nome}"
