# Generated by Django 2.1.7 on 2019-02-21 16:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0008_auto_20190221_1832'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Comments',
            new_name='Comment',
        ),
        migrations.RenameField(
            model_name='comment',
            old_name='restaurant',
            new_name='restaurant_id',
        ),
    ]