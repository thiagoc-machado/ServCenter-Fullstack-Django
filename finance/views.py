from django.shortcuts import render, redirect
from django.contrib.messages import constants
from django.contrib import messages
from django.http import HttpResponse, HttpResponseBadRequest
from finance.models import Finance, Categoria_in, Categoria_out, Caixa
from datetime import date, datetime, timedelta
from django.contrib.auth.decorators import user_passes_test, login_required
import pytz
import pandas as pd
from django.utils import timezone
import matplotlib.pyplot as plt
from io import BytesIO
import json
from django.db.models import Sum


@user_passes_test(lambda u: u.is_superuser)
def finance(request):
    if request.method == 'POST':
        deposits = request.POST.get('deposits')
        if deposits != '':
            total_deposit = 0
            if Caixa.objects.aggregate(total=Sum('deposits'))['total'] != None:
                total_deposit = Caixa.objects.aggregate(total=Sum('deposits'))[
                    'total'] + float(deposits) or 0
                total_deposits = 'R$ {:.2f}'.format(float(total_deposit))
            else:
                total_deposits = 0
            caixa = Caixa.objects.all()

            tot = tot_in()
            saldo = tot - total_deposit
            caixa = Caixa(deposits=deposits, date=date.today(),
                        obs='Depósito', saldo='R$ {:.2f}'.format(float(saldo)))
            caixa.save()
            messages.add_message(request, constants.SUCCESS,
                                'Depósito lançado com sucesso!')
        else:
            messages.add_message(request, constants.ERROR,
                                'Nenhum valor foi inserido!')

        return redirect('/finance')
    else:
        br_tz = pytz.timezone('America/Sao_Paulo')
        today = timezone.localtime(timezone=br_tz).date()
        finance = Finance.objects.all

        total_dia = '{:.2f}'.format(diario()[0])
        entrada_dia = '{:.2f}'.format(diario()[2])
        saida_dia = '{:.2f}'.format(diario()[1])

        total_sem = '{:.2f}'.format(semanal()[0])
        entrada_sem = '{:.2f}'.format(semanal()[2])
        saida_sem = '{:.2f}'.format(semanal()[1])

        total_mes = '{:.2f}'.format(mensal()[0])
        entrada_mes = '{:.2f}'.format(mensal()[2])
        saida_mes = '{:.2f}'.format(mensal()[1])

        total_ano = '{:.2f}'.format(anual()[0])
        entrada_ano = '{:.2f}'.format(anual()[2])
        saida_ano = '{:.2f}'.format(anual()[1])

        chart = finance_chart()
        chart_ano = finance_year_chart()
        # pie_mes_in = pie_chart_mes_in()
        # pie_ano_in = pie_chart_ano_in()
        # pie_mes_out = pie_chart_mes_out()
        # pie_ano_out = pie_chart_ano_out()
        dates, entradas, saidas = finance_chart()

        caixas_do_dia = Caixa.objects.filter(date=today).aggregate(
            total=Sum('deposits'))['total'] or 0

        total_deposit = Caixa.objects.aggregate(
            total=Sum('deposits'))['total'] or 0
        total_dep = Caixa.objects.aggregate(total=Sum('deposits'))['total']
        total_deposits = 'R$ {:.2f}'.format(float(total_deposit))

        tot = tot_in()
        if total_dep == None:
            total_dep = 0
        gaveta = tot - total_dep

        pizza_chart_mes_in = pie_chart_mes_in()
        pizza_chart_ano_in = pie_chart_ano_in()
        pizza_chart_mes_out = pie_chart_mes_out()
        pizza_chart_ano_out = pie_chart_ano_out()
        payment_day_data = pie_chart_dia_pgto()
        payment_month_data = pie_chart_mes_pgto()
        print("pizza_chart_mes_in", pizza_chart_mes_in)
        return render(request, 'finance.html',
                        {
                            'finance': finance,
                            'gaveta': '{:.2f}'.format(gaveta),
                            'caixas_do_dia': '{:.2f}'.format(caixas_do_dia),
                            'saidas_json': json.dumps(saidas),
                            'entradas_json': json.dumps(entradas),
                            'dates_json': json.dumps(dates),
                            'finance': finance,
                            'total_dia': total_dia,
                            'total_sem': total_sem,
                            'total_mes': total_mes,
                            'total_ano': total_ano,
                            'saida_ano': saida_ano,
                            'entrada_ano': entrada_ano,
                            'entrada_dia': entrada_dia,
                            'saida_dia': saida_dia,
                            'entrada_sem': entrada_sem,
                            'saida_sem': saida_sem,
                            'entrada_mes': entrada_mes,
                            'saida_mes': saida_mes,
                            'dates': chart[0],
                            'entradas': chart[1],
                            'saidas': chart[2],
                            'months': chart_ano[0],
                            'in_mes': chart_ano[1],
                            'out_mes': chart_ano[2],
                            'pie_chart_mes_in': pizza_chart_mes_in,
                            'pie_chart_mes_out': pizza_chart_mes_out,
                            'pie_chart_data_ano': pizza_chart_ano_in,
                            'pie_chart_data_ano_out': pizza_chart_ano_out,
                            'payment_day_data': json.dumps(payment_day_data),
                            'payment_month_data': json.dumps(payment_month_data),
                            # 'pie_mes_in': pie_mes_in[0],
                            # 'data_mes_in': pie_mes_in[1],
                            # 'value_mes_in': pie_mes_in[2],
                            # 'pie_mes_out': pie_mes_out[0],
                            # 'data_mes_out': pie_mes_out[1],
                            # 'value_mes_out': pie_mes_out[2],
                            # 'pie_ano_in': pie_ano_in[0],
                            # 'data_ano_in': pie_ano_in[1],
                            # 'value_ano_in': pie_ano_in[2],
                            # 'pie_ano_out': pie_ano_out[0],
                            # 'data_ano_out':pie_ano_out[1],
                            # 'value_ano_out': pie_ano_out[2],
                        })


