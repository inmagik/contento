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
    url = models.CharField(blank=True, max_length=200, default="")

    data = JSONField(blank=True, default={})
    content = JSONField(blank=True, default={})

    #relationships modelling:parent is a weak reference
    parent = models.ForeignKey("self", blank=True, null=True, related_name="children")
    order = models.PositiveIntegerField(blank=True, default=0)

    ##persisting full path
    fullpath = models.CharField(blank=True, max_length=200, default="")

    def save(self, *args, **kwargs):
        paths = [self.url]
        if self.parent:
            paths.insert(self.parent.url)

        out = "/".join(paths)
        if not out.startswith("/"):
            out = "/" + out
        return out


    class Meta:
        unique_together=["label", "language", "key"]
