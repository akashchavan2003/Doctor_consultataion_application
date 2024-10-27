# Generated by Django 4.1.13 on 2024-10-15 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_remove_doctor_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appointmentslot',
            name='doctor',
        ),
        migrations.AddField(
            model_name='appointmentslot',
            name='doctor_user_id',
            field=models.TextField(null=True),
        ),
    ]