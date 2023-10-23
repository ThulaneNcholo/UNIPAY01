from django.db import models
from inventory.models import *

# Create your models here.


class ExpensesCategory(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name


class ExpenseModel(models.Model):
    ref = models.CharField(max_length=200, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    amount = models.DecimalField(
        max_digits=30, decimal_places=2, null=True, blank=True)
    description = models.TextField(blank=True)
    category = models.ForeignKey(CategoryModel, null=True, on_delete=models.CASCADE,
                                 blank=True, default=None, related_name='expense_category')
    expense_category = models.ForeignKey(ExpensesCategory, null=True, on_delete=models.CASCADE,
                                 blank=True, default=None, related_name='category_expenses')
    expenseDate = models.DateField(null=True, blank=True)
    month = models.CharField(max_length=200, null=True, blank=True)
    year = models.CharField(max_length=200, null=True, blank=True)
    file = models.FileField(
        null=True, blank=True, upload_to='static/receipts')
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.ref
