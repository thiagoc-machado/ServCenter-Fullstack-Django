# Generated by Django 4.1.5 on 2023-01-19 23:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('employees', '0002_remove_employees_id_employees_cod'),
        ('clients', '0016_alter_client_vendedor'),
        ('services', '0002_alter_services_descr_alter_services_obs_and_more'),
        ('work_order', '0003_services_modo_pgto_services_obs_ser_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Services',
            new_name='work_order',
        ),
        migrations.AlterField(
            model_name='image',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='services.services'),
        ),
    ]
