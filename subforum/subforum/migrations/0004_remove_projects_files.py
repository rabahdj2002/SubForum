# Generated by Django 5.1.4 on 2024-12-15 19:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('subforum', '0003_projects_files'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='projects',
            name='files',
        ),
    ]
