from django.db import models
from PIL import Image


class Services(models.Model):
    cod = models.AutoField(primary_key=True)
    tipo = models.CharField(max_length=20, default="Pessoa Física")
    nome = models.CharField(max_length=50)
    descr = models.CharField(max_length=50, null=True, blank=True)
    valor = models.CharField(max_length=20, null=True, blank=True)
    obs = models.CharField(max_length=50, null=True, blank=True)
    data_cadastro = models.DateField(auto_now_add=True, blank=True)
    foto = models.ImageField(upload_to="foto_cliente", null=True, blank=True)

    def __str__(self):
        return self.nome


