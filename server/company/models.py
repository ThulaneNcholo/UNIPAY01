from django.db import models
from client.models import AddressModel

# Create your models here.


class CompanyInfoModel(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(blank=True, null=True)
    registration = models.CharField(max_length=200, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name


class BankModel(models.Model):
    bankName = models.CharField(max_length=200, null=True, blank=True)
    branch = models.CharField(max_length=200, null=True, blank=True)
    account = models.CharField(max_length=200, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.bankName


class ProfileModel(models.Model):
    ref = models.CharField(max_length=200, null=True, blank=True)
    companyInfo = models.ForeignKey(CompanyInfoModel, null=True, on_delete=models.CASCADE,
                                    blank=True, default=None, related_name='company_info')
    bank = models.ForeignKey(BankModel, null=True, on_delete=models.CASCADE,
                             blank=True, default=None, related_name='company_bank')
    address = models.ForeignKey(AddressModel, null=True, on_delete=models.CASCADE,
                                blank=True, default=None, related_name='company_address')
    logo = models.ImageField(
        null=True, blank=True, upload_to='static/images')
    status = models.CharField(
        max_length=200, null=True, blank=True, default='Pending')
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.ref
