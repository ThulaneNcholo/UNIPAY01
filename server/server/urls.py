from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('client.urls')),
    path('company/', include('company.urls')),
    path('customers/', include('customers.urls')),
    path('inventory/', include('inventory.urls')),
    path('transactions/', include('transactions.urls')),
    path('expenses/', include('exepenses.urls')),
    path('todo/', include('todo.urls')),
    path('employees/', include('employees.urls')),
]
