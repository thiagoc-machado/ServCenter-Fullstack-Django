from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class Documents(models.Model):
    nome = models.CharField(max_length=100, blank=True, null=True)
    texto = models.TextField(blank=True, null=True)
    arquivo = models.FileField(upload_to='documents/', blank=True, null=True)
    data = models.DateField(blank=True, null=True)
    obs = models.TextField(blank=True, null=True)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    def is_image(self):
        return self.arquivo.url.endswith('.png') or self.arquivo.url.endswith('.jpg')
