from __future__ import unicode_literals

from django.db import models

# Create your models here.
class CeasarCipher(models.Model):
    text = models.TextField()
    shift = models.IntegerField()