@login_required
def finance_dia(request):
    if request.method == 'POST':

        deposits = request.POST.get('deposits')
        if deposits != '':
            if Caixa.objects.aggregate(total=Sum('deposits'))['total'] != None:
                total_deposit = Caixa.objects.aggregate(total=Sum('deposits'))[
                    'total'] + float(deposits) or 0
                total_deposits = 'R$ {:.2f}'.format(float(total_deposit))
            else:
                total_deposit = 0

            caixa = Caixa.objects.all()

            tot = tot_in()
            saldo = tot - total_deposit
            caixa = Caixa(deposits=deposits, date=date.today(),
                            obs='Depósito', saldo='R$ {:.2f}'.format(float(saldo)))
            caixa.save()
            messages.add_message(request, constants.SUCCESS,
                                    'Depósito lançado com sucesso!')
        else:
            messages.add_message(request, constants.ERROR,
                                    'Nenhum valor foi inserido!')

        return redirect('finance_dia')
    else:

        br_tz = pytz.timezone('America/Sao_Paulo')
        today = timezone.localtime(timezone=br_tz).date()
        finance = Finance.objects.filter(data=today)
        finance_all = Finance.objects.all()
        qtd = finance.count()
        finance_sum = 0
        finance_min = 0
        for finances in Finance.objects.filter(data=today):
            if finances.movimento == 'entrada':
                valor = finances.valor if finances.valor else 0
                if valor is not None:
                    valor = float(valor.replace('R$', '').replace(',', '.')) # type: ignore
                    finance_sum += valor
            elif finances.movimento == 'saída':
                valor = finances.valor if finances.valor else 0
                if valor is not None:
                    valor = float(valor.replace('R$', '').replace(',', '.')) # type: ignore
                    finance_min -= valor

        finance_minus = finance_min * -1
        finance_tot = finance_sum - finance_minus
        finance_total = round(finance_tot, 2)

        caixas_do_dia = Caixa.objects.filter(date=today).aggregate(
            total=Sum('deposits'))['total'] or 0

        total_deposit = Caixa.objects.aggregate(
            total=Sum('deposits'))['total'] or 0
        total_dep = Caixa.objects.aggregate(total=Sum('deposits'))['total']
        total_deposits = 'R$ {:.2f}'.format(float(total_deposit))

        tot = tot_in()
        if total_dep == None:
            total_dep = 0
        gaveta = tot - total_dep
        gaveta = tot - total_dep
        return render(request, 'finance_dia.html', {'finance': finance,
                                                    'finance_all': finance_all,
                                                    'finance_sum': '{:.2f}'.format(finance_sum),
                                                    'finance_minus': '{:.2f}'.format(finance_minus),
                                                    'finance_total': '{:.2f}'.format(finance_total),
                                                    'qtd': qtd,
                                                    'caixas_do_dia': '{:.2f}'.format(caixas_do_dia),
                                                    'gaveta': '{:.2f}'.format(gaveta),
                                                    })


@user_passes_test(lambda u: u.is_superuser)
def finance_sem(request):
    today = datetime.now().date()
    start_of_week = today - timedelta(days=today.weekday())

    finance = Finance.objects.filter(data__gte=start_of_week)

    finance_sum = 0
    finance_min = 0
    for finances in Finance.objects.filter(data__gte=start_of_week):
        if finances.movimento == 'entrada':
            valor = finances.valor if finances.valor else 0
            if valor is not None:
                valor = float(valor.replace('R$', '').replace(',', '.')) # type: ignore
                finance_sum += valor
        elif finances.movimento == 'saída':
            valor = finances.valor if finances.valor else 0
            if valor is not None:
                valor = float(valor.replace('R$', '').replace(',', '.')) # type: ignore
                finance_min -= valor
    finance_minus = finance_min * -1
    finance_tot = finance_sum - finance_minus
    finance_total = round(finance_tot, 2)

    return render(request, 'finance_sem.html', {'finance': finance,
                                                'finance_sum': '{:.2f}'.format(finance_sum),
                                                'finance_minus': '{:.2f}'.format(finance_minus),
                                                'finance_total': '{:.2f}'.format(finance_total),
                                                })


