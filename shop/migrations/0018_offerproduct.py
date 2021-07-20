# Generated by Django 3.1.7 on 2021-06-20 07:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0017_orders_amount'),
    ]

    operations = [
        migrations.CreateModel(
            name='OfferProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=50)),
                ('desc', models.CharField(max_length=300)),
                ('image', models.ImageField(default='', upload_to='shop/images')),
            ],
        ),
    ]