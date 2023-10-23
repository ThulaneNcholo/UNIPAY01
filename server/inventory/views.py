from django.shortcuts import render, redirect
from .models import *
import random
from django.contrib import messages
from transactions.models import *
from django.utils import timezone
from datetime import timedelta
import datetime
from django.db.models import Q
import json

# Create your views here.


def listInventoryView(request):
    categories = CategoryModel.objects.all().order_by('-date_created')
    inventory = InventoryModel.objects.all().order_by('-date_created')
    inventoryCount = InventoryModel.objects.all().count()
    services = ServicesModel.objects.all().order_by('-date_created')
    servicesCount = ServicesModel.objects.all().count()

    # check for low stock inventory
    lowStock = 0
    outStock = 0
    for i in inventory:
        restockNumber = i.restocklevel
        quantity = i.quantity
        # low stock
        if quantity < restockNumber:
            lowStock = lowStock + 1
        # out of stock
        if quantity <= 0:
            outStock = outStock + 1

    context = {
        "categories": categories,
        "inventory": inventory,
        "services": services,
        "inventoryCount": inventoryCount,
        "servicesCount": servicesCount,
        "lowStock": lowStock,
        "outStock": outStock,
    }
    return render(request, 'inventory/list_inventory.html', context)


def AddInventoryView(request):
    ref_number = random.randrange(10000, 1000000)
    ref = 'IN' + str(ref_number)
    categories = CategoryModel.objects.all().order_by('-date_created')

    if request.method == 'POST' and 'add_inventory' in request.POST:
        categoryID = request.POST.get('category')
        categoryProfile = CategoryModel.objects.get(id=categoryID)

        addInventory = InventoryModel()
        addInventory.ref = request.POST.get('Referrance')
        addInventory.name = request.POST.get('itemName')
        addInventory.restocklevel = request.POST.get('lowStock')
        addInventory.unitprice = request.POST.get('UnitPrice')
        addInventory.sellingprice = request.POST.get('SellingPrice')
        addInventory.description = request.POST.get('description')
        addInventory.category = categoryProfile

        # Quantity
        qty_type = request.POST.get('qty_type')

        if qty_type == 'single':
            addInventory.quantity = request.POST.get('Quantity')
        elif qty_type == 'bulk':
            bulkQuantity = request.POST.get('bulkQuantity')
            boxQty = request.POST.get('boxQty')
            bulkQuantity = int(bulkQuantity) * int(boxQty)
            addInventory.quantity = bulkQuantity

        # save inventory
        addInventory.save()
        messages.success(request, 'new inventory item added')
        return redirect('list-inventory')

    context = {
        "ref": ref,
        "categories": categories
    }

    return render(request, 'inventory/add_inventory.html', context)


def InventoryDetailsView(request, id):
    item = InventoryModel.objects.get(id=id)
    transactions = TransactionModel.objects.filter(
        transactionDocuments__inventory=item).order_by('-date_created')

    # stock total
    stockTotal = float(item.sellingprice) * float(item.quantity)

    soldQuantity = 0
    soldStockTotal = 0
    for i in transactions:
        qty = i.quantity
        soldQuantity = int(soldQuantity) + int(qty)

    soldStockTotal = float(item.sellingprice) * soldQuantity
    unitfee = float(item.unitprice) * soldQuantity
    profit = float(soldStockTotal) - float(unitfee)

    context = {
        "item": item,
        "transactions": transactions,
        "soldQuantity": soldQuantity,
        "stockTotal": stockTotal,
        "soldStockTotal": soldStockTotal,
        "profit": profit
    }
    return render(request, 'inventory/inventory_view.html', context)


def AddServiceView(request):
    ref_number = random.randrange(10000, 1000000)
    ref = 'SV' + str(ref_number)
    categories = CategoryModel.objects.all().order_by('-date_created')

    if request.method == 'POST' and 'add_service' in request.POST:
        addService = ServicesModel()
        addService.ref = request.POST.get('Referrance')
        addService.name = request.POST.get('serviceName')
        addService.description = request.POST.get('description')
        addService.serviceFee = request.POST.get('price')
        categoryID = request.POST.get('category')
        categoryProfile = CategoryModel.objects.get(id=categoryID)
        addService.category = categoryProfile
        addService.save()
        messages.success(request, 'new service added')
        return redirect('list-inventory')

    context = {
        "ref": ref,
        "categories": categories
    }

    return render(request, 'inventory/add_service.html', context)


