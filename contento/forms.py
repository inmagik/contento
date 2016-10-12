from django import forms
from django.db import connection

if connection.vendor == 'postgresql':
    from django.contrib.postgres.forms import JSONField as FormJSONField
else:
    from .fields import JSONField as FormJSONField

from .settings import CONTENTO_TEMPLATES


class PageEditBaseForm(forms.Form):
    """
    """
    label = forms.CharField()
    template = forms.ChoiceField(choices=CONTENTO_TEMPLATES)
    url = forms.CharField(required=False)



class PageEditDataForm(forms.Form):
    """
    """
    data = FormJSONField(widget=forms.Textarea)


class PageEditContentForm(forms.Form):
    """
    """
    content = FormJSONField()
