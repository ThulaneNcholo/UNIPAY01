
from django.urls import path
from .import views

urlpatterns = [
    path('customers', views.CustomersView, name='customers'),
    path('add-customer', views.AddCustomerView, name='add-customer'),
    path('client-details/<int:id>',
         views.CustomerDetailsView, name='client-details'),

    # customer transactions
    path('customer-invoice/<int:id>/<int:method>',
         views.InvoicesCustomerView, name='customer-invoice'),

    # htmx urls
    path('remove-company', views.RemoveCompanyDetailsView, name='remove-company'),
    path('add-company-details', views.AddCompanyDetailsView,
         name='add-company-details'),

    path('add-customer-document', views.AddClientInformationView,
         name='add-customer-document'),
    path('remove-customer-document', views.RemoveClinetInformationView,
         name='remove-customer-document'),

    # inventory row htmx
    path('add-document-item', views.AddDocumentItemsView,
         name='add-document-item'),
    path('update-item-qty', views.UpdateDocumentItemQty,
         name='update-item-qty'),
    path('remove-document-item', views.RemoveDocumentItemView,
         name='remove-document-item'),

    # services row htmx
    path('add-document-service', views.AddServiceDocumentView,
         name='add-document-service'),
    path('remove-document-service', views.RemoveDocumentServiceView,
         name='remove-document-service'),
    path('update-service-qty', views.UpdateDocumentService,
         name='update-service-qty'),
]
