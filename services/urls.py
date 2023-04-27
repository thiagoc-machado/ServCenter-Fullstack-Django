from django.urls import path
from . import views

urlpatterns = [
    path('', views.services, name="services"),
    path('new_services/', views.new_services, name="new_services"),
    path('edit_services/<int:cod>', views.edit_services, name="edit_services"),
    path('del_services/<int:cod>', views.del_services, name="del_services"),
    path('services_xlr/', views.services_xlr, name='services_xlr')
]