@user_passes_test(lambda u: u.is_superuser)
def finance_mes(request):
    today = date.today()
    start_of_month = today.replace(day=1)

    finance = Finance.objects.filter(data__gte=start_of_month)

    finance_sum = 0
    finance_min = 0
    for finances in Finance.objects.filter(data__gte=start_of_month):
        if finances.movimento == 'entrada':
            valor = finances.valor if finances.valor else 0
            if valor is not None:
                valor = float(valor.replace('R$', '').replace(',', '.')) # type: ignore
                finance_sum += valor
        elif finances.movimento == 'saída':
            valor = finances.valor if finances.valor else 0
            if valor is not None:
                valor = float(valor.replace('R$', '').replace(',', '.')) # type: ignore
                finance_min -= valor
    finance_minus = finance_min * -1
    finance_tot = finance_sum - finance_minus
    finance_total = finance_tot

    return render(request, 'finance_mes.html', {'finance': finance,
                                                'finance_sum': '{:.2f}'.format(finance_sum),
                                                'finance_minus': '{:.2f}'.format(finance_minus),
                                                'finance_total': '{:.2f}'.format(finance_total),
                                                })


@user_passes_test(lambda u: u.is_superuser)
def finance_ano(request):
    year = date.today().year
    finance = Finance.objects.filter(data__year=year)

    finance_sum = 0
    finance_min = 0
    for finances in Finance.objects.filter(data__year=year):
        if finances.movimento == 'entrada':
            valor = finances.valor if finances.valor else 0
            if valor is not None:
                valor = float(valor.replace('R$', '').replace(',', '.')) # type: ignore
                finance_sum += valor
        elif finances.movimento == 'saída':
            valor = finances.valor if finances.valor else 0
            if valor is not None:
                valor = float(valor.replace('R$', '').replace(',', '.')) # type: ignore
                finance_min -= valor
    finance_minus = finance_min * -1
    finance_tot = finance_sum - finance_minus
    finance_total = round(finance_tot, 2)

    return render(request, 'finance_ano.html', {'finance': finance,
                                                'finance_sum': '{:.2f}'.format(finance_sum),
                                                'finance_minus': '{:.2f}'.format(finance_minus),
                                                'finance_total': '{:.2f}'.format(finance_total),
                                                })


@user_passes_test(lambda u: u.is_superuser)
def finance_tot(request):
    finance = Finance.objects.all()

    finance_sum = 0
    finance_min = 0
    for finances in Finance.objects.all():
        if finances.movimento == 'entrada':
            valor = finances.valor if finances.valor else 0
            if valor is not None:
                valor = float(valor.replace('R$', '').replace(',', '.')) # type: ignore
                finance_sum += valor
        elif finances.movimento == 'saída':
            valor = finances.valor if finances.valor else 0
            if valor is not None:
                valor = float(valor.replace('R$', '').replace(',', '.')) # type: ignore
                finance_min -= valor
    finance_minus = finance_min * -1
    finance_tot = finance_sum - finance_minus
    finance_total = round(finance_tot, 2)

    return render(request, 'finance_tot.html', {'finance': finance,
                                                'finance_sum': '{:.2f}'.format(finance_sum),
                                                'finance_minus': '{:.2f}'.format(finance_minus),
                                                'finance_total': '{:.2f}'.format(finance_total),
                                                })


@login_required
def new_finance(request):
    br_tz = pytz.timezone('America/Sao_Paulo')
    time_br = datetime.now(br_tz).time()
    if request.method == "GET":
        data = timezone.localtime(timezone=br_tz).date().strftime('%Y-%m-%d')
        finances = Finance.objects.all()
        categoria = Categoria_in.objects.all()
        return render(request, 'new_finance.html', {'finances': finances, 'data': data, 'categoria': categoria})

    elif request.method == "POST":

        obs = request.POST.get("inputObs")
        nome = request.POST.get("inputNome")
        data = request.POST.get("inputData")
        valor = round(float(request.POST.get("inputValor")), 2)
        movimento = 'entrada'
        tipo_pgto = request.POST.get("inputTipoPgto")
        categoria = request.POST.get("inputCategoria_in")

        finances = Finance(
            obs=obs,
            nome=nome,
            data=data,
            valor='R$ {:.2f}'.format(valor),
            movimento=movimento,
            tipo_pgto=tipo_pgto,
            hora=time_br,
            categoria=categoria,
        )
        finances.save()

        messages.add_message(request, constants.SUCCESS,
                                'Nova entrada cadastrada com sucesso')
    return redirect('finance_dia')


@login_required
def new_finance_out(request):
    br_tz = pytz.timezone('America/Sao_Paulo')
    time_br = datetime.now(br_tz).time()
    if request.method == "GET":
        data = timezone.localtime(timezone=br_tz).date().strftime('%Y-%m-%d')
        finances = Finance.objects.all()
        categoria = Categoria_out.objects.all()
        return render(request, 'new_finance_out.html', {'finances': finances, 'data': data, 'categoria': categoria})

    elif request.method == "POST":
        obs = request.POST.get("inputObs")
        nome = request.POST.get("inputNome")
        data = request.POST.get("inputData")
        valor = round(float(request.POST.get("inputValor")), 2)
        movimento = 'saída'
        tipo_pgto = request.POST.get("inputTipoPgto")
        categoria = request.POST.get("inputCategoria_out")

        finances = Finance(
            obs=obs,
            nome=nome,
            data=data,
            valor='R$ {:.2f}'.format(valor),
            movimento=movimento,
            hora=time_br,
            tipo_pgto=tipo_pgto,
            categoria=categoria,
        )

        finances.save()

        messages.add_message(request, constants.SUCCESS,
                                'Nova saída cadastrada com sucesso')
    return redirect('finance_dia')


