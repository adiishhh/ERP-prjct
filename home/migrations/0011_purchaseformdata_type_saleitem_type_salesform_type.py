# Generated by Django 5.1.1 on 2024-10-07 06:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0010_salesform_saleitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchaseformdata',
            name='type',
            field=models.CharField(default='Cash', max_length=200),
        ),
        migrations.AddField(
            model_name='saleitem',
            name='type',
            field=models.CharField(default='Cash', max_length=200),
        ),
        migrations.AddField(
            model_name='salesform',
            name='type',
            field=models.CharField(default='Cash', max_length=200),
        ),
    ]
