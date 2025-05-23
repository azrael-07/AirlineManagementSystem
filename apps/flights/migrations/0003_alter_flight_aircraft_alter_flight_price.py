# Generated by Django 5.1.6 on 2025-03-26 15:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flights', '0002_flight_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flight',
            name='aircraft',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flights.aircraft'),
        ),
        migrations.AlterField(
            model_name='flight',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
