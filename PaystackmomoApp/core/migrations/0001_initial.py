# Generated by Django 4.0.6 on 2022-07-31 06:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BankPayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=200)),
                ('ref', models.CharField(max_length=200)),
                ('amount', models.PositiveBigIntegerField()),
                ('verified', models.BooleanField(default=False)),
                ('currency_charged', models.CharField(max_length=3)),
                ('date_created', models.DateField(auto_now_add=True)),
            ],
            options={
                'ordering': ('-date_created',),
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=200)),
                ('ref', models.CharField(max_length=200)),
                ('amount', models.PositiveBigIntegerField()),
                ('verified', models.BooleanField(default=False)),
                ('currency_charged', models.CharField(max_length=3)),
                ('date_created', models.DateField(auto_now_add=True)),
            ],
            options={
                'ordering': ('-date_created',),
            },
        ),
        migrations.CreateModel(
            name='MobileMoneyProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('provider', models.CharField(max_length=5)),
                ('number', models.CharField(max_length=50)),
                ('currency', models.CharField(max_length=150)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BankPaymentProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('bank_name', models.CharField(max_length=150)),
                ('account_name', models.CharField(max_length=150)),
                ('account_number', models.CharField(max_length=150)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
