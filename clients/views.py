from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.messages import constants
from django.contrib.auth.decorators import login_required
from .models import client, User
from django.shortcuts import redirect
import pandas as pd
from django.contrib.auth.decorators import user_passes_test


@login_required
def clients(request):
    if request.method == "GET":
        cli = client.objects.all()

        return render(request, 'clients.html', {'cli': cli})
    else:
        return HttpResponseBadRequest('Invalid request method')


@login_required
def new_client(request):
    if request.method == "GET":
        users = User.objects.all()
        return render(request, 'new_client.html', {'users': users})

    elif request.method == "POST":

        nome = request.POST.get("inputNome")
        rg = request.POST.get("inputRg")
        cpf = request.POST.get("inputCpf")
        data_nasc = request.POST.get("inputNasc")
        tipo_cad = request.POST.get("inputTipo")
        telefone = request.POST.get("inputTel")
        celular = request.POST.get("inputCel")
        whatsapp = request.POST.get("inputWts")
        email = request.POST.get("inputEmail")
        rua = request.POST.get("inputRua")
        numero = request.POST.get("inputNum")
        compl = request.POST.get("inputComp")
        bairro = request.POST.get("inputBai")
        cidade = request.POST.get("inputCid")
        uf = request.POST.get("inputUf")
        cep = request.POST.get("inputCep")
        tipo_end = request.POST.get("inputTipoEnd")
        vendedor = User.objects.get(pk=request.POST.get("inputVend"))
        ativo = request.POST.get("gridCheck")
        foto = request.FILES.get("foto")

        if ativo == 'on':
            ativo = True
        else:
            ativo = False

        if data_nasc == "":
            data_nasc = "1900-01-01"

        Client = client(

            nome=nome,
            rg=rg,
            cpf=cpf,
            data_nasc=data_nasc,
            tipo_cad=tipo_cad,
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
            vendedor=vendedor,
            ativo=ativo,
        )

        if nome == "":
            messages.add_message(request, constants.ERROR,
                                 'Verifique os dados inseridos')
            users = User.objects.all()
            return render(request, 'new_client.html', {'users': users, 'vendedor': vendedor, 'name': nome, 'rg': rg, 'cpf': cpf, 'data_nasc': data_nasc,
                                                       'tipo_cad': tipo_cad, 'telefone': telefone, 'celular': celular, 'whatsapp': whatsapp, 'email': email, 'cpf': cpf,
                                                       'foto': foto, 'rua': rua, 'numero': numero, 'compl': compl, 'bairro': bairro,
                                                       'cidade': cidade, 'uf': uf, 'cep': cep, 'tipo_end': tipo_end, 'vendedor': vendedor, 'ativo': ativo})

        else:

            Client.save()
            messages.add_message(request, constants.SUCCESS,
                                 'Novo cliente cadastrado com sucesso')
            return redirect('clients')
    else:
        return HttpResponseBadRequest('Invalid request method')


@ login_required
def del_cli(request, cod_cli):
    cli = client.objects.get(cod_cli=cod_cli)
    cli.delete()
    messages.add_message(request, constants.SUCCESS,
                         'Cliente apagado com sucesso')
    return redirect('clients')


