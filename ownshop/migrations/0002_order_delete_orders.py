# Generated by Django 4.0.2 on 2022-08-25 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ownshop', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('provider_order_id', models.CharField(max_length=40)),
                ('payment_id', models.CharField(max_length=36)),
                ('signature_id', models.CharField(max_length=128)),
                ('status', models.BooleanField(default=False)),
                ('items_json', models.CharField(default='', max_length=5000)),
                ('amount', models.IntegerField(default=0)),
                ('email', models.CharField(default='', max_length=100)),
                ('name', models.CharField(default='', max_length=100)),
                ('address', models.CharField(default='', max_length=1000)),
                ('city', models.CharField(default='', max_length=500)),
                ('state', models.CharField(default='', max_length=500)),
                ('zip_code', models.CharField(default='', max_length=100)),
                ('mobile', models.CharField(default='', max_length=20)),
            ],
        ),
        migrations.DeleteModel(
            name='Orders',
        ),
    ]