@login_required
def edit_finance(request, id):

    if request.method == 'GET':
        categoria_out = Categoria_out.objects.all()
        categoria_in = Categoria_in.objects.all()
        return render(request, 'edit_finance.html', {
            'id': Finance.objects.get(id=id).id,  # type: ignore
            'obs': Finance.objects.get(id=id).obs,
            'nome': Finance.objects.get(id=id).nome,
            'data': Finance.objects.get(id=id).data.strftime('%Y-%m-%d'),
            'valor': Finance.objects.get(id=id).valor,
            'movimento': Finance.objects.get(id=id).movimento,
            'tipo_pgto': Finance.objects.get(id=id).tipo_pgto,
            'categoria': Finance.objects.get(id=id).categoria,
            'categoria_out': categoria_out,
            'categoria_in': categoria_in,
        })

    elif request.method == "POST":
        finances = Finance.objects.get(id=id)
        finances.obs = request.POST.get("inputObs")
        finances.nome = request.POST.get("inputNome")
        finances.data = request.POST.get("inputData")
        # Processa e formata o valor
        input_valor = request.POST.get("inputValor").replace(',', '.').replace('R$', '').replace(' ', '')
        valor = round(float(input_valor), 2)
        finances.valor = f'R$ {valor:.2f}'  # Formata o valor com "R$ {:.2f}"
        finances.movimento = request.POST.get("in_out")
        finances.tipo_pgto = request.POST.get("inputTipoPgto")
        finances.categoria = request.POST.get("inputCategoria")
        if finances.movimento == 'on':
            finances.movimento = "entrada"
        else:
            finances.movimento = "saída"

        finances.save()
        messages.add_message(request, constants.SUCCESS,
                                'Entrada avulsa atualizada com sucesso')
        return redirect('finance')
    else:
        return HttpResponseBadRequest('Invalid request method')


@user_passes_test(lambda u: u.is_superuser)
def del_finance(request, id):
    finances = Finance.objects.get(id=id)
    finances.delete()
    messages.add_message(request, constants.SUCCESS,
                            'Lançamento no caixa apagado com sucesso')
    return redirect('finance')


@user_passes_test(lambda u: u.is_superuser)
def finance_xlrx(request, id):
    today = datetime.now().date()
    if id == 1:
        finance = Finance.objects.filter(data=today)
        print('dia')
    elif id == 2:
        start_of_week = today - timedelta(days=today.weekday())
        finance = Finance.objects.filter(data__gte=start_of_week)
        print('semana')
    elif id == 3:
        start_of_month = today.replace(day=1)
        finance = Finance.objects.filter(data__gte=start_of_month)
        print('mês')
    elif id == 4:
        year = date.today().year
        finance = Finance.objects.filter(data__year=year)
        print('ano')
    else:
        finance = Finance.objects.all()
        print('todos')

    # Converter os dados para um DataFrame do Pandas
    df = pd.DataFrame(list(finance.values()))

    # Configurar o nome do arquivo de download
    filename = 'workorders.xlsx'

    # Configurar o tipo de resposta HTTP
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    # Gerar o arquivo Excel usando o Pandas e salvar no objeto HttpResponse
    df.to_excel(response, index=False)

    return response


def diario():
    br_tz = pytz.timezone('America/Sao_Paulo')
    today = timezone.localtime(timezone=br_tz).date().strftime('%Y-%m-%d')

    finance = Finance.objects.filter(data=today)
    qtd = finance.count()
    finance_sum = 0
    finance_min = 0
    for finances in Finance.objects.filter(data=today):
        if finances.movimento == 'entrada':
            valor = finances.valor if finances.valor else 0
            try:
                valor = finances.valor if finances.valor else 0
                if valor is not None:
                    # valor = float(valor.replace('R$', '').replace('.', '').replace(',', '.'))
                    valor_str = valor.replace('R$', '').replace('.', '').replace(',', '').replace(' ', '') # type: ignore
                    valor = float(valor_str) / 100
            except ValueError:
                valor = 0
            finance_sum += valor
        elif finances.movimento == 'saída':
            valor = finances.valor if finances.valor else 0
            try:
                valor = finances.valor if finances.valor else 0
                if valor is not None:
                    # valor = float(valor.replace('R$', '').replace('.', '').replace(',', '.'))
                    valor_str = valor.replace('R$', '').replace('.', '').replace(',', '').replace(' ', '') # type: ignore
                    valor = float(valor_str) / 100
            except ValueError:
                valor = 0
            finance_min -= valor

    finance_minus = finance_min * -1
    finance_tot = finance_sum - finance_minus
    finance_total = round(finance_tot, 2)
    return (finance_total, finance_minus, finance_sum, qtd)


