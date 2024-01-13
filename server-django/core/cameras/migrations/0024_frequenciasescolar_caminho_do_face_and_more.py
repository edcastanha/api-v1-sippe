# Generated by Django 4.2.7 on 2023-11-23 07:20

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('cameras', '0023_alter_faces_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='frequenciasescolar',
            name='caminho_do_face',
            field=models.CharField(default=django.utils.timezone.now, max_length=500),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='frequenciasescolar',
            name='file_dataset',
            field=models.CharField(default=django.utils.timezone.now, max_length=500),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='frequenciasescolar',
            name='processo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cameras.processamentos'),
        ),
    ]