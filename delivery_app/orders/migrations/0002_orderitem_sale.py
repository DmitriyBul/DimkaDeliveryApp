# Generated by Django 3.2.7 on 2021-10-23 05:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='sale',
            field=models.IntegerField(default=0),
        ),
    ]
