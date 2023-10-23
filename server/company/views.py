from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from client.models import AddressModel

# Create your views here.


def CompnayProfileView(request):
    companyRef = "CO98364"
    company = ProfileModel.objects.get(ref=companyRef)

    # company profile submit
    if request.method == 'POST' and 'submit_company' in request.POST:
        createCompanyInfo = CompanyInfoModel()
        createCompanyInfo.name = request.POST.get('companyName')
        createCompanyInfo.phone = request.POST.get('companyPhone')
        createCompanyInfo.email = request.POST.get('email')
        createCompanyInfo.registration = request.POST.get('registration')
        createCompanyInfo.save()

        # update Company Profile
        company.companyInfo = createCompanyInfo
        company.save()

        messages.success(request, 'company information updated')
        return redirect('company-profile')

    # company Address submit
    if request.method == 'POST' and 'submit_address' in request.POST:
        createAddress = AddressModel()
        createAddress.street = request.POST.get('street')
        createAddress.suburb = request.POST.get('suburb')
        createAddress.city = request.POST.get('city')
        createAddress.province = request.POST.get('province')
        createAddress.pobox = request.POST.get('pobox')
        createAddress.save()

        # update Company Profile
        company.address = createAddress
        company.save()

        messages.success(request, 'company Address updated')
        return redirect('company-profile')

    # company logo
    if request.method == 'POST' and 'submit_logo' in request.POST:
        companylogo = request.FILES['companylogo']
        company.logo = companylogo
        company.save()
        messages.success(request, 'Logo Updated')
        return redirect('company-profile')

    # company bank submit
    if request.method == 'POST' and 'submit_bank' in request.POST:
        createBank = BankModel()
        createBank.bankName = request.POST.get('bank')
        createBank.branch = request.POST.get('branch')
        createBank.account = request.POST.get('account')
        createBank.save()

        # update Company Profile
        company.bank = createBank
        company.save()

        messages.success(request, 'Bank details updated')
        return redirect('company-profile')

    context = {
        "company": company
    }

    return render(request, 'company/companyProfile.html', context)
