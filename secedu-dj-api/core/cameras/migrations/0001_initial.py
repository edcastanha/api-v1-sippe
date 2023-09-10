# Generated by Django 4.2.5 on 2023-09-09 22:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cadastros', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cameras',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_cadastro', models.DateTimeField(auto_now_add=True)),
                ('data_atualizacao', models.DateTimeField(auto_now=True)),
                ('descricao', models.CharField(max_length=100)),
                ('acesso', models.CharField(max_length=100)),
                ('modelo', models.CharField(max_length=50)),
                ('usuario', models.CharField(max_length=100)),
                ('senha', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Câmera',
                'verbose_name_plural': 'Câmeras',
            },
        ),
        migrations.CreateModel(
            name='NotaFiscal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_cadastro', models.DateTimeField(auto_now_add=True)),
                ('data_atualizacao', models.DateTimeField(auto_now=True)),
                ('numero', models.CharField(max_length=100)),
                ('data', models.DateTimeField()),
            ],
            options={
                'verbose_name': 'Nota Fiscal',
                'verbose_name_plural': 'Notas Fiscais',
            },
        ),
        migrations.CreateModel(
            name='Locais',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_cadastro', models.DateTimeField(auto_now_add=True)),
                ('data_atualizacao', models.DateTimeField(auto_now=True)),
                ('nome', models.CharField(max_length=100)),
                ('descricao', models.CharField(max_length=100)),
                ('camera', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cameras.cameras')),
                ('ponto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cadastros.escolas')),
            ],
            options={
                'verbose_name': 'Local',
                'verbose_name_plural': 'Locais',
            },
        ),
        migrations.CreateModel(
            name='Frequencias',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_cadastro', models.DateTimeField(auto_now_add=True)),
                ('data_atualizacao', models.DateTimeField(auto_now=True)),
                ('data', models.DateField()),
                ('hora', models.TimeField()),
                ('local', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cameras.locais')),
                ('pessoa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cadastros.pessoas')),
            ],
            options={
                'verbose_name': 'Frequência',
                'verbose_name_plural': 'Frequências',
            },
        ),
        migrations.AddField(
            model_name='cameras',
            name='nf',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cameras.notafiscal'),
        ),
    ]