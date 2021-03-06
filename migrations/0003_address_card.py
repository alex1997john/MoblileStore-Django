# Generated by Django 3.1 on 2020-10-30 18:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mobicart', '0002_cart'),
    ]

    operations = [
        migrations.CreateModel(
            name='card',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('card_number', models.IntegerField()),
                ('expiry', models.TextField()),
                ('cvv', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('mobileno', models.IntegerField()),
                ('house_name', models.TextField()),
                ('area', models.TextField()),
                ('state', models.TextField()),
                ('pincode', models.IntegerField()),
                ('address_type', models.TextField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
