from django.shortcuts import render, redirect
from .models import *
from inventory.models import *
from customers.models import *
from client.models import AddressModel
import random
from django.contrib import messages
import datetime
from company.models import *
from django.utils import timezone
from django.db.models import Q

# Create your views here.

# *********** Inventory Views ***********


def InventorySaleView(request, id):
    item = InventoryModel.objects.get(id=id)
    itemPrice = item.sellingprice
    customers = CustomerModel.objects.all().order_by('-date_created')

    ref_number = random.randrange(10000, 1000000)
    ref = 'SL' + str(ref_number)

    if request.method == 'POST' and 'submit_sale' in request.POST:
        addSale = TransactionModel()
        addSale.item = item
        addSale.ref = request.POST.get('reference')
        addSale.transactionMethod = 'Sale'

        # check if theres a customer selected
        customerID = request.POST.get('customerID')
        if customerID != 'none':
            customerProfile = CustomerModel.objects.get(id=customerID)
            addSale.customer = customerProfile

        # check if theres a discount
        discount = request.POST.get('discount')

        # check quantity type single or bulk sale
        qty_type = request.POST.get('qty_type')
        if qty_type == 'single':
            addSale.quantity = request.POST.get('Quantity')
            total = float(itemPrice) * float(addSale.quantity)
            if discount != '0':
                discountNumber = float(discount)
                discountPrice = total * (discountNumber / 100)
                addSale.discounted_price = discountPrice
                addSale.discount = discountNumber
                # income
                addSale.income = float(total) - float(discountPrice)
            else:
                addSale.income = total

        elif qty_type == 'bulk':
            bulkQuantity = request.POST.get('bulkQuantity')
            boxQty = request.POST.get('boxQty')
            addSale.quantity = int(bulkQuantity) * int(boxQty)
            total = float(itemPrice) * float(addSale.quantity)
            if discount != '0':
                discountNumber = float(discount)
                discountPrice = total * (discountNumber / 100)
                addSale.discounted_price = discountPrice
                addSale.discount = discountNumber
                # income
                addSale.income = float(total) - float(discountPrice)
            else:
                addSale.income = total

        # check if attacted address
        addressValue = request.POST.get('addressValue')
        if addressValue == 'Yes':
            addAddress = AddressModel()
            addAddress.street = request.POST.get('street')
            addAddress.suburb = request.POST.get('Suburb')
            addAddress.city = request.POST.get('city')
            addAddress.province = request.POST.get('province')
            addAddress.pobox = request.POST.get('pobox')
            addAddress.save()

            # save to transaction model
            addSale.addressStatus = 'Yes'
            addSale.address = addAddress
            addSale.fullName = request.POST.get('fullName')
            addSale.phone = request.POST.get('PhoneNumber')

        addSale.save()
        addSale.transactionStatus = 'Complete'
        addSale.save()

        # update inventory object from database
        updateInventory = InventoryModel.objects.get(id=item.id)
        updateInventory.quantity = int(
            updateInventory.quantity) - int(addSale.quantity)
        updateInventory.save()

        messages.success(request, 'new Sale transcation created')
        return redirect('transaction-success', addSale.id)

    context = {
        "item": item,
        "customers": customers,
        "ref": ref,
    }

    return render(request, 'inventoryTrans/inventorySale.html', context)


