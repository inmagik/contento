import json
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
    parent = forms.CharField(required=False)


DATA_SCHEMA = {
    "title": "Data",
    "type" : "object",
    "properties": {
        "published": {
            "type": "boolean",
            "propertyOrder": 1
        },
        "menu_title": {
            "type": "string",
            "propertyOrder": 2
        },

    },
    "required": ["published"]
}
class PageEditDataForm(forms.Form):
    """
    """
    data = FormJSONField(widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super(PageEditDataForm, self).__init__(*args, **kwargs)
        self.fields['data'].widget.attrs["data-jshook"] = "textarea-jsonschema"
        self.fields['data'].widget.attrs["data-textarea-jsonschema"] = json.dumps(DATA_SCHEMA)



class PageEditContentForm(forms.Form):
    """
    """

    def __init__(self, *args, **kwargs):
        self.region_names = kwargs.pop("region_names")
        self.fragments_schemas = kwargs.pop("fragments_schemas")

        super(PageEditContentForm, self).__init__(*args, **kwargs)

        self.fields['content'].widget.attrs["data-jshook"] = "content-editor"
        self.fields['content'].widget.attrs["data-contenteditor-regions"] = json.dumps(self.region_names)
        self.fields['content'].widget.attrs["data-contenteditor-fragments-schemas"] = json.dumps(self.fragments_schemas)


    content = FormJSONField(widget=forms.Textarea)
