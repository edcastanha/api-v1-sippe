# Generated by Django 4.2.5 on 2023-10-17 03:40

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('cameras', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='processamentos',
            name='dia',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='processamentos',
            name='path',
            field=models.CharField(default=django.utils.timezone.now, max_length=150, unique=True),
            preserve_default=False,
        ),
    ]
