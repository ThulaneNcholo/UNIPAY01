from django.urls import path
from .import views


urlpatterns = [
    path('employees', views.EmployeesView, name='employees'),
    path('add-employee', views.AddEmployeeView, name='add-employee'),
]
