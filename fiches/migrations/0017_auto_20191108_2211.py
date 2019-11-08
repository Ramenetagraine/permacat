# Generated by Django 2.1.11 on 2019-11-08 21:11

from django.db import migrations, models
import uuid

from fiches.models import Fiche, Atelier  #where app == tango_app_name

class Migration(migrations.Migration):

    dependencies = [
        ('fiches', '0016_auto_20191108_2209'),
    ]

    def gen_uuid(apps, schema_editor):
        for row in Fiche.objects.all():
            row.slug = uuid.uuid4()
            row.save()

        for row in Atelier.objects.all():
            row.slug = uuid.uuid4()
            row.save()

    operations = [
        migrations.AddField(
            model_name='fiche',
            name='slug',
            field=models.SlugField(default=uuid.uuid4),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='atelier',
            name='slug',
            field=models.SlugField(default=uuid.uuid4),
            preserve_default=True,
        ),

        migrations.RunPython(gen_uuid),

        migrations.AlterField(
            model_name='fiche',
            name='slug',
            field=models.SlugField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='atelier',
            name='slug',
            field=models.SlugField(max_length=100, unique=True),
        ),
    ]
