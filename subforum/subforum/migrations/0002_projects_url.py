# Generated by Django 5.1.4 on 2024-12-15 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subforum', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='projects',
            name='url',
            field=models.CharField(default='', max_length=255),
        ),
    ]