def semanal():
    br_tz = pytz.timezone('America/Sao_Paulo')

    today = timezone.localtime(timezone=br_tz).date()
    start_of_week = today - timedelta(days=today.weekday())

    finance = Finance.objects.filter(data__gte=start_of_week)
    qtd = finance.count()
    finance_sum = 0
    finance_min = 0
    for finances in Finance.objects.filter(data__gte=start_of_week):
        if finances.movimento == 'entrada':
            valor = finances.valor if finances.valor else 0
            try:
                valor = finances.valor if finances.valor else 0
                if valor is not None:
                    # valor = float(valor.replace('R$', '').replace('.', '').replace(',', '.'))
                    valor_str = valor.replace('R$', '').replace('.', '').replace(',', '').replace(' ', '') # type: ignore
                    valor = float(valor_str) / 100
            except ValueError:
                valor = 0
            finance_sum += valor
        elif finances.movimento == 'saída':
            valor = finances.valor if finances.valor else 0
            try:
                valor = finances.valor if finances.valor else 0
                if valor is not None:
                    # valor = float(valor.replace('R$', '').replace('.', '').replace(',', '.'))
                    valor_str = valor.replace('R$', '').replace('.', '').replace(',', '').replace(' ', '') # type: ignore
                    valor = float(valor_str) / 100
            except ValueError:
                valor = 0
            finance_min -= valor
    finance_minus = finance_min * -1
    finance_tot = finance_sum - finance_minus
    finance_total = round(finance_tot, 2)

    return (finance_total, finance_minus, finance_sum, qtd)


def mensal():
    br_tz = pytz.timezone('America/Sao_Paulo')

    today = timezone.localtime(timezone=br_tz).date()
    start_of_month = today.replace(day=1)

    finance = Finance.objects.filter(data__gte=start_of_month)
    qtd = finance.count()
    finance_sum = 0
    finance_min = 0
    for finances in Finance.objects.filter(data__gte=start_of_month):
        if finances.movimento == 'entrada':
            try:
                valor = finances.valor if finances.valor else 0
                if valor is not None:
                    # valor = float(valor.replace('R$', '').replace('.', '').replace(',', '.'))
                    valor_str = valor.replace('R$', '').replace('.', '').replace(',', '').replace(' ', '') # type: ignore
                    valor = float(valor_str) / 100
            except ValueError:
                valor = 0
            finance_sum += valor
        elif finances.movimento == 'saída':
            try:
                valor = finances.valor if finances.valor else 0
                if valor is not None:
                    # valor = float(valor.replace('R$', '').replace('.', '').replace(',', '.'))
                    valor_str = valor.replace('R$', '').replace('.', '').replace(',', '').replace(' ', '') # type: ignore
                    valor = float(valor_str) / 100
                
            except ValueError:
                valor = 0
            finance_min -= valor
    finance_minus = finance_min * -1
    finance_tot = finance_sum - finance_minus
    finance_total = round(finance_tot, 2)
    return (finance_total, finance_minus, finance_sum, qtd)


def anual():
    br_tz = pytz.timezone('America/Sao_Paulo')

    year = date.today().year
    finance = Finance.objects.filter(data__year=year)
    qtd = finance.count()
    finance_sum = 0
    finance_min = 0
    for finances in Finance.objects.filter(data__year=year):
        if finances.movimento == 'entrada':
            try:
                valor = finances.valor if finances.valor else 0
                if valor is not None:
                    # valor = float(valor.replace('R$', '').replace('.', '').replace(',', '.'))
                    valor_str = valor.replace('R$', '').replace('.', '').replace(',', '').replace(' ', '') # type: ignore
                    valor = float(valor_str) / 100
            except ValueError:
                valor = 0
            finance_sum += valor
        elif finances.movimento == 'saída':
            try:
                valor = finances.valor if finances.valor else 0
                if valor is not None:
                    # valor = float(valor.replace('R$', '').replace('.', '').replace(',', '.'))
                    valor_str = valor.replace('R$', '').replace('.', '').replace(',', '').replace(' ', '') # type: ignore
                    valor = float(valor_str) / 100
            except ValueError:
                valor = 0
            finance_min -= valor
    finance_minus = finance_min * -1
    finance_tot = finance_sum - finance_minus
    finance_total = round(finance_tot, 2)
    return (finance_total, finance_minus, finance_sum, qtd)


def finance_chart():
    br_tz = pytz.timezone('America/Sao_Paulo')

    now = timezone.localtime(timezone=br_tz)
    start_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    end_month = (start_month + timedelta(days=32)
                    ).replace(day=1) - timedelta(days=1)
    finance_data = Finance.objects.filter(data__range=[start_month, end_month])

    data = {}
    for finance in finance_data:
        day = finance.data.day
        try:
            valor = finance.valor if finance.valor else 0
            if valor is not None:
                # valor = float(valor.replace('R$', '').replace('.', '').replace(',', '.'))
                valor_str = valor.replace('R$', '').replace('.', '').replace(',', '').replace(' ', '') # type: ignore
                valor = float(valor_str) / 100
        except ValueError:
            valor = 0
        if finance.movimento == 'entrada':
            data[day] = data.get(day, {'entradas': 0, 'saidas': 0})
            data[day]['entradas'] += valor
        elif finance.movimento == 'saída':
            data[day] = data.get(day, {'entradas': 0, 'saidas': 0})
            data[day]['saidas'] += valor

    dates = [{'day': day} for day in range(1, end_month.day + 1)]
    entradas = [{'day': day, 'value': data.get(day, {'entradas': 0})[
        'entradas']} for day in range(1, end_month.day + 1)]
    saidas = [{'day': day, 'value': data.get(day, {'saidas': 0})[
        'saidas']} for day in range(1, end_month.day + 1)]

    return (dates, entradas, saidas)


