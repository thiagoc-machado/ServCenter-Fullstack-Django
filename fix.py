import os
import django
from datetime import datetime

# Configure o ambiente do Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'servcenter.settings')
django.setup()

from work_order.models import work_order  # Agora a importação funcionará

def update_data_saida():
    # Filtra todas as ordens finalizadas que não possuem data de saída
    work_orders = work_order.objects.filter(os_finalizada=True)

    for order in work_orders:
        if order.data_alteracao:
            try:
                # Converte a string no formato 'yyyy-mm-dd' para um objeto datetime
                data_obj = datetime.strptime(order.data_alteracao, "%Y-%m-%d")
                # Formata a data no formato 'dd/mm/yyyy'
                order.data_saida = data_obj.strftime("%d/%m/%Y")
            except ValueError:
                print(f"Erro ao converter data_alteracao para o registro ID {order.id}: {order.data_alteracao}")
                continue
        else:
            # Define uma data padrão se data_alteracao não existir
            order.data_saida = "01/01/1970"  # Ou outra data padrão desejada

        order.save()  # Salva no banco de dados

    print(f"Atualização concluída.")
# Execute a função
if __name__ == "__main__":
    update_data_saida()