def InventoryInvoiceView(request, id, method=None):
    if method == 1:

        clientValue = 'No'
        companyValue = 'No'
        bankValue = 'No'
        methodtype = 'Invoice'

        # new transaction view
        ref_number = random.randrange(10000, 1000000)
        ref = 'IN' + str(ref_number)
        companyRef = "CO98364"
        company = ProfileModel.objects.get(ref=companyRef)
        bankData = company.bank
        clients = CustomerModel.objects.all()
        item = InventoryModel.objects.get(id=id)

        if request.method == 'POST' and 'submit_invoice' in request.POST:
            customerID = request.POST.get('customerID')
            quantity = request.POST.get('itemQuantity')
            dueDate = request.POST.get('dueDate')

            # create Invoice Document start
            current_date = datetime.date.today()
            saveDocument = InvoiceDocumentsModel()
            saveDocument.docuemntType = "Inventory"
            saveDocument.inventory = item
            saveDocument.documentQuantity = quantity
            saveDocument.documentTotal = float(
                item.sellingprice) * float(quantity)
            saveDocument.documentMonth = current_date.strftime("%B")
            saveDocument.documentYear = current_date.year
            saveDocument.method = "Invoice"
            saveDocument.save()

            # create Transaction Document start
            createInvoice = TransactionModel()
            createInvoice.ref = request.POST.get('ref')
            createInvoice.transactionMethod = "Invoice"
            createInvoice.company = company

            if customerID != '':
                clinetProfile = CustomerModel.objects.get(id=customerID)
                createInvoice.customer = clinetProfile
            createInvoice.quantity = quantity
            createInvoice.notes = request.POST.get('notes')
            createInvoice.income = saveDocument.documentTotal
            createInvoice.outstandingBalance = saveDocument.documentTotal
            createInvoice.issueDate = request.POST.get('issueDate')
            if dueDate:
                createInvoice.dueDate = dueDate
            createInvoice.save()
            createInvoice.transactionDocuments.add(saveDocument)

            # update item quantity
            updateInventory = InventoryModel.objects.get(id=id)
            updateInventory.quantity = int(
                updateInventory.quantity) - int(quantity)
            updateInventory.save()

            return redirect('view-document', createInvoice.id, 1)

        context = {
            "companyData": company,
            "bankData": bankData,
            "clients": clients,
            "item": item,
            "ref": ref,
            "clientValue": clientValue,
            "companyValue": companyValue,
            "bankValue": bankValue,
            "methodtype": methodtype
        }
        return render(request, 'inventoryTrans/inventoryInvoice.html', context)

    elif method == 2:
        methodtype = "Qoute"
        companyRef = "CO98364"
        companyData = ProfileModel.objects.get(ref=companyRef)
        bankData = companyData.bank
        ref_number = random.randrange(10000, 1000000)
        ref = 'QT' + str(ref_number)
        clients = CustomerModel.objects.all()
        item = InventoryModel.objects.get(id=id)

        if request.method == 'POST' and 'submit_qoute' in request.POST:
            customerID = request.POST.get('customerID')

            quantity = request.POST.get('itemQuantity')
            dueDate = request.POST.get('dueDate')

            # create Invoice Document start
            current_date = datetime.date.today()
            saveDocument = InvoiceDocumentsModel()
            saveDocument.docuemntType = "Inventory"
            saveDocument.inventory = item
            saveDocument.documentQuantity = quantity
            saveDocument.documentTotal = float(
                item.sellingprice) * float(quantity)
            saveDocument.documentMonth = current_date.strftime("%B")
            saveDocument.documentYear = current_date.year
            saveDocument.save()

            # create Transaction Document start
            createInvoice = TransactionModel()
            createInvoice.ref = request.POST.get('ref')
            createInvoice.transactionMethod = "Qoute"
            createInvoice.company = companyData
            if customerID != '':
                clinetProfile = CustomerModel.objects.get(id=customerID)
                createInvoice.customer = clinetProfile
            createInvoice.quantity = quantity
            createInvoice.notes = request.POST.get('notes')
            createInvoice.income = saveDocument.documentTotal
            createInvoice.issueDate = request.POST.get('issueDate')
            if dueDate:
                createInvoice.dueDate = dueDate
            createInvoice.save()
            createInvoice.transactionDocuments.add(saveDocument)

            # update item quantity
            updateInventory = InventoryModel.objects.get(id=id)
            updateInventory.quantity = int(
                updateInventory.quantity) - int(quantity)
            updateInventory.save()

            return redirect('view-document', createInvoice.id, 2)

        context = {
            "methodtype": methodtype,
            "companyData": companyData,
            "bankData": bankData,
            "ref": ref,
            "clients": clients,
            "item": item
        }

        return render(request, 'inventoryTrans/inventoryInvoice.html', context)


# htmx client data
def CompanyDataView(request):
    companyData = {}
    companyValue = 'No'

    if request.method == 'POST':
        companyValue = 'Yes'
        companyID = request.POST.get('companyID')
        companyData = ProfileModel.objects.get(ref=companyID)

    context = {
        "companyData": companyData,
        "companyValue": companyValue
    }

    return render(request, 'partials/invoiceCompanyData.html', context)


