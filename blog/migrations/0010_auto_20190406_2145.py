# Generated by Django 2.1.3 on 2019-04-06 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_auto_20190403_2121'),
    ]

    operations = [
        migrations.RenameField(
            model_name='projet',
            old_name='fichier',
            new_name='fichier_projet',
        ),
    ]
