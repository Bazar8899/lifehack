# Generated by Django 2.2.1 on 2019-06-26 05:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
        ('story', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='content',
            name='characters',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='user.Character'),
        ),
        migrations.AddField(
            model_name='content',
            name='question',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='story.Question', verbose_name='Question'),
        ),
        migrations.AddField(
            model_name='content',
            name='step',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='story.StoryStep', verbose_name='Step'),
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='story.Question', verbose_name='Question'),
        ),
    ]