from __future__ import unicode_literals

from django.db import models


class CeasarCipher(models.Model):
    text = models.TextField()
    rot = models.IntegerField()
