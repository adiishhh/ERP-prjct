# Generated by Django 5.1.1 on 2024-10-03 04:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_employeecontactform'),
    ]

    operations = [
        migrations.CreateModel(
            name='categoryFormData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
    ]
