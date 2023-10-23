from django.shortcuts import render, redirect
from .models import *
from client.models import *
from transactions.models import *
from customers.models import *

from django.contrib import messages
import random
from django.db.models import Q
from django.db.models import F, Sum
from django.db.models import F, Value, IntegerField
import datetime

# Create your views here.


def CustomersView(request):
    clients = CustomerModel.objects.all().order_by('-date_created')

    context = {
        "clients": clients
    }
    return render(request, 'customers/customers_list.html', context)


def CustomerDetailsView(request, id):
    client = CustomerModel.objects.get(id=id)
    invoices = TransactionModel.objects.filter(
        Q(transactionMethod="Invoice") & Q(customer=client)).order_by('-date_created')
    invoicesCount = TransactionModel.objects.filter(
        Q(transactionMethod="Invoice") & Q(customer=client)).count()
    sales = TransactionModel.objects.filter(
        Q(transactionMethod="Sale") & Q(customer=client))
    qoutes = TransactionModel.objects.filter(
        Q(transactionMethod="Qoute") & Q(customer=client)).order_by('-date_created')
    qoutesCount = TransactionModel.objects.filter(
        Q(transactionMethod="Qoute") & Q(customer=client)).count()

    balance = float(0)
    for i in invoices:
        if i.outstandingBalance != None:
            balance = float(
                balance) + float(i.outstandingBalance)

    # sales income
    salesIncome = 0
    for i in sales:
        income = i.income
        salesIncome = salesIncome + income

    # company logo
    if request.method == 'POST' and 'submit_logo' in request.POST:
        client_logo = request.FILES['client_logo']
        client.logo = client_logo
        client.save()
        messages.success(request, 'Logo Updated')
        return redirect('client-details', id)

    # company bank submit
    if request.method == 'POST' and 'submit_bank' in request.POST:
        createBank = BankModel()
        createBank.bankName = request.POST.get('bank')
        createBank.branch = request.POST.get('branch')
        createBank.account = request.POST.get('account')
        createBank.save()

        # update Company Profile
        client.bank = createBank
        client.save()

        messages.success(request, 'Bank details updated')
        return redirect('client-details', id)

    context = {
        "client": client,
        "invoices": invoices,
        "invoicesCount": invoicesCount,
        "sales": sales,
        "salesIncome": salesIncome,
        "qoutes": qoutes,
        "qoutesCount": qoutesCount,
        "balance": balance
    }
    return render(request, 'customers/view_client.html', context)


def AddCustomerView(request):
    if request.method == 'POST' and 'submit_client' in request.POST:
        current_date = datetime.date.today()
        # save address
        saveAdress = AddressModel()
        saveAdress.street = request.POST.get('street')
        saveAdress.suburb = request.POST.get('Suburb')
        saveAdress.city = request.POST.get('city')
        saveAdress.province = request.POST.get('province')
        saveAdress.pobox = request.POST.get('pobox')
        saveAdress.save()

        # save client
        saveClient = CustomerModel()
        saveClient.ref = random.randrange(0, 10000000)
        saveClient.firstName = request.POST.get('FirstName')
        saveClient.lastName = request.POST.get('lastName')
        saveClient.phone = request.POST.get('PhoneNumber')
        saveClient.email = request.POST.get('email')
        saveClient.company_name = request.POST.get('companyName')
        saveClient.company_registered_number = request.POST.get(
            'companyNumber')
        saveClient.company_tax_number = request.POST.get('companyTax')
        saveClient.address = saveAdress
        saveClient.month = current_date.strftime("%B")
        saveClient.year = current_date.year
        saveClient.save()
        messages.success(request, 'New Client Added')
        return redirect('customers')

    return render(request, 'customers/add_customer.html')


