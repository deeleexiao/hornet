# Generated by Django 4.0.1 on 2022-05-02 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='testresult',
            name='passed',
            field=models.IntegerField(default=0, verbose_name='错误用例'),
        ),
    ]