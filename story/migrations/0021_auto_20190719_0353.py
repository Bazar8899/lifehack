# Generated by Django 2.2.1 on 2019-07-19 03:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('story', '0020_userstory_answer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userstory',
            name='step',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='story.StoryStep'),
        ),
    ]
