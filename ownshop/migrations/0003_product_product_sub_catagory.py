# Generated by Django 4.0.2 on 2023-08-09 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ownshop', '0002_order_delete_orders'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='product_sub_catagory',
            field=models.CharField(default='', max_length=200),
        ),
    ]