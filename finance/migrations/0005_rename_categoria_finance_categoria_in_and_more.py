# Generated by Django 4.1.5 on 2023-04-10 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0004_finance_categoria'),
    ]

    operations = [
        migrations.RenameField(
            model_name='finance',
            old_name='categoria',
            new_name='categoria_in',
        ),
        migrations.AddField(
            model_name='finance',
            name='categoria_out',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