def CompanyBankView(request):
    bankData = {}
    bankValue = 'No'

    if request.method == 'POST':
        bankValue = 'Yes'
        companyBank = request.POST.get('companyBank')
        bankData = BankModel.objects.get(id=companyBank)

    context = {
        "bankData": bankData,
        "bankValue": bankValue
    }
    return render(request, 'partials/invoiceBank.html', context)


def ClientDataView(request):
    client = {}
    clientValue = 'No'

    if request.method == 'POST':
        clientValue = 'Yes'
        clientID = request.POST.get('clientID')
        client = CustomerModel.objects.get(id=clientID)

    context = {
        "client": client,
        "clientValue": clientValue
    }

    return render(request, 'partials/invoiceClientDetails.html', context)


# *********** Service Views ***********


# *********** Transaction Success or Fail ***********
def SuccessTransactionView(request, id):
    transaction = TransactionModel.objects.get(id=id)
    addressValue = transaction.addressStatus

    context = {
        "transaction": transaction,
        "addressValue": addressValue,
    }
    return render(request, 'partials/transactionSucces.html', context)


# *********** view transaction documents ***********
def DocumentView(request, id, method=None):
    if method == 1:
        methodType = "Invoice"
        document = TransactionModel.objects.get(id=id)
        transactions = document.transactionDocuments.all()
        payments = document.payments.all()
        payment_total = float(0)

        for i in payments:
            payment_total = payment_total + float(i.paid)

        if request.method == 'POST' and 'submit_payment' in request.POST:
            # create Payment modal
            payment = request.POST.get('payment')
            paid = float(payment)
            addPayment = PaymentHistoryModel()
            addPayment.ref = document.ref
            addPayment.paid = paid
            addPayment.save()

            paid = document.amountPaid
            if paid != None:
                amountPaid = float(document.amountPaid) + \
                    float(addPayment.paid)
                # update invoice document
                updateDocument = TransactionModel.objects.get(id=id)
                updateDocument.payments.add(addPayment)
                updateDocument.amountPaid = amountPaid
                updateDocument.outstandingBalance = float(
                    document.income) - amountPaid
                updateDocument.save()
            else:
                amountPaid = float(0) + \
                    float(addPayment.paid)
                # update invoice document
                updateDocument = TransactionModel.objects.get(id=id)
                updateDocument.payments.add(addPayment)
                updateDocument.amountPaid = amountPaid
                updateDocument.outstandingBalance = float(
                    document.income) - amountPaid
                updateDocument.save()

            return redirect('view-document', id, 1)

        # Create Recurring invoice
        if request.method == 'POST' and 'submit_recurring' in request.POST:
            # create recurring transaction
            addRecurring = RecurringTransaction()
            addRecurring.recurrence_period = request.POST.get('selectedMonth')
            addRecurring.start_date = request.POST.get('selectedDate')
            addRecurring.save()

            # update Transaction document
            createRecurring = TransactionModel.objects.get(id=id)
            createRecurring.recurring_transaction = addRecurring
            createRecurring.save()

            return redirect('view-document', id, 1)

        context = {
            "methodType": methodType,
            "document": document,
            "transactions": transactions,
            "payment_total": payment_total,
            "payments": payments
        }
        return render(request, 'transactions/viewDocuments.html', context)
    elif method == 2:
        methodType = "Qoute"
        document = TransactionModel.objects.get(id=id)
        transactions = document.transactionDocuments.all()

        if request.method == 'POST' and 'convert_qoute' in request.POST:
            convertQoute = TransactionModel.objects.get(id=id)
            convertQoute.ref = convertQoute.ref.replace('QT', 'IN')
            convertQoute.transactionMethod = "Invoice"
            convertQoute.date_created = timezone.now()
            convertQoute.save()

            for i in transactions:
                updateDocimentItems = InvoiceDocumentsModel.objects.get(
                    id=i.id)
                updateDocimentItems.method = "Invoice"
                updateDocimentItems.save()

            return redirect('view-document', id, 1)

        context = {
            "methodType": methodType,
            "document": document,
            "transactions": transactions,
        }
        return render(request, 'transactions/viewDocuments.html', context)
    if method == 3:
        methodType = "Sale"
        document = TransactionModel.objects.get(id=id)
        transactions = document.transactionDocuments.all()

        context = {
            "methodType": methodType,
            "document": document,
            "transactions": transactions,
        }

        return render(request, 'transactions/viewDocuments.html', context)

