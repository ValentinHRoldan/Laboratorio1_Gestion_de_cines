# Generated by Django 5.1.7 on 2025-05-26 19:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('funciones', '0008_remove_sala_nombre'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='funcion',
            unique_together={('fecha', 'hora', 'sala', 'tipo_formato')},
        ),
    ]
