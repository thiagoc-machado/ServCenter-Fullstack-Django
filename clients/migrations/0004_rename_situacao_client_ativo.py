# Generated by Django 4.1.5 on 2023-01-14 21:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0003_alter_client_celular_alter_client_cpf_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='client',
            old_name='situacao',
            new_name='ativo',
        ),
    ]
