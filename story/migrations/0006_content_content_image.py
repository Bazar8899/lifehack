# Generated by Django 2.2.1 on 2019-06-27 04:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('story', '0005_auto_20190627_0327'),
    ]

    operations = [
        migrations.AddField(
            model_name='content',
            name='content_image',
            field=models.ImageField(default=None, upload_to='media/character_image', verbose_name='Character Image'),
        ),
    ]
