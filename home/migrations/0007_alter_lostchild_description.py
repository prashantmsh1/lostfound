# Generated by Django 4.2.1 on 2023-10-29 01:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_lostchild_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lostchild',
            name='description',
            field=models.CharField(default=None, max_length=100),
        ),
    ]