# Customer Transactions
def InvoicesCustomerView(request, id, method=None):
    if method == 1:
        methodtype = "Invoice"
        ref_number = random.randrange(10000, 1000000)
        ref = 'IN' + str(ref_number)
        companyRef = "CO98364"
        company = ProfileModel.objects.get(ref=companyRef)
        clients = CustomerModel.objects.all().order_by('-date_created')
        inventory = InventoryModel.objects.all()
        services = ServicesModel.objects.all()
        clientProfile = CustomerModel.objects.get(id=id)
        subtotal = 0
        total_due = 0

        user = UserModel.objects.get(userRef="7636387")
        documents = DocumentModel.objects.filter(beanUser=user)
        inventoryItems = documents.filter(
            Q(documentType="Inventory") | Q(documentType="Service"))

        if inventoryItems:
            for i in inventoryItems:
                i.delete()

        if request.method == 'POST' and 'submit_invoice' in request.POST:
            document_qty = 0
            total_income = float(0)
            # Calculate GrandTotal and Quantity
            for i in inventoryItems:
                total_income = total_income + float(i.total)
                document_qty = document_qty + 1

            # create a document transaction invoice
            saveTransaction = TransactionModel()
            saveTransaction.ref = request.POST.get('ref')
            saveTransaction.transactionMethod = 'Invoice'
            saveTransaction.customer = clientProfile
            saveTransaction.quantity = document_qty
            saveTransaction.income = total_income
            saveTransaction.company = company
            saveTransaction.notes = request.POST.get('notes')
            saveTransaction.issueDate = request.POST.get('issueDate')
            saveTransaction.outstandingBalance = total_income
            dueDate = request.POST.get('dueDate')
            if dueDate:
                saveTransaction.dueDate = request.POST.get('dueDate')
            saveTransaction.save()

            # save documents to invoice document model
            for i in inventoryItems:
                if i.documentType == 'Inventory':
                    # Get the current date
                    current_date = datetime.date.today()
                    createInventoryDoc = InvoiceDocumentsModel()
                    createInventoryDoc.docuemntType = "Inventory"
                    createInventoryDoc.inventory = i.item
                    createInventoryDoc.documentQuantity = i.quantity
                    createInventoryDoc.documentTotal = i.total
                    createInventoryDoc.documentMonth = current_date.strftime(
                        "%B")
                    createInventoryDoc.documentYear = current_date.year
                    createInventoryDoc.method = "Invoice"
                    createInventoryDoc.save()
                    saveTransaction.transactionDocuments.add(
                        createInventoryDoc)
                elif i.documentType == 'Service':
                    # Get the current date
                    current_date = datetime.date.today()
                    createServiceDoc = InvoiceDocumentsModel()
                    createServiceDoc.docuemntType = "Service"
                    createServiceDoc.service = i.services
                    createServiceDoc.documentQuantity = i.quantity
                    createServiceDoc.documentTotal = i.total
                    createServiceDoc.documentMonth = current_date.strftime(
                        "%B")
                    createServiceDoc.documentYear = current_date.year
                    createServiceDoc.method = "Invoice"
                    createServiceDoc.save()
                    saveTransaction.transactionDocuments.add(createServiceDoc)

            return redirect('view-document', saveTransaction.id, 1)

        context = {
            "ref": ref,
            "company": company,
            "clients": clients,
            "inventory": inventory,
            "services": services,
            "clientProfile": clientProfile,
            "subtotal": subtotal,
            "total_due": total_due,
            "methodtype": methodtype
        }
        return render(request, 'customerTransactions/invoicesCustomer.html', context)
    elif method == 2:
        methodtype = "Qoute"
        user = UserModel.objects.get(userRef="7636387")
        ref_number = random.randrange(10000, 1000000)
        ref = 'QT' + str(ref_number)
        companyRef = "CO98364"
        company = ProfileModel.objects.get(ref=companyRef)
        clients = CustomerModel.objects.all().order_by('-date_created')
        inventory = InventoryModel.objects.all()
        services = ServicesModel.objects.all()
        clientProfile = CustomerModel.objects.get(id=id)
        subtotal = 0
        total_due = 0

        documents = DocumentModel.objects.filter(beanUser=user)
        inventoryItems = documents.filter(
            Q(documentType="Inventory") | Q(documentType="Service"))

        if inventoryItems:
            for i in inventoryItems:
                i.delete()

        if request.method == 'POST' and 'submit_qoute' in request.POST:
            clientID = request.POST.get('customerID')
            clientProfile = CustomerModel.objects.get(id=clientID)
            document_qty = 0
            total_income = float(0)
            # Calculate GrandTotal and Quantity
            for i in inventoryItems:
                total_income = total_income + float(i.total)
                document_qty = document_qty + 1

            # create new qoute transaction
            transactionQoute = TransactionModel()
            transactionQoute.ref = request.POST.get('ref')
            transactionQoute.transactionMethod = "Qoute"
            transactionQoute.company = company
            transactionQoute.customer = clientProfile
            transactionQoute.income = total_income
            transactionQoute.quantity = document_qty
            transactionQoute.notes = request.POST.get('notes')
            transactionQoute.issueDate = request.POST.get('issueDate')
            dueDate = request.POST.get('dueDate')
            if dueDate:
                transactionQoute.dueDate = request.POST.get('dueDate')
            transactionQoute.save()

            # save documents to invoice document model
            for i in inventoryItems:
                if i.documentType == 'Inventory':
                    # Get the current date
                    current_date = datetime.date.today()
                    createInventoryDoc = InvoiceDocumentsModel()
                    createInventoryDoc.docuemntType = "Inventory"
                    createInventoryDoc.inventory = i.item
                    createInventoryDoc.documentQuantity = i.quantity
                    createInventoryDoc.documentTotal = i.total
                    createInventoryDoc.documentMonth = current_date.strftime(
                        "%B")
                    createInventoryDoc.documentYear = current_date.year
                    createInventoryDoc.method = "Qoute"
                    createInventoryDoc.save()
                    transactionQoute.transactionDocuments.add(
                        createInventoryDoc)
                elif i.documentType == 'Service':
                    # Get the current date
                    current_date = datetime.date.today()
                    createServiceDoc = InvoiceDocumentsModel()
                    createServiceDoc.docuemntType = "Service"
                    createServiceDoc.service = i.services
                    createServiceDoc.documentQuantity = i.quantity
                    createServiceDoc.documentTotal = i.total
                    createServiceDoc.documentMonth = current_date.strftime(
                        "%B")
                    createServiceDoc.documentYear = current_date.year
                    createServiceDoc.method = "Qoute"
                    createServiceDoc.save()
                    transactionQoute.transactionDocuments.add(createServiceDoc)

            return redirect('view-document', transactionQoute.id, 2)

        context = {
            "methodtype": methodtype,
            "ref": ref,
            "company": company,
            "clients": clients,
            "inventory": inventory,
            "services": services,
            "clientProfile": clientProfile,
            "subtotal": subtotal,
            "total_due": total_due,
        }

        return render(request, 'customerTransactions/invoicesCustomer.html', context)

