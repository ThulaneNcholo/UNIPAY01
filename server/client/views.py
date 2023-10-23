from django.shortcuts import render, redirect
from transactions.models import *
from django.db.models import Q
from inventory.models import *
from exepenses.models import *
from todo.models import *
import json
from datetime import datetime, timedelta
from django.db.models import F, Sum, FloatField
from django.db.models.functions import Coalesce

# Create your views here.


def IndexView(request):
    transactions = TransactionModel.objects.all()
    sales = transactions.filter(
        Q(transactionMethod="Invoice") | Q(transactionMethod="Sale"))
    qoutes = transactions.filter(
        transactionMethod="Qoute").order_by("-date_created")[0:5]
    qoutesCount = transactions.filter(
        transactionMethod="Qoute").count()
    clients = CustomerModel.objects.all()
    clientsCount = clients.count()
    inventory = InventoryModel.objects.all()
    total_sales = 0
    todos = TodoModel.objects.filter(
        status='Pending').order_by('-status', '-date_created')[0:5]
    invoices = transactions.filter(transactionMethod="Invoice")

    # Get Recurring Invoices
    current_date = datetime.now()
    this_month = current_date.strftime("%B")
    current_month = current_date.month
    today = datetime.now()
    monday = today - timedelta(days=today.weekday())
    sunday = monday + timedelta(days=6)

    # Extract the day of the month for Monday and Sunday
    monday_day = monday.day
    sunday_day = sunday.day

    recurringInvoiceDays = invoices.filter(
        recurring_transaction__start_date__range=(monday_day, sunday_day))
    recurringInvoices = recurringInvoiceDays.filter(
        Q(recurring_transaction__recurrence_period=1) | Q(recurring_transaction__recurrence_period=current_month)).order_by('-date_created')[0:6]

    # Open Invoices start

    openInvoices = invoices.filter(
        ~Q(amountPaid=F('income'))).order_by('-date_created')[0:6]

    for i in sales:
        total_sales = float(total_sales) + float(i.income)

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

    # Bar graph start
    income = float(0)
    barChart = []
    documents = InvoiceDocumentsModel.objects.all()
    expenses = ExpenseModel.objects.all()

    # Monthly Earnings
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
                'expense': float(0),  # Initialize 'expense' to 0
            }
            barChart.append(barChart_data)

    # Monthly Expenses
    for i in expenses:
        month_exists = False
        for data in barChart:
            if data['month'] == i.month:
                data['expense'] += float(i.amount)
                month_exists = True
                break
        if not month_exists:
            barChart_data = {
                'month': i.month,
                'expense': float(i.amount),
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

    # Monthly Clients onboarding
    onboardClients = []

    for i in clients:
        month_exists = False
        for data in onboardClients:
            if data['month'] == i.month:
                data['total'] += 1
                month_exists = True
                break
        if not month_exists:
            clinetList = {
                'month': i.month,
                'total': 1,
            }
            onboardClients.append(clinetList)

    onboardClients.sort(key=lambda x: get_month_numerical_value(x['month']))
    clinetsGraph = json.dumps(onboardClients)

    # Top selling products
    products = []
    for i in documents:
        if i.inventory != None:
            product_exists = False
            for data in products:
                if data['ref'] == i.inventory.ref:
                    data['total'] += float(i.documentTotal)
                    product_exists = True
                    break
            if not product_exists:
                product_data = {
                    'ref': i.inventory.ref,
                    'total': float(i.documentTotal),
                    'name': i.inventory.name
                }
                products.append(product_data)

    for i in documents:
        if i.service != None:
            product_exists = False
            for data in products:
                if data['ref'] == i.service.ref:
                    data['total'] += float(i.documentTotal)
                    product_exists = True
                    break
            if not product_exists:
                product_data = {
                    'ref': i.service.ref,
                    'total': float(i.documentTotal),
                    'name': i.service.name
                }
                products.append(product_data)

    # Sort the products by 'total' in descending order
    sorted_products = sorted(products, key=lambda x: x['total'], reverse=True)

    # Get the top 5 selling products
    top_5_selling_products = sorted_products[:5]

    # Calculate the total income for the top 5 selling products
    total_income_top_5 = sum(product['total']
                             for product in top_5_selling_products)

    # Calculate the percentages for the top 5 selling products and round them to one decimal place
    for product in top_5_selling_products:
        percentage = (product['total'] / total_income_top_5) * 100
        product['percentage'] = round(percentage, 1)

    top_products = json.dumps(top_5_selling_products)

    if request.method == 'POST' and 'complete_todo_list' in request.POST:
        todoID = request.POST.get('todoID')
        complete_todo = TodoModel.objects.get(id=todoID)
        complete_todo.status = 'Complete'
        complete_todo.save()
        return redirect('index')

    context = {
        "transactions": transactions,
        "total_sales": total_sales,
        "qoutes": qoutes,
        "qoutesCount": qoutesCount,
        "clientsCount": clientsCount,
        "lowStock": lowStock,
        "outStock": outStock,
        "barChart_json": barChart_json,
        "top_5_selling_products": top_5_selling_products,
        "top_products": top_products,
        "clinetsGraph": clinetsGraph,
        "todos": todos,
        "openInvoices": openInvoices,
        "recurringInvoices": recurringInvoices,
        "this_month": this_month,
    }
    return render(request, 'client/index.html', context)
