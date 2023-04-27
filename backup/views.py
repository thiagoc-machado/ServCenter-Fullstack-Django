from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse, FileResponse
from django.core import management
from django.shortcuts import render, redirect
import os
from django.conf import settings
from django.db import connection
import time
from django.contrib import messages
from django.contrib.messages import constants
from django.core import management
from io import StringIO
import zipfile
from wsgiref.util import FileWrapper
import pandas as pd
import sqlite3
from datetime import datetime
from django.core.management import call_command
from io import BytesIO
import shutil
from django.core.files.storage import default_storage
from django.core.files.uploadedfile import InMemoryUploadedFile

@user_passes_test(lambda u: u.is_superuser)
def backup(request):
    response = HttpResponse(content_type='application/x-sqlite3')
    response['Content-Disposition'] = 'attachment; filename="backup.db"'
    management.call_command('dbbackup', stdout=response)
    response = FileResponse(response, as_attachment=True)
    context = {'backup_success': True}
    delete_backup_files(request)
    return render(request, 'backup.html', context)

@user_passes_test(lambda u: u.is_superuser)
def backup_sqlite(request):
    backup_filename = 'backup.dump'
    backup_path = os.path.join('media', 'backup', backup_filename)

    management.call_command('dbbackup', output_path=backup_path)

    if os.path.exists(backup_path):
        with open(backup_path, 'rb') as f:
            response = HttpResponse(
                f.read(), content_type='application/x-sqlite3')
            response['Content-Disposition'] = f'attachment; filename="{backup_filename}"'
            messages.add_message(request, constants.SUCCESS,
                                'Backup realizado com sucesso!')
            return response
    else:
        messages.add_message(request, constants.ERROR,
                            'Erro ao efetuar o backup, Nenhum arquivo encontrado!')
        return redirect('backup')


@user_passes_test(lambda u: u.is_superuser)
def restore_backup(request):
    if request.method == 'POST':
        if 'backup' not in request.FILES:
            return HttpResponse('Arquivo de backup não enviado. Por favor, tente novamente.')

        backup_file: InMemoryUploadedFile = request.FILES['backup']
        backup_file: InMemoryUploadedFile = request.FILES['backup']

        # Crie um diretório temporário para extrair o arquivo ZIP
        temp_extract_path = os.path.join(settings.MEDIA_ROOT, 'temp_extract')
        os.makedirs(temp_extract_path, exist_ok=True)

        # Extraia o arquivo ZIP para o diretório temporário
        with zipfile.ZipFile(backup_file, 'r') as backup_zip:
            backup_zip.extractall(temp_extract_path)

        # Restaure o banco de dados usando o arquivo de backup extraído
        db_backup_path = os.path.join(temp_extract_path, 'backup.dump')
        call_command('dbrestore', input_path=db_backup_path)

        # Copie os arquivos de mídia extraídos para o diretório de mídia do Django
        media_root_len = len(settings.MEDIA_ROOT)
        for root, dirs, files in os.walk(temp_extract_path):
            for file in files:
                if file != 'backup.dump':
                    file_path = os.path.join(root, file)
                    destination_path = os.path.join(settings.MEDIA_ROOT, file_path[media_root_len:])
                    # Copie o arquivo para o diretório de mídia, preservando a estrutura do diretório
                    default_storage.save(destination_path, default_storage.open(file_path))

        # Limpe o diretório temporário
        shutil.rmtree(temp_extract_path)
        messages.add_message(request, constants.SUCCESS,
                                 'Restauração de backup realizado com sucesso!')
        return HttpResponse('Restauração concluída com sucesso.')
    else:
        messages.add_message(request, constants.ERROR,
                                 'Restauração não concluída.')
        return render(request, 'backup.html')  # Renderize a página de upload do arquivo ZIP

