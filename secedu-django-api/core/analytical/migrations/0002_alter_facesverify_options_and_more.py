# Generated by Django 4.2.5 on 2023-11-06 17:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('analytical', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='facesverify',
            options={'verbose_name': 'Face Auditada', 'verbose_name_plural': 'Faces Auditadas'},
        ),
        migrations.RemoveField(
            model_name='facesprevisaoemocional',
            name='pessoa',
        ),
    ]