from django.db import models
from django.core.exceptions import ValidationError

# CLASS FOTOS
from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver
import os

# MODELO BASE
class baseModel(models.Model):
    data_cadastro = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Contratos(baseModel):
    protocolo = models.CharField(max_length=100)
    assinado_em = models.DateTimeField()
    responsavel = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Contratos"
        verbose_name = "Contrato"

    def __str__(self):
        return f"{self.protocolo} - {self.responsavel}"


class Escolas(baseModel):
    nome = models.CharField(max_length=100)
    contrato = models.ForeignKey(Contratos, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Escolas"
        verbose_name = "Escola"

    def __str__(self):
        return self.nome

class Pessoas(baseModel):
    CHOICE_SEXO = (
        ('Masculino', 'Masculino'),
        ('Feminino', 'Feminino'),
        ('Outros', 'Outros'),
    )

    CHOICE_PERFIL = (
        ('Tutor', 'Tutor'),
        ('Colaborador', 'Colaborador'),
        ('Estudante', 'Estudante'),
    )

    nome = models.CharField(max_length=100)
    sexo = models.CharField(max_length=10, choices=CHOICE_SEXO)
    perfil = models.CharField(max_length=11, choices=CHOICE_PERFIL)
    ra = models.CharField(max_length=10, blank=True, null=True)
    #turma = models.ForeignKey(Turmas,
    #                          on_delete=models.CASCADE,
    #                          verbose_name='turma',
    #                          related_name='pessoas',
    #                          )

    def clean(self):
        super().clean()

        if not self.ra:
            raise ValidationError('O campo RA é obrigatório para estudantes.')

    class Meta:
        verbose_name_plural = "Pessoas"
        verbose_name = "Pessoa"

    def __str__(self):
        return f"{self.nome} - {self.perfil} - {self.ra}"
    
class Turmas(baseModel):
    CHOICE_PERIODOS = (
        ('Morning', 'Morning'),
        ('Afternoon', 'Afternoon'),
        ('Outros', 'Outros'),
    )

    nome = models.CharField(max_length=50)
    periodo = models.CharField(max_length=10, choices=CHOICE_PERIODOS)
    escola = models.ForeignKey(Escolas, on_delete=models.CASCADE, blank=False, null=False)
    alunos =models.ManyToManyField(Pessoas, through='Aluno')
    
    class Meta:
        verbose_name_plural = "Turmas"
        verbose_name = "Turma"

    def __str__(self):
        return f"{self.nome} - {self.periodo}"

class Aluno(baseModel):
    pessoa = models.ForeignKey(Pessoas, on_delete=models.CASCADE)
    turma = models.ForeignKey(Turmas, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name_plural = "Alunos"
        verbose_name = "Alunos"

    def __str__(self):
        return f"{self.pessoa.nome} - {self.turma.nome}"

class Fotos(models.Model):
    def get_upload_path(instance, filename):
        return f'fotos/{instance.pessoa.ra}/{filename}'

    pessoa = models.ForeignKey(Pessoas, on_delete=models.CASCADE,)
    foto = models.ImageField(blank=False, null=False,
                             upload_to=get_upload_path)

    class Meta:
        verbose_name_plural = "Fotos"
        verbose_name = "Foto"

    def __str__(self):
        return f"{self.pessoa.nome} - {self.foto}"

    def save(self, *args, **kwargs):
        if Fotos.objects.filter(pessoa=self.pessoa).count() >= 10:
            raise ValidationError(
                'Este cadastro já possui o limite de 10 fotos.')
        super().save(*args, **kwargs)

# Atualiza files de fotos ao Atualizar ou Excluir Fotos
@receiver(pre_delete, sender=Fotos)
def foto_pre_delete(sender, instance, **kwargs):
    # Exclui o arquivo de imagem quando o registro é excluído
    if instance.foto:
        if os.path.isfile(instance.foto.path):
            os.remove(instance.foto.path)

@receiver(pre_save, sender=Fotos)
def foto_pre_save(sender, instance, **kwargs):
    # Atualiza o arquivo de imagem quando o registro é atualizado
    if instance.pk:
        old_foto = Fotos.objects.get(pk=instance.pk).foto
        if old_foto:
            if not old_foto == instance.foto:
                if os.path.isfile(old_foto.path):
                    os.remove(old_foto.path)
