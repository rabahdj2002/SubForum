# Generated by Django 5.1.4 on 2024-12-15 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subforum', '0002_projects_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='projects',
            name='files',
            field=models.JSONField(default=list),
        ),
    ]
