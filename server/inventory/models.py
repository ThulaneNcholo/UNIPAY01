from django.db import models

# Create your models here.


class CategoryModel(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name


class InventoryModel(models.Model):
    ref = models.CharField(max_length=200, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True)
    restocklevel = models.IntegerField(null=True, blank=True)
    unitprice = models.DecimalField(
        max_digits=30, decimal_places=2, null=True, blank=True)
    sellingprice = models.DecimalField(
        max_digits=30, decimal_places=2, null=True, blank=True)
    description = models.TextField(blank=True)
    category = models.ForeignKey(CategoryModel, null=True, on_delete=models.CASCADE,
                                 blank=True, default=None, related_name='item_category')
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.ref


class ServicesModel(models.Model):
    ref = models.CharField(max_length=200, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    serviceFee = models.DecimalField(
        max_digits=30, decimal_places=2, null=True, blank=True)
    description = models.TextField(blank=True)
    category = models.ForeignKey(CategoryModel, null=True, on_delete=models.CASCADE,
                                 blank=True, default=None, related_name='service_category')
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.ref