@user_passes_test(lambda u: u.is_superuser)
def backup_download(request):
    data = datetime.now().strftime('%d %m %Y')
    backup_filename = f'backup {data}.zip'
    backup_path = os.path.join(settings.MEDIA_ROOT, 'backup', backup_filename)
    print ('Backup [*      ]')
    # cria um arquivo zip que inclui o arquivo de backup e a pasta de mídia
    with zipfile.ZipFile(backup_path, 'w', compression=zipfile.ZIP_DEFLATED) as backup_zip:
        # adiciona o arquivo de backup ao arquivo zip
        db_backup_path = os.path.join(
            settings.MEDIA_ROOT, 'backup', 'backup.dump')
        print ('Backup [**     ]')
        management.call_command('dbbackup', output_path=db_backup_path)
        print ('Backup [***    ]')
        backup_zip.write(db_backup_path, 'backup.dump')
        print ('Backup [****   ]')
        # adiciona a pasta de mídia ao arquivo zip
        media_root_len = len(settings.MEDIA_ROOT)
        print ('Backup [*****  ]')
        for root, dirs, files in os.walk(settings.MEDIA_ROOT):
            for file in files:
                file_path = os.path.join(root, file)
                # remove o prefixo do caminho da pasta de mídia
                zip_path = file_path[media_root_len:]
                print(f"Adding file to zip: {file_path} as {zip_path}")
                backup_zip.write(file_path, zip_path)
        print ('Backup [****** ]')
        
    if os.path.exists(backup_path):
        with open(backup_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/zip')
            response['Content-Disposition'] = f'attachment; filename="{backup_filename}"'
            messages.add_message(request, constants.SUCCESS,
                                 'Backup realizado com sucesso!')
            print ('Backup [*******]')

            return response
        
    else:
        messages.add_message(request, constants.ERROR,
                             'Erro ao efetuar o backup, Nenhum arquivo encontrado!')
        return redirect('backup')

@user_passes_test(lambda u: u.is_superuser)
def restore(request):
    backup_file = request.FILES.get('backup_file')
    confirm_restore = request.POST.get('confirm_restore')

    if backup_file and confirm_restore == "CONFIRMAR":
        connection.close()
        time.sleep(2)
        backup_path = os.path.join(
            settings.MEDIA_ROOT, 'backup', backup_file.name)
        with open(backup_path, 'wb') as f:
            for chunk in backup_file.chunks():
                f.write(chunk)

        # Add these lines to disable the prompt for confirmation
        in_buffer = StringIO('yes\n')
        out_buffer = StringIO()
        with open(backup_path, 'rb') as backup_file:
            management.call_command("dbrestore", database='default',
                                    input_filename=backup_path, interactive=False)

        try:
            os.remove(backup_path)
        except PermissionError:
            # Tenta remover o arquivo várias vezes, esperando entre cada tentativa
            for i in range(10):
                try:
                    os.remove(backup_path)
                    break  # Sai do loop se conseguir remover o arquivo
                except PermissionError:
                    # Espera um segundo antes de tentar novamente
                    time.sleep(1)
        try:
            time.sleep(2)
            connection.connect()
            messages.add_message(request, constants.SUCCESS,
                                 'Backup Restaurado com sucesso!')
            return redirect('backup')
        except Exception as e:
            messages.add_message(request, constants.ERROR,
                                 f'Erro ao restaurar backup: {str(e)}, status=500')
            return redirect('backup')
    elif backup_file:
        messages.add_message(request, constants.ERROR,
                             'Por favor, confirme a restauração digitando "CONFIRMAR".')
    else:
        messages.add_message(request, constants.ERROR,
                             'Nenhum arquivo de backup enviado!')
    return redirect('backup')

@user_passes_test(lambda u: u.is_superuser)
def export_to_excel(request):

    # Connect to SQLite database
    conn = sqlite3.connect('nome_do_banco_de_dados.db')

    # Get list of table names
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    table_names = cursor.fetchall()
    cursor.close()

    # Create a Pandas Excel writer
    writer = pd.ExcelWriter('backup.xlsx', engine='xlsxwriter')

    # Loop through tables and add to Excel file
    for table_name in table_names:
        # Create a DataFrame from table in SQLite database
        df = pd.read_sql_query(f"SELECT * FROM {table_name[0]}", conn)

        # Add DataFrame to Excel writer
        df.to_excel(writer, sheet_name=table_name[0], index=False)

    # Close Excel writer
    writer.close()

    # Close database connection
    conn.close()

    # Send Excel file as a download
    file_path = os.path.abspath('backup.xlsx')
    with open(file_path, 'rb') as file:
        response = HttpResponse(file, content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = f'attachment; filename={os.path.basename(file_path)}'
    return response

@user_passes_test(lambda u: u.is_superuser)
def delete_backup_files(request):
    backup_folder = os.path.join(settings.MEDIA_ROOT, 'backup')
    for filename in os.listdir(backup_folder):
        file_path = os.path.join(backup_folder, filename)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
        except Exception as e:
            print(f'Erro ao excluir o arquivo: {file_path}. Erro: {e}')
            
