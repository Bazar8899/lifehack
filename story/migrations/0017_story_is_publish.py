# Generated by Django 2.2.1 on 2019-07-18 04:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('story', '0016_auto_20190708_0101'),
    ]

    operations = [
        migrations.AddField(
            model_name='story',
            name='is_publish',
            field=models.IntegerField(choices=[(0, 'Publish'), (1, 'Un publish')], default=0),
        ),
    ]
