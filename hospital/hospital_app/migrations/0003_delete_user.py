# Generated by Django 4.2.4 on 2024-01-25 14:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hospital_app', '0002_user'),
    ]

    operations = [
        migrations.DeleteModel(
            name='User',
        ),
    ]