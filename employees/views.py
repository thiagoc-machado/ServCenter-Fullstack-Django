from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.messages import constants
from .models import Employees
from django.contrib.auth.decorators import user_passes_test
import pandas as pd

@user_passes_test(lambda u: u.is_superuser)
def employees(request):
    if request.method == "GET":
        emp = Employees.objects.all()

        return render(request, 'employees.html', {'emp': emp})


@user_passes_test(lambda u: u.is_superuser)
def new_employees(request):
    if request.method == "GET":
        return render(request, 'new_employees.html')

    elif request.method == "POST":

        nome = request.POST.get("inputNome")
        rg = request.POST.get("inputRg")
        cpf = request.POST.get("inputCpf")
        data_nasc = request.POST.get("inputNasc")
        func = request.POST.get("inputTipo")
        telefone = request.POST.get("inputTel")
        celular = request.POST.get("inputCel")
        whatsapp = request.POST.get("inputWts")
        email = request.POST.get("inputEmail")
        foto = request.POST.get("foto")
        rua = request.POST.get("inputRua")
        numero = request.POST.get("inputNum")
        compl = request.POST.get("inputComp")
        bairro = request.POST.get("inputBai")
        cidade = request.POST.get("inputCid")
        uf = request.POST.get("inputUf")
        cep = request.POST.get("inputCep")
        tipo_end = request.POST.get("inputTipoEnd")
        ativo = True

        if data_nasc == "":
            data_nasc = "1900-01-01"

        Client = Employees(

            nome=nome,
            rg=rg,
            cpf=cpf,
            data_nasc=data_nasc,
            func=func,
            telefone=telefone,
            celular=celular,
            whatsapp=whatsapp,
            email=email,
            foto=foto,
            rua=rua,
            numero=numero,
            compl=compl,
            bairro=bairro,
            cidade=cidade,
            uf=uf,
            cep=cep,
            tipo_end=tipo_end,
            ativo=ativo,
        )

        if nome == "":
            messages.add_message(request, constants.ERROR,
                                 'Verifique os dados inseridos')

            return render(request, 'new_employees.html', {'name': nome, 'rg': rg, 'cpf': cpf, 'data_nasc': data_nasc,
                                                          'tipo_cad': func, 'telefone': telefone, 'celular': celular, 'whatsapp': whatsapp, 'email': email, 'cpf': cpf,
                                                          'foto': foto, 'rua': rua, 'numero': numero, 'compl': compl, 'bairro': bairro,
                                                          'cidade': cidade, 'uf': uf, 'cep': cep, 'tipo_end': tipo_end, 'ativo': ativo})

        else:

            Client.save()
            messages.add_message(request, constants.SUCCESS,
                                 'Novo funcionario cadastrado com sucesso')
            return redirect('employees')