def finance_year_chart():
    br_tz = pytz.timezone('America/Sao_Paulo')
    now = timezone.localtime(timezone=br_tz)
    start_year = now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
    end_year = start_year.replace(month=12, day=31) + timedelta(days=1)
    finance_data = Finance.objects.filter(data__range=[start_year, end_year])

    # print(f"Total de registros (distintos): {finance_data.distinct().count()}")

    data = {}
    seen = set()

    for finance in finance_data:
        unique_entry = (finance.data, finance.valor, finance.categoria, finance.movimento)
        if unique_entry not in seen:
            seen.add(unique_entry)
            month = finance.data.month
            valor_str = finance.valor.replace('R$', '').replace('.', '').replace(',', '').replace(' ', '') # type: ignore
            valor = float(valor_str) / 100 if finance.valor else 0
            if finance.movimento == 'entrada':
                if month not in data:
                    data[month] = {'entradas': 0, 'saidas': 0}
                data[month]['entradas'] += valor
            elif finance.movimento == 'saída':
                if month not in data:
                    data[month] = {'entradas': 0, 'saidas': 0}
                data[month]['saidas'] += valor

            # Adiciona prints para debug
            # print(f"Mês: {month}, Movimento: {finance.movimento}, Valor: {valor}")
            # print(f"Dados atualizados para o mês {month}: {data[month]}")

    months = [{'month': month} for month in range(1, 13)]
    entradas = [data.get(month, {'entradas': 0})['entradas'] for month in range(1, 13)]
    saidas = [data.get(month, {'saidas': 0})['saidas'] for month in range(1, 13)]

    # Adiciona print para verificar as somas finais
    # print(f"Meses: {months}")
    # print(f"Entradas: {entradas}")
    # print(f"Saídas: {saidas}")

    return (months, entradas, saidas)

# def pie_chart_mes_in():
#     br_tz = pytz.timezone('America/Sao_Paulo')

#     today = timezone.localtime(timezone=br_tz).date()
#     month = today.month
#     finances = Finance.objects.filter(
#         data__month=month).filter(movimento='entrada')

#     # Cria um dicionário para armazenar a soma dos gastos de cada categoria
#     expenses_by_category = {}
#     for finance in finances:
#         category = finance.categoria
#         if category in expenses_by_category:
#             expenses_by_category[category] += float(finance.valor.replace(
#                 ',', '.').replace('R$', '').replace(' ', '')) if finance.valor else 0
#         else:
#             expenses_by_category[category] = float(finance.valor.replace(
#                 ',', '.').replace('R$', '').replace(' ', '')) if finance.valor else 0

#     # Cria uma lista com as categorias e outra com os valores correspondentes
#     categories = list(expenses_by_category.keys())
#     values = list(expenses_by_category.values())

#     # Cria um gráfico de pizza
#     plt.figure(figsize=(8, 6))
#     plt.pie(values, labels=categories, autopct='%1.1f%%')
#     plt.title(f'Entadas por categoria - Mês {month}')
#     plt.legend(loc='upper left', bbox_to_anchor=(0.9, 1.0))

#     # Converte o gráfico em uma imagem
#     from io import StringIO
#     import base64
#     buffer = BytesIO()
#     plt.savefig(buffer, format='png')
#     buffer.seek(0)
#     image_png = buffer.getvalue()
#     buffer.close()
#     graphic = base64.b64encode(image_png)
#     graphic = graphic.decode('utf-8')

#     return graphic, categories, values
def pie_chart_dia_pgto():
    br_tz = pytz.timezone('America/Sao_Paulo')
    today = timezone.localtime(timezone=br_tz).date()

    # Filtrando os registros do dia com movimento de entrada
    finances = Finance.objects.filter(data=today, movimento='entrada')

    # Dicionário para armazenar a soma por tipo de pagamento
    payment_methods = {}
    for finance in finances:
        payment_type = finance.tipo_pgto if finance.tipo_pgto else 'Outros'
        valor_str = finance.valor.replace('R$', '').replace('.', '').replace(',', '').replace(' ', '') # type: ignore
        valor = float(valor_str) / 100 if finance.valor else 0
        if payment_type in payment_methods:
            payment_methods[payment_type] += valor
        else:
            payment_methods[payment_type] = valor

    # Convertendo o dicionário em listas para retorno
    categories = list(payment_methods.keys())
    values = list(payment_methods.values())

    # Adicionando valor padrão se não houver dados
    if not categories:
        categories.append('')
        values.append(0)

    return {'categories': categories, 'values': values}


def pie_chart_mes_pgto():
    br_tz = pytz.timezone('America/Sao_Paulo')
    today = timezone.localtime(timezone=br_tz).date()
    month = today.month
    year = today.year

    # Filtrando os registros do mês atual com movimento de entrada
    finances = Finance.objects.filter(data__month=month, data__year=year, movimento='entrada')

    # Dicionário para armazenar a soma por tipo de pagamento
    payment_methods = {}
    for finance in finances:
        payment_type = finance.tipo_pgto if finance.tipo_pgto else 'Outros'
        valor_str = finance.valor.replace('R$', '').replace('.', '').replace(',', '').replace(' ', '') # type: ignore
        valor = float(valor_str) / 100 if finance.valor else 0
        if payment_type in payment_methods:
            payment_methods[payment_type] += valor
        else:
            payment_methods[payment_type] = valor

    # Convertendo o dicionário em listas para retorno
    categories = list(payment_methods.keys())
    values = list(payment_methods.values())

    # Adicionando valor padrão se não houver dados
    if not categories:
        categories.append('')
        values.append(0)

    return {'categories': categories, 'values': values}



