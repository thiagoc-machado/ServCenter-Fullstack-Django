from django.urls import path
from . import views

urlpatterns = [
    path('', views.my_login, name="login"),
    path('sair/', views.sair, name="sair")
]