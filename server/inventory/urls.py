
from django.urls import path
from .import views

urlpatterns = [
    path('list-inventory', views.listInventoryView, name='list-inventory'),
    path('add-inventory', views.AddInventoryView, name='add-inventory'),
    path('inventory-view/<int:id>',
         views.InventoryDetailsView, name='inventory-view'),
    path('add-service', views.AddServiceView, name='add-service'),
    path('service-view/<int:id>',
         views.ServiceDetailsView, name='service-view'),

    # HTMX URLS
    path('add-category', views.AddCategoryView, name='add-category'),
    path('delete-category',
         views.DeleteCategoryView, name='delete-category'),

    # Service views urls
    path('service-sale/<int:id>',
         views.ServiceSaleView, name='service-sale'),
    path('client-address',
         views.clientAddressHtmx, name='client-address'),
    path('service-document/<int:id>/<int:method>',
         views.ServiceDocumentView, name='service-document'),

]
