# Generated by Django 4.2.5 on 2023-09-28 15:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0002_profilemodel_logo'),
        ('transactions', '0007_transactionmodel_bank_transactionmodel_company_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='transactionmodel',
            name='bankRef',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='transactionmodel',
            name='bank',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='invoice_bank', to='company.bankmodel'),
        ),
    ]
