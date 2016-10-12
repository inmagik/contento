"""
Dashboard views
"""
import json
from django.views.generic import TemplateView, View, FormView
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

from .forms import PageEditBaseForm, PageEditDataForm, PageEditContentForm


class DashboardEditPageBase(FormView):


    def __init__(self, *args, **kwargs):
        self.cms_backend = import_string(CONTENTO_BACKEND)()
        super(DashboardEditPageBase, self).__init__(*args, **kwargs)


    def get(self, request, label, language=None, key=None):
        self.page = self.cms_backend.get_page(label, language=language, key=key)
        self.label = label
        return super(DashboardEditPageBase, self).get(request)

    def post(self, request, label, language=None, key=None):
        self.page = self.cms_backend.get_page(label, language=language, key=key)
        self.label = label
        return super(DashboardEditPageBase, self).post(request)

    def get_success_url(self):
        return self.request.path

    def get_context_data(self, **kwargs):
        ctx = super(DashboardEditPageBase, self).get_context_data(**kwargs)
        ctx['label'] = self.label
        ctx['key'] = self.kwargs.get("key")
        return ctx



class DashboardEditPageBaseView(DashboardEditPageBase):
    template_name = "contento/dashboard/dashboard_page_edit_base.html"
    form_class = PageEditBaseForm

    def get_initial(self):
        kwargs = super(DashboardEditPageBaseView, self).get_initial()
        kwargs['label'] = self.label
        kwargs['template'] = self.page.get("template")
        kwargs['url'] = self.page.get("url", "/")
        return kwargs

    def form_valid(self, form):
        url = None
        if 'url' in form.changed_data:
            url=form.cleaned_data['url']

        template = None
        if 'template' in form.changed_data:
            template=form.cleaned_data['template']

        self.cms_backend.modify_page(
            self.label,
            template=template,
            url=url,
            page_data=None, page_content=None, language=None, key=None)

        return super(DashboardEditPageBaseView, self).form_valid(form)


class DashboardEditPageDataView(DashboardEditPageBase):
    template_name = "contento/dashboard/dashboard_page_edit_data.html"
    form_class = PageEditDataForm

    def get_initial(self):
        kwargs = super(DashboardEditPageDataView, self).get_initial()
        kwargs['data'] = self.page.get("data")
        return kwargs

    def form_valid(self, form):

        if 'data' in form.changed_data:
            self.cms_backend.modify_page(
                self.label,
                template=None,
                url=None,
                page_data=form.cleaned_data["data"], page_content=None, language=None, key=None)

        return super(DashboardEditPageDataView, self).form_valid(form)


class DashboardEditPageContentView(DashboardEditPageBase):
    template_name = "contento/dashboard/dashboard_page_edit_content.html"
    form_class = PageEditContentForm

    def get_initial(self):
        kwargs = super(DashboardEditPageContentView, self).get_initial()
        kwargs['content'] = self.page.get("content")
        return kwargs

    def form_valid(self, form):

        if 'content' in form.changed_data:
            self.cms_backend.modify_page(
                self.label,
                template=None,
                url=None,
                page_data=None, page_content=form.cleaned_data["content"], language=None, key=None)

        return super(DashboardEditPageContentView, self).form_valid(form)
