# Generated by Django 2.2.1 on 2019-05-22 07:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_auto_20190521_1840'),
    ]

    operations = [
        migrations.AddField(
            model_name='challenge',
            name='Score',
            field=models.CharField(default='100', max_length=10, verbose_name='Score'),
        ),
    ]
