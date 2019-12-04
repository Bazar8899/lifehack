# Generated by Django 2.2.1 on 2019-07-07 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0011_auto_20190706_1340'),
    ]

    operations = [
        migrations.AlterField(
            model_name='character',
            name='avatar_img_l',
            field=models.ImageField(default=None, upload_to='media/character/avatar_l', verbose_name='Character avatar 3x'),
        ),
        migrations.AlterField(
            model_name='character',
            name='avatar_img_m',
            field=models.ImageField(default=None, upload_to='media/character/avatar_m', verbose_name='Character avatar 2x'),
        ),
        migrations.AlterField(
            model_name='character',
            name='avatar_img_s',
            field=models.ImageField(default=None, upload_to='media/character/avatar_s', verbose_name='Character avatar 1x'),
        ),
    ]