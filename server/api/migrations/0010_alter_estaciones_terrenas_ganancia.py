# Generated by Django 3.2.5 on 2021-08-10 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_auto_20210802_2003'),
    ]

    operations = [
        migrations.AlterField(
            model_name='estaciones_terrenas',
            name='ganancia',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
