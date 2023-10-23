from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from inventory.models import *
import random
import datetime

# Create your views here.


def ExpensesView(request):
    categories = ExpensesCategory.objects.all().order_by('-date_created')
    expenses = ExpenseModel.objects.all().order_by('-date_created')

    context = {
        "categories": categories,
        "expenses": expenses
    }
    return render(request, 'expenses/list_expenses.html', context)


def AddExpenseView(request):
    ref_number = random.randrange(10000, 1000000)
    ref = 'EP' + str(ref_number)
    categories = CategoryModel.objects.all().order_by('-date_created')

    if request.method == 'POST' and 'submit_expense' in request.POST:
        current_date = datetime.date.today()
        amount = request.POST.get('Amount')
        categoryID = request.POST.get('category')
        categoryProfile = CategoryModel.objects.get(id=categoryID)
        if 'receipt' in request.FILES:
            receipt = request.FILES['receipt']
        else:
            receipt = None

        createExpense = ExpenseModel()
        createExpense.ref = request.POST.get('Referrance')
        createExpense.name = request.POST.get('name')
        createExpense.description = request.POST.get('description')
        createExpense.expenseDate = request.POST.get('expenseDate')
        createExpense.amount = float(amount)
        createExpense.month = current_date.strftime("%B")
        createExpense.year = current_date.year
        createExpense.category = categoryProfile
        if receipt:
            createExpense.file = receipt
        createExpense.save()
        messages.success(request, 'new expense created')
        return redirect('list-expenses')

    context = {
        "ref": ref,
        "categories": categories
    }
    return render(request, 'expenses/add_expense.html', context)
