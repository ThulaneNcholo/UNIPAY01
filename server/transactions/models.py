from django.db import models
from inventory.models import InventoryModel, ServicesModel
from client.models import AddressModel
from customers.models import CustomerModel
from company.models import *

# Create your models here.


class InvoiceDocumentsModel(models.Model):
    docuemntType = models.CharField(max_length=200, null=True, blank=True)
    method = models.CharField(max_length=200, null=True, blank=True)
    inventory = models.ForeignKey(InventoryModel, null=True, on_delete=models.CASCADE,
                                  blank=True, default=None, related_name='document_inventory')
    service = models.ForeignKey(ServicesModel, null=True, on_delete=models.CASCADE,
                                blank=True, default=None, related_name='document_service')
    documentQuantity = models.IntegerField(null=True, blank=True)
    documentTotal = models.DecimalField(
        max_digits=30, decimal_places=2, null=True, blank=True)
    documentMonth = models.CharField(max_length=200, null=True, blank=True)
    documentYear = models.CharField(max_length=200, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.docuemntType


class PaymentHistoryModel(models.Model):
    ref = models.CharField(max_length=200, null=True, blank=True)
    paid = models.DecimalField(
        max_digits=30, decimal_places=2, null=True, blank=True)
    date = models.DateField(auto_now_add=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.ref


class RecurringTransaction(models.Model):
    recurrence_period = models.IntegerField(null=True, blank=True)
    start_date = models.IntegerField(null=True, blank=True)
    status = models.CharField(
        max_length=200, null=True, blank=True, default='Active')
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.status


class TransactionModel(models.Model):
    ref = models.CharField(max_length=200, null=True, blank=True)
    transactionMethod = models.CharField(max_length=200, null=True, blank=True)
    item = models.ForeignKey(InventoryModel, null=True, on_delete=models.CASCADE,
                             blank=True, default=None, related_name='inventory')
    addressStatus = models.CharField(
        max_length=200, null=True, blank=True, default='No')
    address = models.ForeignKey(AddressModel, null=True, on_delete=models.CASCADE,
                                blank=True, default=None, related_name='address')
    customer = models.ForeignKey(CustomerModel, null=True, on_delete=models.CASCADE,
                                 blank=True, default=None, related_name='customer')
    quantity = models.IntegerField(null=True, blank=True)
    income = models.DecimalField(
        max_digits=30, decimal_places=2, null=True, blank=True)
    paid = models.DecimalField(
        max_digits=30, decimal_places=2, null=True, blank=True)
    discount = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True)
    discounted_price = models.DecimalField(
        max_digits=30, decimal_places=2, null=True, blank=True)
    fullName = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=200, null=True, blank=True)
    transactionStatus = models.CharField(
        max_length=200, null=True, blank=True, default='Pending')
    # documents data
    company = models.ForeignKey(ProfileModel, null=True, on_delete=models.CASCADE,
                                blank=True, default=None, related_name='company')
    bank = models.ForeignKey(BankModel, null=True, on_delete=models.CASCADE,
                             blank=True, default=None, related_name='invoice_bank')
    bankRef = models.CharField(max_length=200, null=True, blank=True)
    notes = models.TextField(blank=True)
    issueDate = models.DateField(null=True, blank=True)
    dueDate = models.DateField(null=True, blank=True)
    transactionDocuments = models.ManyToManyField(
        InvoiceDocumentsModel, blank=True, default=None, related_name='documents')
    payments = models.ManyToManyField(
        PaymentHistoryModel, blank=True, default=None, related_name='payment_history')
    amountPaid = models.DecimalField(
        max_digits=30, decimal_places=2, null=True, blank=True)
    outstandingBalance = models.DecimalField(
        max_digits=30, decimal_places=2, null=True, blank=True)
    recurring_transaction = models.ForeignKey(RecurringTransaction, null=True, on_delete=models.CASCADE,
                                              blank=True, default=None, related_name='recurring_transaction')
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.ref
