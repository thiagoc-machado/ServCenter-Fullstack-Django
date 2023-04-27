from django.db import models
from PIL import Image
from clients.models import client
from employees.models import Employees
from services.models import Services
from django.contrib.auth.models import User


class work_order(models.Model):

    cod_cli = models.ForeignKey(client, on_delete=models.DO_NOTHING)
    cod_tec = models.ForeignKey(Employees, on_delete=models.DO_NOTHING)
    cod_ser = models.ForeignKey(Services, on_delete=models.DO_NOTHING)
    cod_user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    whatsapp = models.CharField(max_length=20, null=True, blank=True)
    obs_cli = models.CharField(max_length=50, null=True, blank=True)
    data_entrada = models.DateField(auto_now_add=True, blank=True)
    status = models.CharField(max_length=20, null=True, blank=True)
    produto = models.CharField(max_length=20, null=True, blank=True)
    marca = models.CharField(max_length=20, null=True, blank=True)
    modelo = models.CharField(max_length=20, null=True, blank=True)
    serie = models.CharField(max_length=20, null=True, blank=True)
    condicao = models.CharField(max_length=50, null=True, blank=True)
    acessorios = models.CharField(max_length=50, null=True, blank=True)
    defeito = models.CharField(max_length=50, null=True, blank=True)
    solucao = models.CharField(max_length=50, null=True, blank=True)
    preco = models.CharField(max_length=50, null=True, blank=True)
    desconto = models.CharField(max_length=50, null=True, blank=True)
    acressimo = models.CharField(max_length=50, null=True, blank=True)
    data_saida = models.CharField(max_length=50, null=True, blank=True)
    data_alteracao = models.CharField(max_length=50, null=True, blank=True)
    obs_ser = models.CharField(max_length=50, null=True, blank=True)
    total = models.CharField(max_length=50, null=True, blank=True)
    modo_pgto = models.CharField(max_length=50, null=True, blank=True)
    pgto_adiantado = models.BooleanField()
    os_finalizada = models.BooleanField()

    def __str__(self):
        return self.produto


class image(models.Model):
    photo = models.ImageField(upload_to="work_order/")
    order = models.ForeignKey(work_order, on_delete=models.CASCADE)
