# Generated by Django 4.2.5 on 2023-10-25 05:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cameras', '0009_alter_processamentos_options'),
    ]

    operations = [
        migrations.RenameField(
            model_name='faces',
            old_name='path',
            new_name='path_face',
        ),
    ]