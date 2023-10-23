from django.contrib import admin
from .models import CategoryModel, InventoryModel, ServicesModel

# Register your models here.
admin.site.register(CategoryModel)
admin.site.register(InventoryModel)
admin.site.register(ServicesModel)
