# Generated by Django 4.2.5 on 2023-10-07 06:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0010_invoicedocumentsmodel_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoicedocumentsmodel',
            name='documentMonth',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='invoicedocumentsmodel',
            name='documentYear',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