def pie_chart_mes_in():
    br_tz = pytz.timezone('America/Sao_Paulo')
    today = timezone.localtime(timezone=br_tz).date()
    month = today.month
    year = today.year

    # Filtrando os registros com base no mês, ano e movimento
    finances = Finance.objects.filter(data__month=month, data__year=year, movimento='entrada')

    print(f"Total de registros (distintos): {finances.distinct().count()}")

    # Cria um dicionário para armazenar a soma dos gastos de cada categoria
    expenses_by_category = {}
    seen = set()
    total_sum = 0

    for finance in finances:
        category = finance.categoria if finance.categoria else 'Outros'
        valor_str = finance.valor.replace('R$', '').replace('.', '').replace(',', '').replace(' ', '') # type: ignore
        valor = float(valor_str) / 100 if finance.valor else 0
        unique_entry = (finance.data, finance.valor, finance.categoria)

        if unique_entry not in seen:
            seen.add(unique_entry)
            if category in expenses_by_category:
                expenses_by_category[category] += valor
            else:
                expenses_by_category[category] = valor
            total_sum += valor

    # Cria uma lista com as categorias e outra com os valores correspondentes
    categories = list(expenses_by_category.keys())
    values = list(expenses_by_category.values())

    # Adiciona print para verificar a soma final
    print(f"Categorias: {categories}")
    print(f"Valores: {values}")
    print(f"Soma total calculada: {total_sum}")
    print(f"Soma total das entradas (dicionário): {sum(values)}")

    # Retorna os dados em formato JSON
    return {'categories': categories, 'values': values}

def pie_chart_ano_in():
    br_tz = pytz.timezone('America/Sao_Paulo')
    today = timezone.localtime(timezone=br_tz).date()
    year = today.year
    finances = Finance.objects.filter(data__year=year, movimento='entrada')

    # print(f"Total de registros (distintos): {finances.distinct().count()}")

    expenses_by_category = {}
    seen = set()

    for finance in finances:
        unique_entry = (finance.data, finance.valor, finance.categoria, finance.movimento)
        if unique_entry not in seen:
            seen.add(unique_entry)
            category = finance.categoria if finance.categoria else 'Outros'
            valor_str = finance.valor.replace('R$', '').replace('.', '').replace(',', '').replace(' ', '') # type: ignore
            valor = float(valor_str) / 100 if finance.valor else 0
            if category in expenses_by_category:
                expenses_by_category[category] += valor
            else:
                expenses_by_category[category] = valor

            # print(f"Categoria: {category}, Valor: {valor}")
            # print(f"Soma atualizada para {category}: {expenses_by_category[category]}")

    categories = list(expenses_by_category.keys())
    values = list(expenses_by_category.values())

    # print(f"Categorias: {categories}")
    # print(f"Valores: {values}")

    return {'categories': categories, 'values': values}

# def pie_chart_ano_in():
#     br_tz = pytz.timezone('America/Sao_Paulo')
#     today = timezone.localtime(timezone=br_tz).date()
#     year = today.year
#     finances = Finance.objects.filter(
#         data__year=year).filter(movimento='entrada')

#     # Cria um dicionário para armazenar a soma dos gastos de cada categoria
#     expenses_by_category = {}
#     for finance in finances:
#         category = finance.categoria
#         if category in expenses_by_category:
#             expenses_by_category[category] += float(finance.valor.replace(
#                 ',', '.').replace('R$', '').replace(' ', '')) if finance.valor else 0
#         else:
#             expenses_by_category[category] = float(finance.valor.replace(
#                 ',', '.').replace('R$', '').replace(' ', '')) if finance.valor else 0

#     # Cria uma lista com as categorias e outra com os valores correspondentes
#     categories = list(expenses_by_category.keys())
#     values = list(expenses_by_category.values())

#     # Cria um gráfico de pizza
#     plt.figure(figsize=(8, 6))
#     plt.pie(values, labels=categories, autopct='%1.1f%%')
#     plt.title(f'Entadas por categoria - Ano {year}')
#     plt.legend(loc='upper left', bbox_to_anchor=(0.9, 1.0))

#     # Converte o gráfico em uma imagem
#     from io import StringIO
#     import base64
#     buffer = BytesIO()
#     plt.savefig(buffer, format='png')
#     buffer.seek(0)
#     image_png = buffer.getvalue()
#     buffer.close()
#     graphic = base64.b64encode(image_png)
#     graphic = graphic.decode('utf-8')

#     return graphic, categories, values


