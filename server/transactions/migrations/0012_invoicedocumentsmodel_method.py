# Generated by Django 4.2.5 on 2023-10-07 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0011_invoicedocumentsmodel_documentmonth_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoicedocumentsmodel',
            name='method',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
