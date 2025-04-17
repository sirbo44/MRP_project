# Generated by Django 5.0.6 on 2025-04-17 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Archive',
            fields=[
                ('id', models.CharField(max_length=16, primary_key=True, serialize=False)),
                ('customer', models.CharField(max_length=255)),
                ('date', models.CharField(max_length=12)),
                ('schedule', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand', models.CharField(max_length=255)),
                ('tin', models.CharField(max_length=64)),
                ('phone', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer', models.CharField(max_length=255)),
                ('date', models.CharField(max_length=12)),
                ('schedule', models.CharField(max_length=300)),
            ],
        ),
    ]
