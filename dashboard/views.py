from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from datetime import date
from datetime import datetime
from finance.models import Finance
from pytz import timezone as tz
import pytz

from django.utils import timezone

def get_today_values():
    sao_paulo_tz = tz('America/Sao_Paulo')
    today = timezone.localtime(timezone= sao_paulo_tz).date()
    start = timezone.make_aware(datetime.combine(today, datetime.min.time()), timezone=sao_paulo_tz)
    end = timezone.make_aware(datetime.combine(today, datetime.max.time()), timezone=sao_paulo_tz)
    return Finance.objects.filter(data__range=(start, end))

def get_values_by_hour():
    values = [0] * 11  # 11 horas de trabalho, das 8h às 18h
    today_values = get_today_values()
    for value in today_values:
        if value.movimento == 'entrada':
            value_datetime = datetime.combine(value.data, value.hora)
            value_datetime = tz('America/Sao_Paulo').localize(value_datetime)
            hour = value_datetime.hour - 8  # ajuste de índice da lista
            if 0 <= hour <= 10:
                if not value.valor:
                    valor = 0
                else:
                    valor = value.valor.replace('R$', '').replace('.', '').replace(',', '').strip()
                value_str = f'{valor[:-2]}.{valor[-2:]}' # type: ignore
                value_float = float(value_str)
                values[hour] += value_float # type: ignore
    return values

def get_output_by_hour():
    values = [0] * 11  # 11 horas de trabalho, das 8h às 18h
    today_values = get_today_values()
    for value in today_values:
        if value.movimento == 'saída':
            value_datetime = datetime.combine(value.data, value.hora)
            value_datetime = tz('America/Sao_Paulo').localize(value_datetime)
            hour = value_datetime.hour - 8  # ajuste de índice da lista
            if 0 <= hour <= 10:
                if not value.valor:
                    valor = 0
                else:
                    valor = value.valor.replace('R$', '').replace('.', '').replace(',', '').strip()
                valor = f'{valor[:-2]}.{valor[-2:]}' # type: ignore
                value_float = float(valor)
                values[hour] += value_float# type: ignore
    return values

@login_required
def dashboard(request):
    if request.method == "GET":
        br_tz = pytz.timezone('America/Sao_Paulo')
        today = timezone.localtime(timezone= br_tz).date()
        all_finance = Finance.objects.all()
        finance = Finance.objects.filter(data=today)
        qtd = finance.filter(movimento='entrada').count()
        values_by_hour = get_values_by_hour()
        output_by_hour = get_output_by_hour()

        finance_sum = 0
        finance_min = 0
        for finances in Finance.objects.filter(data=today):
            if finances.movimento == 'entrada':
                valor = finances.valor
                if valor is not None:
                    valor = valor.replace('R$', '').replace('.', '').replace(',', '').strip()
                    valor = f'{valor[:-2]}.{valor[-2:]}'
                    valor_float = float(valor)
                    finance_sum += valor_float
            elif finances.movimento == 'saída':
                valor = finances.valor
                if valor is not None:
                    valor = valor.replace('R$', '').replace('.', '').replace(',', '').strip()
                    valor = f'{valor[:-2]}.{valor[-2:]}'
                    valor = float(valor)
                    finance_min -= valor

        finance_minus = finance_min * -1
        finance_total = finance_sum - finance_minus
        print('{:.2f}'.format(finance_sum))
        print(round(float(finance_minus), 2))
        return render(request, 'dashboard.html', {'finance': finance,
                                                'all_finance': all_finance,
                                                'finance_sum': '{:.2f}'.format(finance_sum),
                                                'finance_minus': '{:.2f}'.format(finance_minus),
                                                'finance_total': '{:.2f}'.format(finance_total),
                                                'qtd': qtd,
                                                'values_by_hour': values_by_hour,
                                                'output_by_hour': output_by_hour
                                                })

    else:
        return HttpResponseBadRequest('Invalid request method')
