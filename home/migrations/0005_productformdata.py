# Generated by Django 5.1.1 on 2024-10-03 05:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_vendorcontactform'),
    ]

    operations = [
        migrations.CreateModel(
            name='productFormData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('unit', models.CharField(max_length=200)),
                ('price', models.CharField(max_length=200)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.categoryformdata')),
            ],
        ),
    ]
