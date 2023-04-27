from django.db import models
from PIL import Image


class Employees(models.Model):
    cod = models.AutoField(primary_key=True)
    func = models.CharField(max_length=15, default="Pessoa Física")
    nome = models.CharField(max_length=50)
    rg = models.CharField(max_length=11, null=True, blank=True)
    cpf = models.CharField(max_length=20, null=True, blank=True)
    data_nasc = models.DateField(null=True, blank=True)
    telefone = models.CharField(max_length=50, null=True, blank=True)
    celular = models.CharField(max_length=14, null=True, blank=True)
    whatsapp = models.CharField(max_length=14, null=True, blank=True)
    email = models.CharField(max_length=30, null=True, blank=True)
    ativo = models.BooleanField(null=True, blank=True)
    data_cadastro = models.DateField(auto_now_add=True, blank=True)
    foto = models.ImageField(upload_to="foto_cliente", null=True, blank=True)
    tipo_end = models.CharField(max_length=15, default="Residencial")
    rua = models.CharField(max_length=50, null=True, blank=True)
    numero = models.CharField(max_length=5, null=True, blank=True)
    compl = models.CharField(max_length=50, null=True, blank=True)
    bairro = models.CharField(max_length=50, null=True, blank=True)
    cidade = models.CharField(max_length=50, null=True, blank=True)
    uf = models.CharField(max_length=20, null=True, blank=True)
    cep = models.CharField(max_length=9, null=True, blank=True)

    def __str__(self):
        return self.nome