def ServiceDetailsView(request, id):
    # Get the current date
    current_date = datetime.date.today()
    current_year = current_date.year
    service = ServicesModel.objects.get(id=id)
    documents = InvoiceDocumentsModel.objects.filter(
        Q(service=service) & Q(documentYear=current_year)).order_by('-date_created')

    income = float(0)

    barChart = []

    for i in documents:
        income = float(i.documentTotal) + income
        month_exists = False
        for data in barChart:
            if data['month'] == i.documentMonth:
                data['total'] += float(i.documentTotal)
                month_exists = True
                break
        if not month_exists:
            barChart_data = {
                'month': i.documentMonth,
                'total': float(i.documentTotal),
            }
            barChart.append(barChart_data)

    # Convert the month names to numerical values for sorting
    month_names = [
        "January", "February", "March", "April",
        "May", "June", "July", "August",
        "September", "October", "November", "December"
    ]

    def get_month_numerical_value(month_name):
        return month_names.index(month_name) + 1

    # Sort the barChart data chronologically
    barChart.sort(key=lambda x: get_month_numerical_value(x['month']))

    # Convert the sorted data to JSON
    barChart_json = json.dumps(barChart)

    context = {
        "service": service,
        "documents": documents,
        "barChart_json": barChart_json,
        "income": income
    }
    return render(request, 'servicesfolder/service_view.html', context)

# HTMX VIEWS


def AddCategoryView(request):
    categories = CategoryModel.objects.all().order_by('-date_created')

    if request.method == 'POST':
        name = request.POST.get('categoryName')

        if name != 'none':
            saveCategory = CategoryModel()
            saveCategory.name = request.POST.get('categoryName')
            saveCategory.save()
        else:
            print('none')

    categories = CategoryModel.objects.all().order_by('-date_created')

    context = {
        "categories": categories
    }

    return render(request, 'partials/category_list.html', context)


def DeleteCategoryView(request):

    if request.method == 'POST':
        categoryID = request.POST.get('categoryID')

        deleteCategory = CategoryModel.objects.get(id=categoryID)
        deleteCategory.delete()

    categories = CategoryModel.objects.all().order_by('-date_created')

    context = {
        "categories": categories
    }

    return render(request, 'partials/category_list.html', context)


# Services Views start
def ServiceSaleView(request, id):
    service = ServicesModel.objects.get(id=id)
    ref_number = random.randrange(10000, 1000000)
    ref = 'SL' + str(ref_number)
    customers = CustomerModel.objects.all().order_by('-date_created')

    if request.method == 'POST' and 'submit_sale' in request.POST:
        sale_service = service
        reference = request.POST.get('reference')
        quantity = request.POST.get('quantity')
        customerID = request.POST.get('customerID')
        customerProfile = CustomerModel.objects.get(id=customerID)
        companyRef = "CO98364"
        company = ProfileModel.objects.get(ref=companyRef)

        # create Transaction document
        saveDocument = InvoiceDocumentsModel()
        current_date = datetime.date.today()
        saveDocument.method = "Sale"
        saveDocument.service = service
        saveDocument.documentQuantity = quantity
        saveDocument.documentTotal = float(
            service.serviceFee) * float(quantity)
        saveDocument.documentMonth = current_date.strftime(
            "%B")
        saveDocument.documentYear = current_date.year
        saveDocument.save()

        addServiceSale = TransactionModel()
        addServiceSale.transactionMethod = "Sale"
        addServiceSale.ref = reference
        addServiceSale.customer = customerProfile
        addServiceSale.company = company
        addServiceSale.quantity = quantity
        addServiceSale.income = float(service.serviceFee) * float(quantity)
        addServiceSale.save()
        addServiceSale.transactionDocuments.add(saveDocument)

    context = {
        "service": service,
        "ref": ref,
        "customers": customers
    }
    return render(request, 'servicesfolder/service_sale.html', context)


def clientAddressHtmx(request):
    if request.method == 'POST':
        customerID = request.POST.get('customerID')
        client = CustomerModel.objects.get(id=customerID)

        context = {
            "client": client
        }

    return render(request, 'partials/address_partial.html', context)


def ServiceDocumentView(request, id, method=None):
    # invoice
    if method == 1:
        methodtype = "Invoice"
        companyRef = "CO98364"
        company = ProfileModel.objects.get(ref=companyRef)
        ref_number = random.randrange(10000, 1000000)
        ref = 'IN' + str(ref_number)
        clients = CustomerModel.objects.all()

        context = {
            "methodtype": methodtype,
            "company": company,
            "ref": ref,
            "clients": clients,
        }
        return render(request, 'servicesfolder/serviceDocument.html', context)
    # qoutation
    elif method == 2:
        methodtype = "Qoute"
        companyRef = "CO98364"
        company = ProfileModel.objects.get(ref=companyRef)
        ref_number = random.randrange(10000, 1000000)
        ref = 'QT' + str(ref_number)
        clients = CustomerModel.objects.all()

        context = {
            "methodtype": methodtype,
            "company": company,
            "ref": ref,
            "clients": clients,
        }

        return render(request, 'servicesfolder/serviceDocument.html', context)
