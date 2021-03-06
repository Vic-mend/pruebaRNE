# Generated by Django 3.2.5 on 2021-07-14 17:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_remove_radioaficionados_last_login'),
    ]

    operations = [
        migrations.CreateModel(
            name='estaciones_terrenas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_estacion', models.CharField(max_length=30)),
                ('marca', models.CharField(max_length=30)),
                ('modelo', models.CharField(max_length=40)),
                ('antena', models.CharField(max_length=30)),
                ('tipo_antena', models.IntegerField()),
                ('ganancia', models.IntegerField(blank=True)),
                ('frecuencia', models.CharField(max_length=20)),
                ('polarizacion', models.CharField(max_length=20)),
                ('altura', models.DecimalField(decimal_places=4, max_digits=7)),
                ('grid', models.CharField(max_length=10)),
                ('indicativo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.radioaficionados')),
            ],
        ),
    ]
