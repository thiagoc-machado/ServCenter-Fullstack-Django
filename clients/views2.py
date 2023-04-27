from django.http import HttpResponse
from django.shortcuts import render
from .forms import FormClient
from django.contrib import messages
from django.contrib.messages import constants
from django.contrib.auth.decorators import login_required
from .models import client
from django.shortcuts import redirect


@login_required
def clients(request):
    if request.method == "GET":
        # return HttpResponse("clients")
        cli = client.objects.all()
        return render(request, 'clients.html', {'cli': cli})


@login_required
def new_client(request):
    if request.method == "GET":
        form = FormClient
        return render(request, 'new_client.html', {'form': form})
    elif request.method == "POST":
        form = FormClient(request.POST)

        if form.is_valid():
            form.save()
            messages.add_message(request, constants.SUCCESS,
                                 'Novo cliente cadastrado com sucesso')
            return redirect('clients')
        else:
            messages.add_message(request, constants.ERROR,
                                 'Verifique os dados inseridos')
            return render(request, 'new_client.html', {'form': form})


@login_required
def del_cli(request, cod_cli):
    cli = client.objects.get(cod_cli=cod_cli)
    cli.delete()
    messages.add_message(request, constants.SUCCESS,
                         'Cliente apagado com sucesso')
    return redirect('clients')
    # return HttpResponse(cod_cli)


@login_required
def edit_client(request, cod_cli):
    client_obj = client.objects.get(cod_cli=cod_cli)
    if request.method == 'GET':
        form = FormClient(instance=client_obj)
        return render(request, 'edit_client.html', {'form': form, 'client_obj': client_obj})
    elif request.method == 'POST':
        form = FormClient(request.POST, instance=client_obj)
        if form.is_valid():
            form.save()
            messages.add_message(request, constants.SUCCESS,
                                 'Cliente atualizado com sucesso')
            return redirect('clients')
        else:
            messages.add_message(request, constants.ERROR,
                                 'Erro ao atualizar cliente')
            return render(request, 'edit_client.html', {'form': form, 'client_id': client_obj.cod_cli})
