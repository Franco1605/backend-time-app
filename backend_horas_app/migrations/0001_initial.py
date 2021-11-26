# Generated by Django 3.2.5 on 2021-11-19 13:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Persona',
            fields=[
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=255)),
                ('correo', models.CharField(max_length=255)),
                ('password', models.CharField(max_length=255)),
                ('area', models.CharField(max_length=255)),
                ('id_calendario', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Proyectos',
            fields=[
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Eventos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=255)),
                ('descripcion', models.CharField(max_length=255)),
                ('participantes', models.IntegerField()),
                ('inicio', models.DateTimeField()),
                ('termino', models.DateTimeField()),
                ('id_persona', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend_horas_app.persona')),
            ],
        ),
    ]
