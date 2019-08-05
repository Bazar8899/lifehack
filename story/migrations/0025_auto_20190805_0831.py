# Generated by Django 2.2.1 on 2019-08-05 08:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('story', '0024_auto_20190728_0717'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='step',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='story.StoryStep', verbose_name='Step'),
        ),
        migrations.AlterField(
            model_name='content',
            name='height',
            field=models.IntegerField(choices=[(0, 'Short'), (1, 'Tall')], default=0),
        ),
        migrations.AlterField(
            model_name='content',
            name='width',
            field=models.IntegerField(choices=[(1, 'Small'), (2, 'Medium'), (3, 'Big')], default=0, verbose_name='Text box width'),
        ),
    ]
