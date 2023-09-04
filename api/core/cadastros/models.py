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
        return f"{self.numero} - {self.data}"

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
        ('M', 'Masculino'),
        ('F', 'Feminino'),
        ('O', 'Outros'),
    )

    CHOICE_PERFIL = (
        ('T', 'Tutor'),
        ('C', 'Colaborador'),
        ('E', 'Estudante'),
    )

    escola = models.ForeignKey(Escolas, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    sexo = models.CharField(max_length=1, choices=CHOICE_SEXO)
    perfil = models.CharField(max_length=1, choices=CHOICE_PERFIL)
    ra = models.CharField(max_length=10, blank=True, null=True)

    def clean(self):
        super().clean()

        if not self.ra:
            raise ValidationError('O campo RA é obrigatório para estudantes.')

    class Meta:
        verbose_name_plural = "Pessoas"
        verbose_name = "Pessoa"

    def __str__(self):
        return f"{self.nome} - {self.escola.nome}"

class Fotos(models.Model):
    def get_upload_path(instance, filename):
        return f'fotos/{instance.pessoa.ra}/{filename}'
    
    pessoa = models.ForeignKey(Pessoas, on_delete=models.CASCADE,)
    foto = models.ImageField(blank=False, null=False, upload_to=get_upload_path)

    class Meta:
        verbose_name_plural = "Fotos"
        verbose_name = "Foto"

    def __str__(self):
        return f"{self.pessoa.nome} - {self.foto}"
    
    def save(self, *args, **kwargs):
        if Fotos.objects.filter(pessoa=self.pessoa).count() >= 10:
            raise ValidationError('Este cadastro já possui o limite de 10 fotos.')
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
