# Generated by Django 4.1.5 on 2023-01-24 00:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('work_order', '0006_work_order_whatsapp'),
    ]

    operations = [
        migrations.RenameField(
            model_name='work_order',
            old_name='data_saída',
            new_name='data_saida',
        ),
    ]
