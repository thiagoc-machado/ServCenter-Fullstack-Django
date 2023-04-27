from django.urls import path
from . import views

urlpatterns = [
    path('', views.users, name="users"),
    path('new_users/', views.new_users, name="new_users"),
    path('edit_users/<int:id>', views.edit_users, name="edit_users"),
    path('del_users/<int:id>', views.del_users, name="del_users"),
    #path('users_xlr/', views.users_xlr, name='users_xlr')
]


