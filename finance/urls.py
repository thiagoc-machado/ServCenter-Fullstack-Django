from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', views.finance, name="finance"),
    path('finance_dia/', views.finance_dia, name="finance_dia"),
    path('finance_sem/', views.finance_sem, name="finance_sem"),
    path('finance_mes/', views.finance_mes, name="finance_mes"),
    path('finance_ano/', views.finance_ano, name="finance_ano"),
    path('finance_tot/', views.finance_tot, name="finance_tot"),
    path('new_finance/', views.new_finance, name="new_finance"),
    path('new_finance_out/', views.new_finance_out, name="new_finance_out"),
    path('del_finance/<int:id>', views.del_finance, name="del_finance"),
    path('edit_finance/<int:id>', views.edit_finance, name='edit_finance'),
    path('finance_xlrx/<int:id>', views.finance_xlrx, name='finance_xlrx'),
]