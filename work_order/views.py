from datetime import datetime
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.messages import constants
from .models import Services, User, client, Employees, work_order as work_order_model, image
from finance.models import Finance
from config.models import Config
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO
import pytz
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
import pandas as pd
from django.contrib.auth.decorators import user_passes_test

br_tz = pytz.timezone('America/Sao_Paulo')
time_br = datetime.now(br_tz).time()


@login_required
def work_order(request):
    if request.method == "GET":
        workorders = work_order_model.objects.all()
        return render(request, 'work_order.html', {'workorders': workorders})
    else:
        return HttpResponseBadRequest('Invalid request method')


@login_required
def new_work_order(request):

    if request.method == "GET":
        list_client = client.objects.all()
        list_employee = Employees.objects.all()
        list_service = Services.objects.all()
        list_client = client.objects.all()
        user = request.user

        try:
            service = Services.objects.get(cod=id)
        except:
            service = ""
        try:
            tipo = Services.objects.get(cod=id).tipo
        except:
            tipo = ""
        hora = datetime.now().time()
        data = datetime.now().date().strftime("%Y-%m-%d")

        return render(request, 'new_work_order.html', {'list_client': list_client,
                                                       'list_employee': list_employee,
                                                       'list_service': list_service,
                                                       'data': data,
                                                       'hora': hora,
                                                       'user': user,
                                                       })

    elif request.method == "POST":

        if request.POST.get("pgto_adiantado") == None:
            pgto_adiantado = False
        else:
            pgto_adiantado = True
        if request.POST.get("os_finalizada") == None:
            os_finalizada = False
        else:
            os_finalizada = True

        cod_cli_str = request.POST.get("cod_cli")

        if not cod_cli_str:
            # Se o cod_cli estiver vazio, cria um novo objeto 'client'
            message = True
            nome = request.POST.get("cliente")
            whatsapp = request.POST.get("whatsapp")
            client_obj, created = client.objects.get_or_create(
                nome=nome,
                whatsapp=whatsapp,
                vendedor=request.user,
                data_nasc="1900-01-01",
                ativo=True,
            )
        else:
            message = False
            client_obj = client.objects.get(pk=cod_cli_str)

        work_orders = work_order_model(
            # Services.objects.get(cod=id)
            cod_cli=client_obj,
            cod_tec=Employees.objects.get(
                pk=request.POST.get("cod_tecnico")),
            cod_ser=Services.objects.get(pk=request.POST.get("cod_ser")),
            cod_user=request.user,
            whatsapp=request.POST.get("whatsapp"),
            status=request.POST.get("status"),
            obs_cli=request.POST.get("obs_cli"),
            produto=request.POST.get("produto"),
            marca=request.POST.get("marca"),
            modelo=request.POST.get("modelo"),
            serie=request.POST.get("serie"),
            condicao=request.POST.get("condicao"),
            acessorios=request.POST.get("acessorios"),
            defeito=request.POST.get("defeito"),
            obs_ser=request.POST.get("obs_ser"),
            solucao=request.POST.get("solucao"),
            preco=request.POST.get("preco"),
            desconto=request.POST.get("desconto"),
            acressimo=request.POST.get("acressimo"),
            total=request.POST.get("total"),
            modo_pgto=request.POST.get("modo_pgto"),
            data_alteracao=datetime.now().date().strftime("%Y-%m-%d"),
            pgto_adiantado=pgto_adiantado,
            os_finalizada=os_finalizada,
        )
        # if not client.objects.filter(pk=request.POST.get("cod_cli")).exists():
        if 'photos' in request.FILES:
            # percorre cada imagem enviada
            for photo in request.FILES.getlist('photos'):
                # cria um objeto image para cada imagem enviada
                image_obj = image(
                    photo=photo,
                    order=work_orders
                )
                image_obj.save()
        work_orders.save()

        if pgto_adiantado == True and request.POST.get("total") != '':

            finances = Finance.objects.all()

            obs = 'Pagamento adiantado da OS: ' + str(work_orders)
            nome = client.objects.get(pk=request.POST.get("cod_cli")).nome
            data = datetime.now().date().strftime("%Y-%m-%d")
            valor = request.POST.get("total")
            movimento = 'entrada'
            tipo_pgto = request.POST.get("modo_pgto")

            finances = Finance(
                obs=obs,
                nome=nome,
                data=data,
                valor=valor,
                movimento=movimento,
                hora=time_br,
                tipo_pgto=tipo_pgto,
            )
            finances.save()

            if message == True:
                messages.add_message(request, constants.SUCCESS,
                                     'Nova ordem de serviço criada, novo cliente cadastrado com sucesso e pagamento lançado no financeiro')
            else:
                messages.add_message(request, constants.SUCCESS,
                                     'Nova ordem de serviço criada com sucesso e pagamento lançado no financeiro')
        else:
            if message == True:
                messages.add_message(request, constants.SUCCESS,
                                     'Nova ordem de serviço criada e novo cliente cadastrado com sucesso')
            else:
                messages.add_message(request, constants.SUCCESS,
                                     'Nova ordem de serviço criada com sucesso')

        return redirect('work_order')
    else:
        return HttpResponseBadRequest('Invalid request method')


