from django.db import models

class Finance(models.Model):
    obs = models.CharField(max_length=6, blank=True, null=True)
    nome = models.CharField(max_length=50, null=True, blank=True)
    data = models.DateField(blank=True)
    valor = models.CharField(max_length=10, null=True, blank=True)
    movimento = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return self.nome
