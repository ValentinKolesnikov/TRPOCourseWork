# Generated by Django 2.1.4 on 2019-04-24 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0024_week'),
    ]

    operations = [
        migrations.AddField(
            model_name='week',
            name='timework',
            field=models.CharField(default='Пн-Пт 10:00-18:00', max_length=30),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='worktime',
            field=models.CharField(max_length=30),
        ),
    ]
