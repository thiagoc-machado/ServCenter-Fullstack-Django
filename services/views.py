from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.messages import constants
from .models import Services
import pandas as pd
from django.contrib.auth.decorators import user_passes_test


@login_required
def services(request):
    if request.method == "GET":
        serv = Services.objects.all()

        return render(request, 'services.html', {'serv': serv})


@login_required
def new_services(request):
    if request.method == "GET":
        return render(request, 'new_services.html')

    elif request.method == "POST":

        tipo = request.POST.get("inputTipo")
        nome = request.POST.get("inputNome")
        descr = request.POST.get("inputRg")
        valor = request.POST.get("inputCpf")
        obs = request.POST.get("inputTipo")
        foto = request.POST.get("foto")

        services = Services(

            tipo=tipo,
            nome=nome,
            descr=descr,
            valor=valor,
            obs=obs,
            foto=foto,
        )

        if nome == "":
            messages.add_message(request, constants.ERROR,
                                 'Verifique os dados inseridos')

            return render(request, 'new_services.html', {'name': nome, 'tipo': tipo, 'descr': descr, 'valor': valor, 'obs': obs, 'foto': foto, })

        else:

            services.save()
            messages.add_message(request, constants.SUCCESS,
                                 'Novo funcionario cadastrado com sucesso')
            return redirect('services')


@login_required
def edit_services(request, cod):

    if request.method == "GET":
        return render(request, 'edit_services.html', {'cod': Services.objects.get(cod=cod).cod,
                                                      'nome': Services.objects.get(cod=cod).nome,
                                                      'tipo': Services.objects.get(cod=cod).tipo,
                                                      'descr': Services.objects.get(cod=cod).descr,
                                                      'valor': Services.objects.get(cod=cod).valor,
                                                      'obs': Services.objects.get(cod=cod).obs,
                                                      'data_cadastro': Services.objects.get(cod=cod).data_cadastro.strftime("%Y-%m-%d"),
                                                      'foto': Services.objects.get(cod=cod).foto, })

    elif request.method == "POST":
        services_obj = Services.objects.get(cod=cod)
        services_obj.nome = request.POST.get("inputNome")
        services_obj.descr = request.POST.get("inputdescr")
        services_obj.valor = request.POST.get("inputvalor")
        services_obj.obs = request.POST.get("inputobs")
        services_obj.tipo = request.POST.get("inputTipo")
        services_obj.data_cadastro = request.POST.get("input-dataCad")
        services_obj.foto = request.POST.get("foto")

        if services_obj.nome == "":
            messages.add_message(request, constants.ERROR,
                                 'Verifique os dados inseridos')
            return render(request, 'new_services.html', {'cod': cod, 'name': services_obj.nome, 'tipo': services_obj.tipo,
                                                         'valor': services_obj.valor, 'descr': services_obj.descr,
                                                         'data_cadastro': services_obj.data_cadastro, 'foto': services_obj.foto, 'obs': services_obj.obs})

        else:
            services_obj.save()
            messages.add_message(request, constants.SUCCESS,
                                 'Cliente atualizado com sucesso')
            return redirect('services')


@ login_required
def del_services(request, cod):
    emp = Services.objects.get(cod=cod)
    emp.delete()
    messages.add_message(request, constants.SUCCESS,
                         'serviços apagado com sucesso')
    return redirect('services')

@user_passes_test(lambda u: u.is_superuser)
def services_xlr(request):
    # Pegar os dados da tabela workorders
    workorders = Services.objects.all()

    # Converter os dados para um DataFrame do Pandas
    df = pd.DataFrame(list(workorders.values()))

    # Configurar o nome do arquivo de download
    filename = 'ordem de servicos.xlsx'

    # Configurar o tipo de resposta HTTP
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    # Gerar o arquivo Excel usando o Pandas e salvar no objeto HttpResponse
    df.to_excel(response, index=False)

    return response
