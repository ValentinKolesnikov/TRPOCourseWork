# Generated by Django 2.1.4 on 2019-04-10 09:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0018_auto_20190410_1147'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='restaurant',
            name='category',
        ),
    ]