# Generated by Django 4.2.1 on 2023-10-29 00:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_child_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='child',
            name='birth_mark',
            field=models.CharField(default='none', max_length=100),
        ),
        migrations.AddField(
            model_name='child',
            name='child_height',
            field=models.IntegerField(default=None, max_length=100),
        ),
    ]