@login_required
def edit_client(request, cod_cli):
    if request.method == 'GET':

        return render(request, 'edit_client.html', {
            'cod_cli': client.objects.get(cod_cli=cod_cli).cod_cli,
            'nome': client.objects.get(cod_cli=cod_cli).nome,
            'rg': client.objects.get(cod_cli=cod_cli).rg,
            'cpf': client.objects.get(cod_cli=cod_cli).cpf,
            'data_nasc': client.objects.get(cod_cli=cod_cli).data_nasc.strftime("%Y-%m-%d"),
            'tipo_cad': client.objects.get(cod_cli=cod_cli).tipo_cad,
            'telefone': client.objects.get(cod_cli=cod_cli).telefone,
            'celular': client.objects.get(cod_cli=cod_cli).celular,
            'whatsapp': client.objects.get(cod_cli=cod_cli).whatsapp,
            'email': client.objects.get(cod_cli=cod_cli).email,
            'data_cadastro': client.objects.get(cod_cli=cod_cli).data_cadastro.strftime("%Y-%m-%d"),
            'foto': client.objects.get(cod_cli=cod_cli).foto,
            'rua': client.objects.get(cod_cli=cod_cli).rua,
            'numero': client.objects.get(cod_cli=cod_cli).numero,
            'compl': client.objects.get(cod_cli=cod_cli).compl,
            "bairro": client.objects.get(cod_cli=cod_cli).bairro,
            'cidade': client.objects.get(cod_cli=cod_cli).cidade,
            'uf': client.objects.get(cod_cli=cod_cli).uf,
            'cep': client.objects.get(cod_cli=cod_cli).cep,
            'tipo_end': client.objects.get(cod_cli=cod_cli).tipo_end,
            'vendedor': client.objects.get(cod_cli=cod_cli).vendedor,
            'ativo': client.objects.get(cod_cli=cod_cli).ativo,
            'users': User.objects.all()
        })

    elif request.method == "POST":
        client_obj = client.objects.get(cod_cli=cod_cli)

        client_obj.nome = request.POST.get("inputNome")
        client_obj.rg = request.POST.get("inputRg")
        client_obj.cpf = request.POST.get("inputCpf")
        client_obj.data_nasc = request.POST.get("inputNasc")
        client_obj.tipo_cad = request.POST.get("inputTipo")
        client_obj.telefone = request.POST.get("inputTel")
        client_obj.celular = request.POST.get("inputCel")
        client_obj.whatsapp = request.POST.get("inputWts")
        client_obj.email = request.POST.get("inputEmail")
        client_obj.data_cadastro = request.POST.get("data_cad")
        client_obj.foto = request.POST.get("foto")
        client_obj.rua = request.POST.get("inputRua")
        client_obj.numero = request.POST.get("inputNum")
        client_obj.compl = request.POST.get("inputComp")
        client_obj.bairro = request.POST.get("inputBai")
        client_obj.cidade = request.POST.get("inputCid")
        client_obj.uf = request.POST.get("inputUf")
        client_obj.cep = request.POST.get("inputCep")
        client_obj.tipo_end = request.POST.get("inputTipoEnd")
        client_obj.ativo = request.POST.get("ativo")
        vendedor_id = request.POST.get("inputVend")
        vendedor = User.objects.get(id=vendedor_id)
        client_obj.vendedor = vendedor

        if client_obj.ativo == 'on':
            client_obj.ativo = True
        else:
            client_obj.ativo = False

        if client_obj.nome == "":
            messages.add_message(request, constants.ERROR,
                                 'Verifique os dados inseridos')
            return render(request, 'new_client.html', {
                'cod_cli': cod_cli, 'name': client_obj.nome, 'rg': client_obj.rg, 'cpf': client_obj.cpf, 'data_nasc': client_obj.data_nasc,
                'tipo_cad': client_obj.tipo_cad, 'telefone': client_obj.telefone, 'celular': client_obj.celular,
                'whatsapp': client_obj.whatsapp, 'email': client_obj.email, 'cpf': client_obj.cpf, 'data_cadastro': client_obj.data_cadastro,
                'foto': client_obj.foto, 'rua': client_obj.rua, 'numero': client_obj.numero, 'compl': client_obj.compl, 'bairro': client_obj.bairro,
                'cidade': client_obj.cidade, 'uf': client_obj.uf, 'cep': client_obj.cep, 'tipo_end': client_obj.tipo_end, 'vendedor': vendedor, 'ativo': client_obj.ativo})

        else:
            client_obj.save()
            messages.add_message(request, constants.SUCCESS,
                                 'Cliente atualizado com sucesso')
            return redirect('clients')
    else:
        return HttpResponseBadRequest('Invalid request method')

@user_passes_test(lambda u: u.is_superuser)
def clientes_xlr(request):
    # Pegar os dados da tabela workorders
    workorders = client.objects.all()

    # Converter os dados para um DataFrame do Pandas
    df = pd.DataFrame(list(workorders.values()))

    # Configurar o nome do arquivo de download
    filename = 'clientes.xlsx'

    # Configurar o tipo de resposta HTTP
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    # Gerar o arquivo Excel usando o Pandas e salvar no objeto HttpResponse
    df.to_excel(response, index=False)

    return response