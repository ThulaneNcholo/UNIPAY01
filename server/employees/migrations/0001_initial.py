# Generated by Django 4.2.5 on 2023-10-14 10:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('client', '0002_usermodel'),
        ('company', '0002_profilemodel_logo'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmployeesModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ref', models.CharField(blank=True, max_length=200, null=True)),
                ('firstName', models.CharField(blank=True, max_length=200, null=True)),
                ('lastName', models.CharField(blank=True, max_length=200, null=True)),
                ('phone', models.CharField(blank=True, max_length=50, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('payday', models.IntegerField(blank=True, null=True)),
                ('salary', models.DecimalField(blank=True, decimal_places=2, max_digits=30, null=True)),
                ('profile_image', models.ImageField(blank=True, null=True, upload_to='static/images')),
                ('status', models.CharField(blank=True, default='Active', max_length=200, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('address', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='employee_address', to='client.addressmodel')),
                ('bank', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='employee_bank', to='company.bankmodel')),
            ],
        ),
    ]
