# Generated by Django 2.2.1 on 2019-05-21 18:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='challenge',
            name='maxScore',
        ),
    ]
