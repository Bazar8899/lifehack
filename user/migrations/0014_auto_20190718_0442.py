# Generated by Django 2.2.1 on 2019-07-18 04:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0013_auto_20190708_0101'),
    ]

    operations = [
        migrations.AlterField(
            model_name='character',
            name='character_type',
            field=models.IntegerField(choices=[(0, 'Straight'), (1, 'Lesbian'), (2, 'Gay'), (3, 'Transgender')], default=None, verbose_name='Character type'),
        ),
    ]
