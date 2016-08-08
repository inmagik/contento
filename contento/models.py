from __future__ import unicode_literals
from django.db import models


class Page(models.Model):

    label = models.CharField(max_length=200)
    language = models.CharField(max_length=200, null=True, blank=True)
    key = models.CharField(max_length=200, null=True, blank=True)
    template_name = models.CharField(max_length=200)

    slug = models.CharField(max_length=200, default="")

    #relationships modelling
    #parent is a weak reference
    parent = models.CharField(max_length=200, null=True)


    class Meta:
        unique_together=["label", "language", "key"]
