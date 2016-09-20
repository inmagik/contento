from __future__ import unicode_literals
from django.db import models, connection

if connection.vendor == 'postgresql':
    from django.contrib.postgres.fields import JSONField
else:
    from jsonfield import JSONField

class Page(models.Model):

    label = models.CharField(max_length=200)
    language = models.CharField(max_length=200, null=True, blank=True)
    key = models.CharField(max_length=200, null=True, blank=True)
    template = models.CharField(max_length=200)
    url = models.CharField(max_length=200, default="")
    data = JSONField(default={})
    #relationships modelling:parent is a weak reference
    parent = models.CharField(max_length=200, null=True)
    order = models.PositiveIntegerField(default=0)
    content = JSONField(default={})

    class Meta:
        unique_together=["label", "language", "key"]
