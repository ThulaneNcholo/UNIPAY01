from django.shortcuts import render, redirect
import random
from .models import *
from client.models import AddressModel
from company.models import BankModel
from django.contrib import messages

# Create your views here.


def EmployeesView(request):
    employees = EmployeesModel.objects.all().order_by('-date_created')

    context = {
        "employees": employees
    }
    return render(request, 'employees/employees.html', context)


def AddEmployeeView(request):

    if request.method == 'POST' and 'submit_empoyee' in request.POST:

        # address
        saveAddress = AddressModel()
        saveAddress.street = request.POST.get('street')
        saveAddress.suburb = request.POST.get('Suburb')
        saveAddress.city = request.POST.get('city')
        saveAddress.province = request.POST.get('province')
        saveAddress.pobox = request.POST.get('pobox')
        saveAddress.save()

        # Bank
        saveBank = BankModel()
        saveBank.bankName = request.POST.get('bankName')
        saveBank.branch = request.POST.get('branch')
        saveBank.account = request.POST.get('account')
        saveBank.save()

        # employee
        refNumner = random.randrange(0, 10000000)
        ref = 'EMP' + str(refNumner)

        saveEmployee = EmployeesModel()
        saveEmployee.ref = ref
        saveEmployee.firstName = request.POST.get('FirstName')
        saveEmployee.lastName = request.POST.get('lastName')
        saveEmployee.phone = request.POST.get('PhoneNumber')
        saveEmployee.email = request.POST.get('email')
        saveEmployee.payday = request.POST.get('paydate')
        saveEmployee.salary = request.POST.get('salary')
        saveEmployee.address = saveAddress
        saveEmployee.bank = saveBank
        profilepic = request.FILES['profilepic']
        if profilepic:
            saveEmployee.profile_image = profilepic
        saveEmployee.save()

        messages.success(request, 'new employee added')
        return redirect('employees')
    return render(request, 'employees/add_employee.html')
