# Generated by Django 3.2.5 on 2021-08-16 01:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_mensajeadmin'),
    ]

    operations = [
        migrations.AddField(
            model_name='radioaficionados',
            name='pais',
            field=models.CharField(blank=True, max_length=30),
        ),
    ]
