# Generated by Django 4.1.13 on 2024-08-10 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_patient_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='age',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=3, null=True),
        ),
    ]