@login_required
def edit_work_order(request, id):
    list_client = client.objects.all()
    list_employee = Employees.objects.all()
    list_service = Services.objects.all()

    try:
        service = Services.objects.get(cod=id)
    except:
        service = ""
    try:
        tipo = Services.objects.get(cod=id).tipo
    except:
        tipo = ""

    if request.method == "GET":

        order = work_order_model.objects.get(id=id)
        fotos = image.objects.filter(order_id=id)
        # print(Services.objects.get(cod=id) )
        return render(request, 'edit_work_order.html', {
            'fotos': fotos,
            'id': id,
            'list_client': list_client,
            'list_employee': list_employee,
            'list_service': list_service,
            'nome': work_order_model.objects.get(id=id).cod_cli.nome,
            'whatsapp': work_order_model.objects.get(id=id).whatsapp,
            'data_entrada': work_order_model.objects.get(id=id).data_entrada,
            'hora_entrada': work_order_model.objects.get(id=id).data_entrada.strftime("%H:%M"),
            'cod_os': work_order_model.objects.get(id=id).pk,
            'cod_cli': work_order_model.objects.get(id=id).cod_cli.pk,
            'cod_tec': work_order_model.objects.get(id=id).cod_tec,
            'cod_ser': work_order_model.objects.get(id=id).cod_ser,
            'cod_user': work_order_model.objects.get(id=id).cod_user,
            'whatsapp': work_order_model.objects.get(id=id).whatsapp,
            'status': work_order_model.objects.get(id=id).status,
            'obs_cli': work_order_model.objects.get(id=id).obs_cli,
            'produto': work_order_model.objects.get(id=id).produto,
            'marca': work_order_model.objects.get(id=id).marca,
            'modelo': work_order_model.objects.get(id=id).modelo,
            'serie': work_order_model.objects.get(id=id).serie,
            'condicao': work_order_model.objects.get(id=id).condicao,
            'acessorios': work_order_model.objects.get(id=id).acessorios,
            'defeito': work_order_model.objects.get(id=id).defeito,
            'obs_ser': work_order_model.objects.get(id=id).obs_ser,
            'solucao': work_order_model.objects.get(id=id).solucao,
            'servico': service,
            'servico_tipo': tipo,
            'preco': work_order_model.objects.get(id=id).preco,
            'desconto': work_order_model.objects.get(id=id).desconto,
            'acressimo': work_order_model.objects.get(id=id).acressimo,
            'total': work_order_model.objects.get(id=id).total,
            'modo_pgto': work_order_model.objects.get(id=id).modo_pgto,
            'pgto_adiantado': work_order_model.objects.get(id=id).pgto_adiantado,
            'os_finalizada': work_order_model.objects.get(id=id).os_finalizada,
            'data_entrada': work_order_model.objects.get(id=id).data_entrada.strftime("%Y-%m-%d"),
            'data_saida': work_order_model.objects.get(id=id).data_saida,
            'data_alteracao': datetime.now().date(),
        })

    if request.method == "POST":

        pago = work_order_model.objects.get(id=id).pgto_adiantado

        work_orders = work_order_model.objects.get(id=id)

        work_orders.cod_cli = client.objects.get(
            pk=request.POST.get("cod_cli"))
        work_orders.cod_tec = Employees.objects.get(
            pk=request.POST.get("cod_tecnico"))
        work_orders.cod_ser = Services.objects.get(
            pk=request.POST.get("cod_ser"))

        work_orders.cod_user = request.user
        work_orders.whatsapp = request.POST.get("whatsapp")
        work_orders.status = request.POST.get("status")
        work_orders.obs_cli = request.POST.get("obs_cli")
        work_orders.produto = request.POST.get("produto")
        work_orders.marca = request.POST.get("marca")
        work_orders.modelo = request.POST.get("modelo")
        work_orders.serie = request.POST.get("serie")
        work_orders.condicao = request.POST.get("condicao")
        work_orders.acessorios = request.POST.get("acessorios")
        work_orders.defeito = request.POST.get("defeito")
        work_orders.obs_ser = request.POST.get("obs_ser")
        work_orders.solucao = request.POST.get("solucao")
        work_orders.preco = request.POST.get("preco")
        work_orders.desconto = request.POST.get("desconto")
        work_orders.acressimo = request.POST.get("acressimo")
        work_orders.total = request.POST.get("total")
        work_orders.modo_pgto = request.POST.get("modo_pgto")
        work_orders.data_alteracao = datetime.now().date().strftime("%Y-%m-%d")
        work_orders.pgto_adiantado = True if request.POST.get(
            "pgto_adiantado") and request.POST.get("total") != '' else False
        work_orders.os_finalizada = True if request.POST.get(
            "os_finalizada") else False

        if 'photos' in request.FILES:
            # percorre cada imagem enviada
            for photo in request.FILES.getlist('photos'):
                # cria um objeto image para cada imagem enviada
                image_obj = image(
                    photo=photo,
                    order=work_orders
                )
                image_obj.save()

        work_orders.save()

        if work_order_model.objects.get(id=id).pgto_adiantado == True and request.POST.get("total") != '' and pago == False:

            finances = Finance.objects.all()

            obs = 'Pagamento adiantado da OS: ' + str(work_orders)  # .cod
            nome = client.objects.get(pk=request.POST.get("cod_cli")).nome
            data = datetime.now().date().strftime("%Y-%m-%d")
            valor = request.POST.get("total")
            movimento = 'entrada'
            tipo_pgto = request.POST.get("modo_pgto")

            finances = Finance(
                obs=obs,
                nome=nome,
                data=data,
                valor=valor,
                movimento=movimento,
                hora=time_br,
                tipo_pgto=tipo_pgto,
            )
            finances.save()

            messages.add_message(request, constants.SUCCESS,
                                 'Nova ordem se serviço editada com sucesso e pagamento lançado no financeiro')
        else:
            messages.add_message(request, constants.SUCCESS,
                                 'Nova ordem se serviço editada com sucesso')

        return redirect('work_order')
    else:
        return HttpResponseBadRequest('Invalid request method')


