import os
import django
import random

# Configure o ambiente do Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'servcenter.settings')
django.setup()

from finance.models import Finance  # Ajuste o caminho para o app 'finance'

def randomize_entry_categories():
    # Categorias novas para entrada
    new_categories = ["Consumidor", "Mecanico", "Empresas"]

    # Filtra apenas os registros com movimento de entrada
    entry_finances = Finance.objects.filter(movimento='entrada')

    for finance in entry_finances:
        # Escolhe uma categoria nova aleatoriamente
        new_category = random.choice(new_categories)
        old_category = finance.categoria or "Vazio"
        finance.categoria = new_category
        finance.save()  # Atualiza no banco de dados
        print(f"Registro ID {finance.id}: Categoria '{old_category}' atualizada para '{new_category}'")

    print("Atualização concluída para categorias de entrada.")

# Execute o script
if __name__ == "__main__":
    randomize_entry_categories()
