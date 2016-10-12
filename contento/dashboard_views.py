"""
Dashboard views
"""
import json
from django.views.generic import TemplateView, View
from django.http import HttpResponse
from django.utils.module_loading import import_string
from django.shortcuts import render
from django.template import loader
from contento.settings import CONTENTO_BACKEND
from contento.render_helpers import get_regions_from_template

class DashboardIndexView(TemplateView):
    template_name = "contento/dashboard/dashboard_index.html"

class DashboardPagesView(TemplateView):
    template_name = "contento/dashboard/dashboard_pages.html"

    def get_context_data(self):
        context_data = super(DashboardPagesView, self).get_context_data()
        cms_backend = import_string(CONTENTO_BACKEND)()
        #TODO: lang here....
        tree = cms_backend.get_tree("/")
        context_data["pages_tree"] = tree
        return context_data

class DashboardSettingsView(TemplateView):
    template_name = "contento/dashboard/dashboard_settings.html"


class DashboardEditPageView(View):
    template_name = "contento/dashboard/dashboard_page_edit.html"

    def __init__(self, *args, **kwargs):
        super(DashboardEditPageView, self).__init__(*args, **kwargs)
        self.cms_backend = import_string(CONTENTO_BACKEND)()

    def get(self, request, label, language=None, key=None):
        page = self.cms_backend.get_page(label, language=language, key=key)

        try:
            page_meta = page.get("data")
            tpl_name = page.get("template")
            tpl = loader.get_template(tpl_name)
            region_names = get_regions_from_template(tpl.template.source)
        except:
            region_names = []


        page_context = {
            "page" : page,
            "label" : label,
            "language" : language,
            "key" : key,
            "region_names" : region_names,
        }

        context = { "page_context" : json.dumps(page_context) }

        return render(
            request,
            self.template_name,
            context=context,
            content_type=None, status=None, using=None
        )