# Remove Company details htmx


def RemoveCompanyDetailsView(request):
    company = {}

    if request.method == 'POST':
        company = {}

    context = {
        "company": company
    }
    return render(request, 'documentForm/documentFrom.html', context)

# Add Company details htmx


def AddCompanyDetailsView(request):
    company = {}

    if request.method == 'POST':
        companyRef = "CO98364"
        company = ProfileModel.objects.get(ref=companyRef)

    context = {
        "company": company
    }
    return render(request, 'documentForm/documentFrom.html', context)

# client htmx views start


def AddClientInformationView(request):
    clientProfile = {}

    if request.method == 'POST':
        clientID = request.POST.get('clientID')
        clientProfile = CustomerModel.objects.get(id=clientID)

    context = {
        "clientProfile": clientProfile
    }

    return render(request, 'documentForm/documentTo.html', context)


def RemoveClinetInformationView(request):
    if request.method == 'POST':
        clientProfile = {}

    context = {
        "clientProfile": clientProfile
    }
    return render(request, 'documentForm/documentTo.html', context)


# Inventory Document items htmx
def AddDocumentItemsView(request):
    if request.method == 'POST':
        user = UserModel.objects.get(userRef="7636387")
        selected_items = request.POST.getlist('inventoryItem')
        userItems = InventoryModel.objects.filter(id__in=selected_items)

        for i in userItems:
            existObjects = DocumentModel.objects.filter(
                item=i).exists()
            if existObjects:
                pass
            else:
                addItem = DocumentModel()
                addItem.beanUser = user
                addItem.documentType = "Inventory"
                addItem.item = i
                addItem.quantity = 1
                addItem.total = i.sellingprice
                addItem.save()

        documents = DocumentModel.objects.filter(beanUser=user)
        inventoryItems = documents.filter(
            Q(documentType="Inventory") | Q(documentType="Service"))
        subtotal = 0
        total_due = 0

        for i in inventoryItems:
            subtotal = subtotal + float(i.total)
            total_due = total_due + float(i.total)

    context = {
        "inventoryItems": inventoryItems,
        "subtotal": subtotal,
        "total_due": total_due,
    }

    return render(request, 'partials/documentTableRow.html', context)


def UpdateDocumentItemQty(request):
    if request.method == 'POST':
        user = UserModel.objects.get(userRef="7636387")
        quantityUpdate = request.POST.get('quantityUpdate')
        itemID = request.POST.get('itemID')

        if quantityUpdate:
            quantity = float(quantityUpdate)
            updateItem = DocumentModel.objects.get(id=itemID)
            updateItem.quantity = quantityUpdate
            updateItem.total = float(updateItem.item.sellingprice) * quantity
            updateItem.save()

            documents = DocumentModel.objects.filter(beanUser=user)
            inventoryItems = documents.filter(
                Q(documentType="Inventory") | Q(documentType="Service"))

            subtotal = 0
            total_due = 0

            for i in inventoryItems:
                subtotal = subtotal + float(i.total)
                total_due = total_due + float(i.total)

            context = {
                "inventoryItems": inventoryItems,
                "subtotal": subtotal,
                "total_due": total_due
            }

        else:
            saveItem = DocumentModel.objects.get(id=itemID)
            saveItem.quantity = None
            saveItem.total = 0
            saveItem.save()

            documents = DocumentModel.objects.filter(beanUser=user)
            inventoryItems = documents.filter(
                Q(documentType="Inventory") | Q(documentType="Service"))

            subtotal = 0
            total_due = 0

            for i in inventoryItems:
                subtotal = subtotal + float(i.total)
                total_due = total_due + float(i.total)

            context = {
                "inventoryItems": inventoryItems,
                "subtotal": subtotal,
                "total_due ": total_due,
            }

    return render(request, 'partials/documentTableRow.html', context)


