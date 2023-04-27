from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.messages import constants
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.hashers import make_password
import pandas as pd

@user_passes_test(lambda u: u.is_superuser)
def users(request):
    if request.method == "GET":
        users = User.objects.all()
        groups = Group.objects.all()
        return render(request, 'users.html', {'users': users, groups:'groups'})


@user_passes_test(lambda u: u.is_superuser)
def new_users(request):
    if request.method == "GET":
        users = User.objects.all()
        return render(request, 'new_users.html', {'users': users})

    elif request.method == "POST":

        password = request.POST.get("password")
        is_superuser = request.POST.get("is_superuser")
        username = request.POST.get("username")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        is_staff = request.POST.get("is_staff")
        is_active = request.POST.get("is_active")
        first_name = request.POST.get("first_name")

        if is_superuser == 'on':
            is_superuser = True
        else:
            is_superuser = False

        if is_staff == 'on':
            is_staff = True
        else:
            is_staff = False

        if is_active == 'on':
            is_active = True
        else:
            is_active = False

        Users = User(
            username=username,
            last_name=last_name,
            email=email,
            first_name=first_name,
            is_superuser=is_superuser,
            is_staff=is_staff,
            is_active=is_active,
        )

        if username == "" or last_name == "" or last_name == "" or email == "" or first_name == "":
            messages.add_message(request, constants.ERROR,
                                 'Todos os campos devem ser preechidos')

            return render(request, 'new_users.html', {'is_superuser': is_superuser, 'username': username, 'last_name': last_name,
                                                     'email': email, 'is_staff': is_staff, 'is_active': is_active, 'first_name': first_name})
        
        
        existing_user = User.objects.filter(username=username)
        if existing_user:
            messages.add_message(request, constants.ERROR,
                                 'Nome de usuário não disponivel, escolha outro')
            return render(request, 'new_users.html', {'is_superuser': is_superuser, 'last_name': last_name,
                                                     'email': email, 'is_staff': is_staff, 'is_active': is_active, 'first_name': first_name
        })
            
        if request.user.is_superuser == False:
            messages.add_message(request, constants.ERROR,
                                 'Voce não tem permissão para atualizar os dados')
            return redirect('users')
            
        else:
            Users.set_password(password)
            Users.save()
            messages.add_message(request, constants.SUCCESS,
                                 'Novo Usuário cadastrado com sucesso')
            return redirect('users')


@user_passes_test(lambda u: u.is_superuser)
def edit_users(request, id):

    if request.method == "GET":

        if User.objects.get(id=id).last_login == None:
            last_login = User.objects.get(id=id).date_joined
        else:
            last_login = User.objects.get(id=id).last_login

        return render(request, 'edit_users.html', {'id': id,
                                                   #'password': User.objects.get(id=id).password,
                                                   'last_login': last_login.strftime("%Y-%m-%d"),
                                                   'is_superuser': User.objects.get(id=id).is_superuser,
                                                   'username': User.objects.get(id=id).username,
                                                   'last_name': User.objects.get(id=id).last_name,
                                                   'email': User.objects.get(id=id).email,
                                                   'is_staff': User.objects.get(id=id).is_staff,
                                                   'is_active': User.objects.get(id=id).is_active,
                                                   'date_joined': User.objects.get(id=id).date_joined.strftime("%Y-%m-%d"),
                                                   'first_name': User.objects.get(id=id).first_name,
                                                   })

    elif request.method == "POST":
        user_obj = User.objects.get(id=id)
        if request.POST.get("password") != User.objects.get(id=id).password:
            user_obj.password = make_password(request.POST.get("password"))
        user_obj.last_login = request.POST.get("last_login")
        user_obj.is_superuser = request.POST.get("is_superuser")
        user_obj.username = request.POST.get("username")
        user_obj.last_name = request.POST.get("last_name")
        user_obj.email = request.POST.get("email")
        user_obj.is_staff = request.POST.get("is_staff")
        user_obj.is_active = request.POST.get("is_active")
        user_obj.date_joined = request.POST.get("date_joined")
        user_obj.first_name = request.POST.get("first_name")

        if user_obj.is_superuser == 'on':
            user_obj.is_superuser = True
        else:
            user_obj.is_superuser = False

        if user_obj.is_staff == 'on':
            user_obj.is_staff = True
        else:
            user_obj.is_staff = False

        if user_obj.is_active == 'on':
            user_obj.is_active = True
        else:
            user_obj.is_active = False

        if user_obj.username == "" or user_obj.last_name == "" or user_obj.last_name == "" or user_obj.email == "" or user_obj.first_name == "":
            messages.add_message(request, constants.ERROR,
                                 'Todos os campos devem ser preechidos')
            return render(request, 'edit_user.html', {'id': id, 'password': user_obj.password, 'is_superuser': user_obj.is_superuser, 'username': user_obj.username, 'last_name': user_obj.last_name,
                                                      'email': user_obj.email, 'is_staff': user_obj.is_staff, 'is_active': user_obj.is_active, 'first_name': user_obj.first_name})

        if request.user.is_superuser == False:
            messages.add_message(request, constants.ERROR,
                                 'Voce não tem permissão para atualizar os dados')
            return redirect('users')
        
        else:
            user_obj.save()
            messages.add_message(request, constants.SUCCESS,
                                 'Usuário atualizado com sucesso')
            return redirect('users')


@user_passes_test(lambda u: u.is_superuser)
def del_users(request, id):
    
    if request.user.is_superuser == False:
            messages.add_message(request, constants.ERROR,
                                 'Voce não tem permissão para atualizar os dados')
            return redirect('users')
    else:
        user = User.objects.get(id=id)
        user.delete()
        messages.add_message(request, constants.SUCCESS,
                            'Usuário apagado com sucesso')
        return redirect('users')

# @user_passes_test(lambda u: u.is_superuser)
# def users_xlr(request):
#     # Pegar os dados da tabela workorders
#     workorders = User.objects.all()

#     # Converter os dados para um DataFrame do Pandas
#     df = pd.DataFrame(list(workorders.values()))

#     # Configurar o nome do arquivo de download
#     filename = 'ordem de servicos.xlsx'

#     # Configurar o tipo de resposta HTTP
#     response = HttpResponse(
#         content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
#     response['Content-Disposition'] = f'attachment; filename="{filename}"'

#     # Gerar o arquivo Excel usando o Pandas e salvar no objeto HttpResponse
#     df.to_excel(response, index=False)

#     return response
