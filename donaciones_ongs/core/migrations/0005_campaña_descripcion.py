# Generated by Django 5.2.3 on 2025-06-16 00:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_campaña_donacion'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaña',
            name='descripcion',
            field=models.TextField(default='Sin descripción'),
        ),
    ]
