# Generated by Django 2.2.1 on 2019-06-26 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_auto_20190626_0801'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lhuser',
            name='device_id',
            field=models.CharField(default='', max_length=100, verbose_name='Гар утасны id'),
        ),
        migrations.AlterField(
            model_name='lhuser',
            name='first_name',
            field=models.CharField(blank=True, default='', max_length=100, verbose_name='Нэр'),
        ),
        migrations.AlterField(
            model_name='lhuser',
            name='gender',
            field=models.IntegerField(choices=[(0, 'Эмэгтэй'), (1, 'Эрэгтэй'), (2, 'Аль нь ч биш')], default=0, verbose_name='Хүйс'),
        ),
        migrations.AlterField(
            model_name='lhuser',
            name='last_name',
            field=models.CharField(blank=True, default='', max_length=100, verbose_name='Овог'),
        ),
        migrations.AlterField(
            model_name='lhuser',
            name='username',
            field=models.CharField(default='', max_length=100, verbose_name='Нэвтрэх нэр'),
        ),
    ]
