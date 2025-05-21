from django.db import models


class Finance(models.Model):
    obs = models.CharField(max_length=6, blank=True, null=True)
    nome = models.CharField(max_length=50, null=True, blank=True)
    data = models.DateField(blank=True)
    valor = models.CharField(max_length=10, null=True, blank=True)
    movimento = models.CharField(max_length=10, null=True, blank=True)
    hora = models.TimeField(blank=True)
    tipo_pgto = models.CharField(max_length=10, null=True, blank=True)
    categoria = models.CharField(max_length=10, null=True, blank=True)


    def __str__(self):
        return self.nome


class Categoria_in(models.Model):
    categoria = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return self.categoria


class Categoria_out(models.Model):
    categoria = models.CharField(max_length=10, null=True, blank=True)

class Caixa(models.Model):
    deposits = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    date = models.DateField(blank=True)
    obs = models.CharField(max_length=10, blank=True, null=True)
    saldo = models.CharField(max_length=10, null=True, blank=True)
    def __str__(self):
        return self.deposits
