# Generated by Django 2.1.7 on 2019-02-21 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0004_auto_20190215_1613'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='restaurant',
            name='countmark',
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='mark',
            field=models.IntegerField(default='0', editable=False),
        ),
    ]
