# Generated by Django 3.2.5 on 2021-08-03 01:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_comentarios'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bitacoras',
            old_name='enlace',
            new_name='mensaje1',
        ),
        migrations.RenameField(
            model_name='bitacoras',
            old_name='estacion_rec',
            new_name='mensaje2',
        ),
        migrations.RenameField(
            model_name='bitacoras',
            old_name='modulacion',
            new_name='mensaje3',
        ),
        migrations.RenameField(
            model_name='bitacoras',
            old_name='grid',
            new_name='modo',
        ),
        migrations.RemoveField(
            model_name='bitacoras',
            name='reporte1',
        ),
        migrations.RemoveField(
            model_name='bitacoras',
            name='reporte2',
        ),
        migrations.AddField(
            model_name='bitacoras',
            name='db',
            field=models.IntegerField(blank=True, default=None),
        ),
        migrations.AddField(
            model_name='bitacoras',
            name='dt',
            field=models.FloatField(default=None),
        ),
        migrations.AddField(
            model_name='bitacoras',
            name='freq_tx',
            field=models.IntegerField(blank=True, default=None),
        ),
        migrations.AddField(
            model_name='bitacoras',
            name='rt',
            field=models.CharField(blank=True, max_length=2),
        ),
    ]
