# Generated by Django 5.1.6 on 2025-04-04 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pilot',
            name='pilotId',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
