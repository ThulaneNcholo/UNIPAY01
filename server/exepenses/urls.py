from django.urls import path
from .import views


urlpatterns = [
    path('list-expenses', views.ExpensesView, name='list-expenses'),
    path('add-expense', views.AddExpenseView, name='add-expense'),
]
