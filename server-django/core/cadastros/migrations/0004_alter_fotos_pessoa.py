# Generated by Django 4.2.5 on 2023-10-19 21:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cadastros', '0003_alter_escalas_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fotos',
            name='pessoa',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cadastros.aluno'),
        ),
    ]
