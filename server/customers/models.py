from django.db import models
from client.models import *
from company.models import *
from inventory.models import *
import datetime

# Create your models here.


class CustomerModel(models.Model):
    ref = models.CharField(max_length=200, null=True, blank=True)
    firstName = models.CharField(max_length=200, null=True, blank=True)
    lastName = models.CharField(max_length=200, null=True, blank=True)
    address = models.ForeignKey(AddressModel, null=True, on_delete=models.CASCADE,
                                blank=True, default=None, related_name='customer_address')
    phone = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(blank=True, null=True)
    company_name = models.CharField(max_length=200, null=True, blank=True)
    company_registered_number = models.CharField(
        max_length=200, null=True, blank=True)
    company_tax_number = models.CharField(
        max_length=200, null=True, blank=True)
    bank = models.ForeignKey(BankModel, null=True, on_delete=models.CASCADE,
                             blank=True, default=None, related_name='customer_bank')
    logo = models.ImageField(
        null=True, blank=True, upload_to='static/images')
    month = models.CharField(max_length=200, null=True, blank=True)
    year = models.CharField(max_length=200, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.ref


class DocumentModel(models.Model):
    beanUser = models.ForeignKey(UserModel, null=True, on_delete=models.CASCADE,
                                 blank=True, default=None, related_name='user_document')
    client = models.ForeignKey(CustomerModel, null=True, on_delete=models.CASCADE,
                               blank=True, default=None, related_name='customer_document')
    documentType = models.CharField(max_length=200, null=True, blank=True)
    item = models.ForeignKey(InventoryModel, null=True, on_delete=models.CASCADE,
                             blank=True, default=None, related_name='item_document')
    services = models.ForeignKey(ServicesModel, null=True, on_delete=models.CASCADE,
                                 blank=True, default=None, related_name='service_document')
    quantity = models.IntegerField(null=True, blank=True)
    total = models.DecimalField(
        max_digits=30, decimal_places=2, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.beanUser.userRef
