# Generated by Django 3.2.5 on 2021-08-10 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_alter_estaciones_terrenas_ganancia'),
    ]

    operations = [
        migrations.AlterField(
            model_name='estaciones_terrenas',
            name='ganancia',
            field=models.IntegerField(blank=True),
        ),
    ]