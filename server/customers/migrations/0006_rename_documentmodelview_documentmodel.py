# Generated by Django 4.2.5 on 2023-10-01 19:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0002_usermodel'),
        ('inventory', '0003_servicesmodel'),
        ('customers', '0005_documentmodelview'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='DocumentModelView',
            new_name='DocumentModel',
        ),
    ]