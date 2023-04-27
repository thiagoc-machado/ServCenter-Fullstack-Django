from django.urls import path
from . import views

urlpatterns = [
    path('', views.employees, name="employees"),
    path('new_employees/', views.new_employees, name="new_employees"),
    path('edit_employees/<int:cod>', views.edit_employees, name="edit_employees"),
    path('del_employees/<int:cod>', views.del_employees, name="del_employees"),
    path('employees_xlrx/', views.employees_xlrx, name='employees_xlrx')
]
