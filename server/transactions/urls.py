from django.urls import path
from .import views

urlpatterns = [
    # *********** Inventory Urls ***********
    path('inventory-sale/<int:id>', views.InventorySaleView, name='inventory-sale'),
    path('inventory-invoice/<int:id>/<int:method>',
         views.InventoryInvoiceView, name='inventory-invoice'),
    path('company-data', views.CompanyDataView, name='company-data'),
    path('company-bank', views.CompanyBankView, name='company-bank'),
    path('client-data', views.ClientDataView, name='client-data'),


    # *********** list all documnets ***********
    path('list-sales', views.ListSalesView, name='list-sales'),
    path('list-invoices', views.ListInvoicesView, name='list-invoices'),
    path('list-qoutes', views.ListQoutesView, name='list-qoutes'),

    # *********** Transaction Success or Fail ***********
    path('transaction-success/<int:id>',
         views.SuccessTransactionView, name='transaction-success'),

    # *********** view transaction document url ***********
    path('view-document/<int:id>/<int:method>',
         views.DocumentView, name='view-document'),
    path('create-transaction/<int:method>', views.MainTransactionView,
         name='create-transaction'),
]
