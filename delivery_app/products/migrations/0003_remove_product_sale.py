# Generated by Django 3.2.7 on 2021-10-17 08:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_product_sale'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='sale',
        ),
    ]
