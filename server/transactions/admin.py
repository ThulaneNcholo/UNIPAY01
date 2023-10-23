from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(TransactionModel)
admin.site.register(InvoiceDocumentsModel)
admin.site.register(PaymentHistoryModel)
admin.site.register(RecurringTransaction)