@ login_required
def del_work_order(request, id):
    order = work_order_model.objects.get(id=id)
    order.delete()
    messages.add_message(request, constants.SUCCESS,
                         'Ordem de serviço apagada com sucesso')
    return redirect('work_order')


@ login_required
def cupon(request, id):

    config = Config.objects.get(id=2)
    order = work_order_model.objects.get(id=id)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="coupon.pdf"'

    # Define as informações do cupom
    company_name = config.nome_empresa
    company_address = f'{config.endereco}, {config.numero}'
    company_city = f'{config.cidade}, {config.estado}'
    company_phone = f'Tel: {config.telefone}'
    company_whastapp = f'Whatsapp: {config.whatsapp}'
    customer_name = order.cod_cli.nome
    customer_whatsapp = order.whatsapp
    customer_os = order.pk

    customer_data_entrada = order.data_entrada.strftime("%d-%m-%Y")
    # customer_data_saida = (order.data_alteracao)
    customer_data_saida = datetime.now().date().strftime("%d-%m-%y")

    service_details = f'{order.cod_ser.nome}'
    line1 = f'Produto: {order.produto}'
    line2 = f'Marca: {order.marca}'
    line3 = f'Modelo: {order.modelo}'
    line4 = f'Série: {order.serie}'
    line5 = f'Condição: {order.condicao}'
    line6 = f'Acessórios: {order.acessorios}'
    line7 = f'Defeito: {order.defeito}'
    line8 = f'Observação: {order.obs_cli}'
    line9 = f'Solução: {order.solucao}'
    line10 = f'Preço: R$ {order.preco},00'
    line11 = f'Desconto: R$ {order.desconto},00'
    line12 = f'Acréscimo: R$ {order.acressimo},00'
    if order.pgto_adiantado == True:
        line13 = f'Serviço pago'
    else:
        line13 = f''
    total = f'Total: {order.total}'

    # Cria um objeto PDF com o ReportLab
    # Cria um objeto PDF com o ReportLab
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=(80, 250))  # alterado para 80x250

    # Adiciona a logo da empresa
    photo_path = config.logo1
    photo = ImageReader(photo_path)
    width, height = photo.getSize()
    ratio = width / height
    pdf.drawImage(photo, 10, 230, width=50, height=50 /
                  ratio)  # alterado posição Y para 230

    # Adiciona as informações da empresa
    pdf.setFont('Helvetica', 4)
    pdf.drawString(5, 220, company_name)
    pdf.drawString(5, 215, company_address)
    pdf.drawString(5, 210, company_city)
    pdf.drawString(5, 205, company_phone)
    pdf.drawString(5, 200, company_whastapp)
    pdf.line(0, 195, 200, 195)

    # Adiciona as informações do cliente e do serviço
    pdf.setFont('Helvetica-Bold', 4)
    pdf.drawString(5, 185, 'OS: {}'.format(customer_os))
    pdf.drawString(5, 180, 'Nome: {}'.format(customer_name))
    pdf.drawString(5, 175, 'Tel: {}'.format(customer_whatsapp))
    pdf.drawString(5, 170, 'Entrada: {}'.format(customer_data_entrada))
    pdf.drawString(5, 165, 'Impressão: {}'.format(customer_data_saida))
    pdf.line(0, 160, 200, 160)
    pdf.setFont('Helvetica', 4)

    pdf.drawString(5, 150, 'Detalhes do Produto:')
    pdf.drawString(5, 145, service_details)
    pdf.drawString(5, 140, line1)
    pdf.drawString(5, 135, line2)
    pdf.drawString(5, 130, line3)
    pdf.drawString(5, 125, line4)
    pdf.drawString(5, 120, line5)
    pdf.drawString(5, 115, line6)
    pdf.drawString(5, 110, line7)
    pdf.drawString(5, 105, line8)
    pdf.line(0, 100, 200, 100)
    pdf.drawString(5, 90, 'Detalhes do Serviço:')
    pdf.drawString(5, 85, line9)
    pdf.drawString(5, 80, line10)
    pdf.drawString(5, 75, line11)
    pdf.drawString(5, 70, line12)
    pdf.line(0, 60, 200, 60)

    # Adiciona o total do cupom
    pdf.setFont('Helvetica-Bold', 7)
    pdf.drawString(5, 45, f'{line13}')
    pdf.drawString(5, 35, f'{total}')  # alterado posição Y para 45

    # Fecha o objeto PDF
    pdf.showPage()
    pdf.save()

    # Converte o PDF para uma string de bytes
    buffer.seek(0)
    pdf_data = buffer.getvalue()

    # Retorna a resposta HTTP com o PDF como conteúdo
    response = HttpResponse(pdf_data, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="coupon.pdf"'
    return response


@ login_required
def print(request, id):

    config = Config.objects.get(id=2)
    order = work_order_model.objects.get(id=id)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="coupon.pdf"'

    # Define as informações do cupom
    company_name = config.nome_empresa
    company_address = f'{config.endereco}, {config.numero}'
    company_city = f'{config.cidade}, {config.estado}'
    company_phone = f'Tel: {config.telefone}'
    company_whatsapp = f'Whatsapp: {config.whatsapp}'
    customer_name = order.cod_cli.nome
    customer_whatsapp = order.whatsapp
    customer_os = order.pk

    if order.os_finalizada == True:
        customer_final = 'Finalizada'
    else:
        customer_final = 'Aberta'

    customer_data_entrada = order.data_entrada.strftime("%d-%m-%Y")
    customer_data_saida = datetime.now().date().strftime("%d-%m-%y")

    service_details = f'{order.cod_ser.nome}'
    line1 = f'Produto: {order.produto}'
    line2 = f'Marca: {order.marca}'
    line3 = f'Modelo: {order.modelo}'
    line4 = f'Série: {order.serie}'
    line5 = f'Condição: {order.condicao}'
    line6 = f'Acessórios: {order.acessorios}'
    line7 = f'Defeito: {order.defeito}'
    line8 = f'Observação: {order.obs_cli}'
    line9 = f'Solução: {order.solucao}'
    line10 = f'Preço: R$ {order.preco},00'
    line11 = f'Desconto: R$ {order.desconto},00'
    line12 = f'Acréscimo: R$ {order.acressimo},00'
    if order.pgto_adiantado == True:
        line13 = f'Serviço pago'
    else:
        line13 = f'Serviço não pago'
    total = f'Total: {order.total}'

    # Cria um objeto PDF com o ReportLab
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)

    # Adiciona a logo da empresa
    photo_path = config.logo1
    photo = ImageReader(photo_path)
    width, height = photo.getSize()
    ratio = width / height
    pdf.drawImage(photo, 20*mm, 270*mm, width=150, height=150/ratio)

    # Adiciona as informações da empresa
    pdf.setFont('Helvetica', 8)
    pdf.drawCentredString(105*mm, 280*mm, company_name)
    pdf.drawCentredString(105*mm, 275*mm, company_address)
    pdf.drawCentredString(105*mm, 270*mm, company_city)
    pdf.drawCentredString(105*mm, 265*mm, company_phone)
    pdf.drawCentredString(105*mm, 260*mm, company_whatsapp)

    # Adiciona as informações do cliente e do serviço
    pdf.setFont('Helvetica-Bold', 8)
    pdf.drawRightString(190*mm, 280*mm, f'OS: {customer_os}')
    pdf.drawRightString(
        190*mm, 275*mm, f'Data de entrada: {customer_data_entrada}')
    pdf.drawRightString(
        190*mm, 270*mm, f'Data de saída: {customer_data_saida}')
    pdf.drawRightString(190*mm, 265*mm, f'Os {customer_final}')
    pdf.drawRightString(190*mm, 260*mm, line13)

    pdf.setFont('Helvetica', 8)
    pdf.drawString(20*mm, 250*mm, f'Cliente: {customer_name}')
    pdf.drawString(20*mm, 245*mm, f'Whatsapp: {customer_whatsapp}')
    pdf.drawString(20*mm, 240*mm, f'Serviço: {service_details}')
    pdf.setFont('Helvetica-Bold', 8)
    pdf.drawString(90*mm, 250*mm, line1)
    pdf.drawString(90*mm, 245*mm, line2)
    pdf.drawString(90*mm, 240*mm, line3)
    pdf.drawString(90*mm, 235*mm, line4)
    pdf.drawString(90*mm, 230*mm, line5)
    pdf.drawString(90*mm, 225*mm, line6)
    pdf.drawString(90*mm, 220*mm, line7)
    pdf.drawString(90*mm, 215*mm, line8)
    pdf.drawString(90*mm, 210*mm, line9)
    pdf.setFont('Helvetica', 8)
    pdf.drawRightString(190*mm, 250*mm, line10)
    pdf.drawRightString(190*mm, 245*mm, line11)
    pdf.drawRightString(190*mm, 240*mm, line12)
    pdf.setFont('Helvetica-Bold', 8)
    pdf.drawRightString(190*mm, 235*mm, line13)
    pdf.setFont('Helvetica-Bold', 10)
    pdf.drawRightString(190*mm, 230*mm, total)

    # Fecha o objeto PDF
    pdf.showPage()
    pdf.save()

    # Define o tamanho do buffer
    buffer.seek(0)

    # Define o conteúdo do arquivo como o buffer
    response.write(buffer.getvalue())

    # Fecha o buffer
    buffer.close()

    return response


@user_passes_test(lambda u: u.is_superuser)
def wo_xlr(request):
    # Pegar os dados da tabela workorders
    workorders = work_order_model.objects.all()

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