def pie_chart_mes_out():
    br_tz = pytz.timezone('America/Sao_Paulo')
    today = timezone.localtime(timezone=br_tz).date()
    month = today.month
    finances = Finance.objects.filter(data__month=month, movimento='saída')

    # print(f"Total de registros (distintos): {finances.distinct().count()}")

    expenses_by_category = {}
    seen = set()

    for finance in finances:
        unique_entry = (finance.data, finance.valor, finance.categoria, finance.movimento)
        if unique_entry not in seen:
            seen.add(unique_entry)
            category = finance.categoria if finance.categoria else 'Outros'
            # valor = float(finance.valor.replace(',', '.').replace('R$', '').replace(' ', '')) if finance.valor else 0
            try:
                valor = finance.valor if finance.valor else 0
                if valor is not None:
                    # valor = float(valor.replace('R$', '').replace('.', '').replace(',', '.'))
                    valor_str = valor.replace('R$', '').replace('.', '').replace(',', '').replace(' ', '') # type: ignore
                    valor = float(valor_str) / 100
            except ValueError:
                valor = 0
            if category in expenses_by_category:
                expenses_by_category[category] += valor
            else:
                expenses_by_category[category] = valor

            # print(f"Categoria: {category}, Valor: {valor}")
            # print(f"Soma atualizada para {category}: {expenses_by_category[category]}")

    categories = list(expenses_by_category.keys())
    values = list(expenses_by_category.values())

    # print(f"Categorias: {categories}")
    # print(f"Valores: {values}")

    return {'categories': categories, 'values': values}

    # # Cria um gráfico de pizza
    # plt.figure(figsize=(8, 6))
    # plt.pie(values, labels=categories, autopct='%1.1f%%')
    # plt.title(f'Gastos por categoria - Mês {month}')
    # plt.legend(loc='upper left', bbox_to_anchor=(0.9, 1.0))

    # # Converte o gráfico em uma imagem
    # from io import StringIO
    # import base64
    # buffer = BytesIO()
    # plt.savefig(buffer, format='png')
    # buffer.seek(0)
    # image_png = buffer.getvalue()
    # buffer.close()
    # graphic = base64.b64encode(image_png)
    # graphic = graphic.decode('utf-8')

    # return graphic, categories, values


def pie_chart_ano_out():
    br_tz = pytz.timezone('America/Sao_Paulo')
    today = timezone.localtime(timezone=br_tz).date()
    year = today.year
    finances = Finance.objects.filter(data__year=year, movimento='saída')

    # print(f"Total de registros (distintos): {finances.distinct().count()}")

    expenses_by_category = {}
    seen = set()

    for finance in finances:
        unique_entry = (finance.data, finance.valor, finance.categoria, finance.movimento)
        if unique_entry not in seen:
            seen.add(unique_entry)
            category = finance.categoria if finance.categoria else 'Outros'
            try:
                valor = finance.valor if finance.valor else 0
                if valor is not None:
                    # valor = float(valor.replace('R$', '').replace('.', '').replace(',', '.'))
                    valor_str = valor.replace('R$', '').replace('.', '').replace(',', '').replace(' ', '') # type: ignore
                    valor = float(valor_str) / 100
            except ValueError:
                valor = 0
            if category in expenses_by_category:
                expenses_by_category[category] += valor
            else:
                expenses_by_category[category] = valor

            # print(f"Categoria: {category}, Valor: {valor}")
            # print(f"Soma atualizada para {category}: {expenses_by_category[category]}")

    categories = list(expenses_by_category.keys())
    values = list(expenses_by_category.values())

    # print(f"Categorias: {categories}")
    # print(f"Valores: {values}")

    return {'categories': categories, 'values': values}
    # fig, ax = plt.subplots()

    # # Cria um gráfico de pizza
    # plt.figure(figsize=(8, 6))
    # plt.pie(values, labels=categories, autopct='%1.1f%%')
    # plt.title(f'Gastos por categoria - Ano {year}')
    # plt.legend(loc='upper left', bbox_to_anchor=(0.9, 1.0))

    # # Converte o gráfico em uma imagem
    # from io import StringIO
    # import base64
    # buffer = BytesIO()
    # plt.savefig(buffer, format='png')
    # buffer.seek(0)
    # image_png = buffer.getvalue()
    # buffer.close()
    # graphic = base64.b64encode(image_png)
    # graphic = graphic.decode('utf-8')

    # # Informações sobre categorias, valores e porcentagens
    # category_info = list(zip(categories, values))
    # category_percentage = [(category, value / sum(values) * 100)
    #                        for category, value in category_info]

    # return graphic, category_info, category_percentage


def deposit_list(request):
    deposits = Caixa.objects.all()
    return render(request, 'deposits.html', {'deposits': deposits})


def del_deposit(request, id):
    deposit = Caixa.objects.get(id=id)
    deposit.delete()
    messages.add_message(request, constants.SUCCESS,
                            'Deposito apagado com sucesso')
    return redirect('deposit_list')


def tot_in():

    finance_sum = 0
    finance_min = 0
    for finances in Finance.objects.all():
        if finances.movimento == 'entrada' and finances.tipo_pgto == 'Dinheiro':
            valor = finances.valor if finances.valor else 0
            if valor is not None:
                valor = float(valor.replace('R$', '').replace(',', '.')) # type: ignore
                finance_sum += valor
        elif finances.movimento == 'saída' and finances.tipo_pgto == 'Dinheiro':
            valor = finances.valor if finances.valor else 0
            if valor is not None:
                valor = float(valor.replace('R$', '').replace(',', '.'))  # type: ignore
                finance_min -= valor
    finance_minus = finance_min * -1
    finance_tot = finance_sum - finance_minus
    finance_total = round(finance_tot, 2)
    return finance_total