@user_passes_test(lambda u: u.is_superuser)
def edit_employees(request, cod):

    if request.method == "GET":
        return render(request, 'edit_employees.html', {'cod': Employees.objects.get(cod=cod).cod,
                                                       'nome': Employees.objects.get(cod=cod).nome,
                                                       'func': Employees.objects.get(cod=cod).func,
                                                       'rg': Employees.objects.get(cod=cod).rg,
                                                       'cpf': Employees.objects.get(cod=cod).cpf,
                                                       'data_nasc': Employees.objects.get(cod=cod).data_nasc.strftime("%Y-%m-%d"),
                                                       'telefone': Employees.objects.get(cod=cod).telefone,
                                                       'celular': Employees.objects.get(cod=cod).celular,
                                                       'whatsapp': Employees.objects.get(cod=cod).whatsapp,
                                                       'email': Employees.objects.get(cod=cod).email,
                                                       'data_cadastro': Employees.objects.get(cod=cod).data_cadastro.strftime("%Y-%m-%d"),
                                                       'foto': Employees.objects.get(cod=cod).foto,
                                                       'rua': Employees.objects.get(cod=cod).rua,
                                                       'numero': Employees.objects.get(cod=cod).numero,
                                                       'compl': Employees.objects.get(cod=cod).compl,
                                                       "bairro": Employees.objects.get(cod=cod).bairro,
                                                       'cidade': Employees.objects.get(cod=cod).cidade,
                                                       'uf': Employees.objects.get(cod=cod).uf,
                                                       'cep': Employees.objects.get(cod=cod).cep,
                                                       'tipo_end': Employees.objects.get(cod=cod).tipo_end,
                                                       'ativo': Employees.objects.get(cod=cod).ativo,

                                                       })

    elif request.method == "POST":
        emp_obj = Employees.objects.get(cod=cod)

        emp_obj.nome = request.POST.get("inputNome")
        emp_obj.rg = request.POST.get("inputRg")
        emp_obj.cpf = request.POST.get("inputCpf")
        emp_obj.data_nasc = request.POST.get("inputNasc")
        emp_obj.func = request.POST.get("inputTipo")
        emp_obj.telefone = request.POST.get("inputTel")
        emp_obj.celular = request.POST.get("inputCel")
        emp_obj.whatsapp = request.POST.get("inputWts")
        emp_obj.email = request.POST.get("inputEmail")
        emp_obj.data_cadastro = request.POST.get("data_cad")
        emp_obj.foto = request.POST.get("foto")
        emp_obj.rua = request.POST.get("inputRua")
        emp_obj.numero = request.POST.get("inputNum")
        emp_obj.compl = request.POST.get("inputComp")
        emp_obj.bairro = request.POST.get("inputBai")
        emp_obj.cidade = request.POST.get("inputCid")
        emp_obj.uf = request.POST.get("inputUf")
        emp_obj.cep = request.POST.get("inputCep")
        emp_obj.tipo_end = request.POST.get("inputTipoEnd")
        emp_obj.ativo = request.POST.get("ativo")

        if emp_obj.ativo == 'on':
            emp_obj.ativo = True
        else:
            emp_obj.ativo = False
        print('******************************')
        print(emp_obj.ativo)
        print('******************************')

        if emp_obj.nome == "":
            messages.add_message(request, constants.ERROR,
                                 'Verifique os dados inseridos')
            return render(request, 'new_employees.html', {'cod': cod, 'name': emp_obj.nome, 'rg': emp_obj.rg, 'cpf': emp_obj.cpf, 'data_nasc': emp_obj.data_nasc,
                                                          'tipo_cad': emp_obj.func, 'telefone': emp_obj.telefone, 'celular': emp_obj.celular,
                                                          'whatsapp': emp_obj.whatsapp, 'email': emp_obj.email, 'cpf': emp_obj.cpf, 'data_cadastro': emp_obj.data_cadastro,
                                                          'foto': emp_obj.foto, 'rua': emp_obj.rua, 'numero': emp_obj.numero, 'compl': emp_obj.compl, 'bairro': emp_obj.bairro,
                                                          'cidade': emp_obj.cidade, 'uf': emp_obj.uf, 'cep': emp_obj.cep, 'tipo_end': emp_obj.tipo_end, 'ativo': emp_obj.ativo})

        else:
            emp_obj.save()
            messages.add_message(request, constants.SUCCESS,
                                 'Cliente atualizado com sucesso')
            return redirect('employees')


@user_passes_test(lambda u: u.is_superuser)
def del_employees(request, cod):
    emp = Employees.objects.get(cod=cod)
    emp.delete()
    messages.add_message(request, constants.SUCCESS,
                         'Employeese apagado com sucesso')
    return redirect('employees')

@user_passes_test(lambda u: u.is_superuser)
def employees_xlrx(request):
    # Pegar os dados da tabela workorders
    workorders = Employees.objects.all()

    # Converter os dados para um DataFrame do Pandas
    df = pd.DataFrame(list(workorders.values()))

    # Configurar o nome do arquivo de download
    filename = 'workorders.xlsx'

    # Configurar o tipo de resposta HTTP
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    # Gerar o arquivo Excel usando o Pandas e salvar no objeto HttpResponse
    df.to_excel(response, index=False)

    return response