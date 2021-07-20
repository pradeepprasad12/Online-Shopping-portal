# Generated by Django 3.1.7 on 2021-05-31 16:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shop', '0009_orderupdate'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='user1',
            field=models.ForeignKey(default = 1, on_delete=django.db.models.deletion.CASCADE, to='auth.user'),
            preserve_default=False,
        ),
    ]