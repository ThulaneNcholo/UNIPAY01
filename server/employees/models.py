from django.db import models
from client.models import *
from company.models import *

# Create your models here.


class EmployeesModel(models.Model):
    ref = models.CharField(max_length=200, null=True, blank=True)
    firstName = models.CharField(max_length=200, null=True, blank=True)
    lastName = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(blank=True, null=True)
    address = models.ForeignKey(AddressModel, null=True, on_delete=models.CASCADE,
                                blank=True, default=None, related_name='employee_address')
    bank = models.ForeignKey(BankModel, null=True, on_delete=models.CASCADE,
                             blank=True, default=None, related_name='employee_bank')
    payday = models.IntegerField(null=True, blank=True)
    salary = models.DecimalField(
        max_digits=30, decimal_places=2, null=True, blank=True)
    profile_image = models.ImageField(
        null=True, blank=True, upload_to='static/images')
    status = models.CharField(
        max_length=200, null=True, blank=True, default='Active')
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.ref