# *********** All documents view ***********
# main transaction view create invoice and qoute


def MainTransactionView(request, method=None):
    companyRef = "CO98364"
    company = ProfileModel.objects.get(ref=companyRef)
    clients = CustomerModel.objects.all().order_by('-date_created')
    inventory = InventoryModel.objects.all().order_by('-date_created')
    services = ServicesModel.objects.all().order_by('-date_created')

    user = UserModel.objects.get(userRef="7636387")
    documents = DocumentModel.objects.filter(beanUser=user)
    inventoryItems = documents.filter(
        Q(documentType="Inventory") | Q(documentType="Service"))

    if inventoryItems:
        for i in inventoryItems:
            i.delete()

    if method == 1:
        methodtype = "Invoice"
        ref_number = random.randrange(10000, 1000000)
        ref = 'IN' + str(ref_number)

        if request.method == 'POST' and 'submit_invoice' in request.POST:
            customerID = request.POST.get('customerID')

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
            if customerID != '':
                customerProfile = CustomerModel.objects.get(id=customerID)
                saveTransaction.customer = customerProfile
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
            "methodtype": methodtype,
            "company": company,
            "clients": clients,
            "inventory": inventory,
            "services": services,
            "ref": ref,
        }

        return render(request, 'document/main_transaction.html', context)

    elif method == 2:
        methodtype = "Qoute"
        ref_number = random.randrange(10000, 1000000)
        ref = 'QT' + str(ref_number)

        if request.method == 'POST' and 'submit_qoute' in request.POST:
            clientID = request.POST.get('customerID')
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
            if clientID != '':
                customerProfile = CustomerModel.objects.get(id=clientID)
                transactionQoute.customer = customerProfile
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
            "company": company,
            "clients": clients,
            "inventory": inventory,
            "services": services,
            "ref": ref
        }

        return render(request, 'document/main_transaction.html', context)
    elif method == 3:
        methodtype = "Sale"
        ref_number = random.randrange(10000, 1000000)
        ref = 'SL' + str(ref_number)

        if request.method == 'POST' and 'submit_sale' in request.POST:
            clientID = request.POST.get('customerID')
            document_qty = 0
            total_income = float(0)
            # Calculate GrandTotal and Quantity
            for i in inventoryItems:
                total_income = total_income + float(i.total)
                document_qty = document_qty + 1

            # create new qoute transaction
            transactionQoute = TransactionModel()
            transactionQoute.ref = request.POST.get('ref')
            transactionQoute.transactionMethod = "Sale"
            transactionQoute.company = company
            if clientID != '':
                customerProfile = CustomerModel.objects.get(id=clientID)
                transactionQoute.customer = customerProfile
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
                    createInventoryDoc.method = "Sale"
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
                    createServiceDoc.method = "Sale"
                    createServiceDoc.save()
                    transactionQoute.transactionDocuments.add(createServiceDoc)

        context = {
            "methodtype": methodtype,
            "company": company,
            "clients": clients,
            "inventory": inventory,
            "services": services,
            "ref": ref
        }

        return render(request, 'document/main_transaction.html', context)


def ListSalesView(request):
    sales = TransactionModel.objects.filter(
        transactionMethod='Sale').order_by('-date_created')

    context = {
        "sales": sales
    }
    return render(request, 'document/list_sale.html', context)


def ListInvoicesView(request):
    invoices = TransactionModel.objects.filter(
        transactionMethod='Invoice').order_by('-date_created')

    context = {
        "invoices": invoices
    }
    return render(request, 'document/list_invoices.html', context)


def ListQoutesView(request):
    qoutes = TransactionModel.objects.filter(
        transactionMethod='Qoute').order_by('-date_created')

    context = {
        "qoutes": qoutes
    }
    return render(request, 'document/list_qoutes.html', context)
