# Generated by Django 5.1.4 on 2024-12-22 21:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subforum', '0003_projects_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projects',
            name='url',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
