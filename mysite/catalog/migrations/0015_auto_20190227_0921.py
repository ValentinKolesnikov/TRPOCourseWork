# Generated by Django 2.1.4 on 2019-02-27 06:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0014_auto_20190224_1424'),
    ]

    operations = [
        migrations.RenameField(
            model_name='restaurant',
            old_name='work',
            new_name='worktime',
        ),
    ]
