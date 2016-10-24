from __future__ import unicode_literals
from django.db import models, connection

from .fields import NullCharField

if connection.vendor == 'postgresql':
    from django.contrib.postgres.fields import JSONField
else:
    from jsonfield import JSONField

class Page(models.Model):

    label = models.CharField(max_length=200)
    language = NullCharField(max_length=200)
    key = NullCharField(max_length=200)

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
            paths.insert(0, self.parent.url)

        out = "/".join(paths)
        if not out.startswith("/"):
            out = "/" + out
        self.fullpath = out

        return super(Page, self).save(*args, **kwargs)

    def __unicode__(self):
        return u'%s' % self.label


    class Meta:
        unique_together=["label", "language", "key"]
