# Generated by Django 3.2.5 on 2021-07-15 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_alter_estaciones_terrenas_tipo_antena'),
    ]

    operations = [
        migrations.AddField(
            model_name='estaciones_terrenas',
            name='modulacion',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
