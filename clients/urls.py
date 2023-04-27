from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', views.clients, name="clients"),
    path('new_client/', views.new_client, name="new_client"),
    path('del_cli/<int:cod_cli>', views.del_cli, name="del_cli"),
    # path('edit_client/<int:cod_cli>', views.edit_cli, name="edit_cli"),
    path('edit_client/<int:cod_cli>/', views.edit_client, name='edit_client'),
    path('clientes_xlr/', views.clientes_xlr, name='clientes_xlr')
]
