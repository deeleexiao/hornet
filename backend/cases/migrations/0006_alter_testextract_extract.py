# Generated by Django 4.0.1 on 2022-07-07 00:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cases', '0005_testextract_extract_alter_testextract_value'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testextract',
            name='extract',
            field=models.CharField(max_length=1000, verbose_name='提取规则'),
        ),
    ]