def RemoveDocumentItemView(request):
    user = UserModel.objects.get(userRef="7636387")
    if request.method == 'POST':
        itemID = request.POST.get('itemID')
        removeItem = DocumentModel.objects.get(id=itemID)
        removeItem.delete()

        documents = DocumentModel.objects.filter(beanUser=user)
        inventoryItems = documents.filter(
            Q(documentType="Inventory") | Q(documentType="Service"))

        subtotal = 0
        total_due = 0

        for i in inventoryItems:
            subtotal = subtotal + float(i.total)
            total_due = total_due + float(i.total)

    context = {
        "inventoryItems": inventoryItems,
        "subtotal": subtotal,
        "total_due": total_due
    }
    return render(request, 'partials/documentTableRow.html', context)


# Service Document Views HTMX
def AddServiceDocumentView(request):

    if request.method == "POST":
        user = UserModel.objects.get(userRef="7636387")
        selected_services = request.POST.getlist('inventoryItem')
        services = ServicesModel.objects.filter(id__in=selected_services)

        for i in services:
            existObjects = DocumentModel.objects.filter(
                services=i).exists()
            if existObjects:
                pass
            else:
                addItem = DocumentModel()
                addItem.beanUser = user
                addItem.documentType = "Service"
                addItem.services = i
                addItem.quantity = 1
                addItem.total = i.serviceFee
                addItem.save()

    documents = DocumentModel.objects.filter(beanUser=user)
    inventoryItems = documents.filter(
        Q(documentType="Inventory") | Q(documentType="Service"))

    subtotal = 0
    total_due = 0

    for i in inventoryItems:
        subtotal = subtotal + float(i.total)
        total_due = total_due + float(i.total)

    context = {
        "inventoryItems": inventoryItems,
        "subtotal": subtotal,
        "total_due": total_due
    }

    return render(request, 'partials/documentTableRow.html', context)


def RemoveDocumentServiceView(request):
    user = UserModel.objects.get(userRef="7636387")
    if request.method == 'POST':
        itemID = request.POST.get('itemID')
        removeItem = DocumentModel.objects.get(id=itemID)
        removeItem.delete()

        documents = DocumentModel.objects.filter(beanUser=user)
        inventoryItems = documents.filter(
            Q(documentType="Inventory") | Q(documentType="Service"))

        subtotal = 0
        total_due = 0

        for i in inventoryItems:
            subtotal = subtotal + float(i.total)
            total_due = total_due + float(i.total)

    context = {
        "inventoryItems": inventoryItems,
        "subtotal": subtotal,
        "total_due": total_due
    }
    return render(request, 'partials/documentTableRow.html', context)


def UpdateDocumentService(request):
    if request.method == 'POST':
        user = UserModel.objects.get(userRef="7636387")
        quantityUpdate = request.POST.get('quantityUpdate')
        itemID = request.POST.get('itemID')

        if quantityUpdate:
            quantity = float(quantityUpdate)
            updateItem = DocumentModel.objects.get(id=itemID)
            updateItem.quantity = quantityUpdate
            updateItem.total = float(updateItem.services.serviceFee) * quantity
            updateItem.save()

            documents = DocumentModel.objects.filter(beanUser=user)
            inventoryItems = documents.filter(
                Q(documentType="Inventory") | Q(documentType="Service"))

            subtotal = 0
            total_due = 0

            for i in inventoryItems:
                subtotal = subtotal + float(i.total)
                total_due = total_due + float(i.total)

            context = {
                "inventoryItems": inventoryItems,
                "subtotal": subtotal,
                "total_due": total_due
            }

        else:
            saveItem = DocumentModel.objects.get(id=itemID)
            saveItem.quantity = None
            saveItem.total = 0
            saveItem.save()

            documents = DocumentModel.objects.filter(beanUser=user)
            inventoryItems = documents.filter(
                Q(documentType="Inventory") | Q(documentType="Service"))

            subtotal = 0
            total_due = 0

            for i in inventoryItems:
                subtotal = subtotal + float(i.total)
                total_due = total_due + float(i.total)

            context = {
                "inventoryItems": inventoryItems,
                "subtotal": subtotal,
                "total_due": total_due
            }

    return render(request, 'partials/documentTableRow.html', context)
