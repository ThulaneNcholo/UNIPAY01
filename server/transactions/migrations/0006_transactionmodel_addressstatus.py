# Generated by Django 4.2.5 on 2023-09-26 20:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0005_transactionmodel_transactionstatus'),
    ]

    operations = [
        migrations.AddField(
            model_name='transactionmodel',
            name='addressStatus',
            field=models.CharField(blank=True, default='No', max_length=200, null=True),
        ),
    ]