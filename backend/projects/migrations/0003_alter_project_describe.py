# Generated by Django 4.0.1 on 2022-03-21 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_rename_imges_project_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='describe',
            field=models.TextField(default='', null=True, verbose_name='描述'),
        ),
    ]