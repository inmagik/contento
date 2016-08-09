"""
Admin views
"""
from django.views.generic import TemplateView
from django.utils.module_loading import import_string
from contento.settings import CONTENTO_BACKEND

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
