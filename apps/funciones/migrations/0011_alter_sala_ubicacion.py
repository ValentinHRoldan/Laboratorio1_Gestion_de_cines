# Generated by Django 5.1.7 on 2025-05-27 04:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('funciones', '0010_alter_sala_ubicacion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sala',
            name='ubicacion',
            field=models.CharField(max_length=200),
        ),
    ]
