# Generated by Django 5.1.6 on 2025-03-30 01:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('quantity', models.DecimalField(decimal_places=2, max_digits=10)),
                ('units_of_measure', models.CharField(max_length=50)),
                ('cost_per_unit', models.DecimalField(decimal_places=3, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='menu_item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('blerb', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='user',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='purchases',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('item', models.ForeignKey(default='OLD MENU ITEM', on_delete=django.db.models.deletion.SET_DEFAULT, to='django_delights.menu_item')),
            ],
        ),
        migrations.CreateModel(
            name='recipe_item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('dish', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='django_delights.menu_item')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='django_delights.ingredient')),
            ],
        ),
    ]
