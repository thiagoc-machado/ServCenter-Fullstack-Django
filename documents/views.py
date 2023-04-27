from django.shortcuts import render, redirect, get_object_or_404
from .models import Documents
import uuid
import os
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.conf import settings
from django.contrib import messages
from django.contrib.messages import constants
from datetime import datetime
from django.http import HttpResponse, Http404
import mimetypes


def documents(request):
    if request.method == 'GET':
        documents = Documents.objects.all()
        data = datetime.now().date().strftime("%Y-%m-%d")
        return render(request, 'documents.html', {'documents': documents, 'data': data})

    if request.method == 'POST':
        nome = request.POST.get('nome')
        texto = request.POST.get('texto')
        arquivo = request.FILES.get('arquivo')
        data = request.POST.get('data')
        obs = request.POST.get('obs')

        if arquivo is not None and isinstance(arquivo, InMemoryUploadedFile) and arquivo.size > 0:
            ext = arquivo.name.split('.')[-1]
            nome_arquivo = f'{uuid.uuid4()}.{ext}'
            with open(os.path.join(settings.MEDIA_ROOT, 'documents', nome_arquivo), 'wb') as f:

                for chunk in arquivo.chunks():
                    f.write(chunk)

            doc = Documents(nome=nome, texto=texto,
                    arquivo='documents/' + nome_arquivo, data=data, obs=obs)
            doc.save()
            messages.add_message(request, constants.SUCCESS,
                                 'Novo arquivo carregado com sucesso')
            return redirect('documents')

    return redirect('documents')


def download_documents(request, id):
    doc = get_object_or_404(Documents, id=id)
    filename = os.path.basename(doc.arquivo.name)
    filepath = os.path.join(settings.MEDIA_ROOT, doc.arquivo.name)
    with open(filepath, 'rb') as f:
        response = HttpResponse(
            f.read(), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response


def view_documents(request, id):
    doc = Documents.objects.get(id=id)
    if doc.arquivo:
        tipo_arquivo, encoding = mimetypes.guess_type(doc.arquivo.path) 
    else:
        tipo_arquivo = ''
     
    print(tipo_arquivo)
    
    if 'image' in str(tipo_arquivo) or tipo_arquivo == 'application/pdf' or  tipo_arquivo == 'text/plain':
        is_image = tipo_arquivo.startswith('image/')
        context = {
            'doc': doc,
            'is_image': is_image,
            'tipo_arquivo': tipo_arquivo
        }
        return render(request, 'view_documents.html', context)
    
    messages.add_message(request, constants.ERROR,
                         'Arquivo não suportado')
    return redirect('documents')


def del_documents(request, id):
    doc = Documents.objects.get(id=id)
    # Obtenha o caminho completo do arquivo
    arquivo = os.path.join(settings.MEDIA_ROOT, doc.arquivo.name)
    # Apague o arquivo do disco
    os.remove(arquivo)
    # Apague o registro do banco de dados
    doc.delete()
    messages.add_message(request, constants.SUCCESS,
                         'Documento apagado com sucesso')
    return redirect('documents')
