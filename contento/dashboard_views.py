"""
Dashboard views
"""
import json
from django.views.generic import TemplateView, View, FormView, DeleteView
from django.views.generic.edit import DeletionMixin
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.module_loading import import_string
from django.shortcuts import render
from django.template import loader
from django.db import transaction
from deepdiff import DeepDiff
from contento.settings import CONTENTO_BACKEND
from contento.meta import get_regions_from_template, get_contento_renderers_schemas
from contento.backends.helpers import get_meta_from_path
from .forms import PageEditBaseForm, PageEditDataForm, PageEditContentForm, PagesSortableForm


def simplify_node(node):
    new_node = { x : node[x] for x in ["label", "language", "key", "order"]}
    new_node["children"] = simplify_tree(node["children"])
    return new_node

def simplify_tree(tree):
    return map(simplify_node, tree)


class DashboardIndexView(TemplateView):
    template_name = "contento/dashboard/dashboard_index.html"

class DashboardPagesView(FormView):
    template_name = "contento/dashboard/dashboard_pages.html"
    form_class = PagesSortableForm


    def dispatch(self, *args, **kwargs):
        self.cms_backend = import_string(CONTENTO_BACKEND)()
        self.tree = self.cms_backend.get_tree(None)
        self.serialized_tree =  self.serialize_tree(self.tree)
        return super(DashboardPagesView, self).dispatch(*args, **kwargs)

    def get_context_data(self):
        context_data = super(DashboardPagesView, self).get_context_data()
        #TODO: lang here....
        context_data["pages_tree"] = self.tree
        return context_data

    def serialize_tree(self, tree):
        out = []
        for node in self.tree:
            out.append(node.serialize())
        return out

    def get_initial(self):
        kwargs = super(DashboardPagesView, self).get_initial()
        kwargs['data'] = self.serialized_tree
        return kwargs

    @transaction.atomic
    def perform_ordering(self, data):
        for i, item in enumerate(data):
            if item.get("order", 0) != i:
                self.cms_backend.reorder_page(
                item["label"], new_order=i, language=item["language"], key=item["key"]
            )
            self.perform_ordering(item.get("children",[]))

    def form_valid(self, form):
        #DO the diff and act accordingly
        sorted_data = form.cleaned_data["data"]

        self.perform_ordering(sorted_data)
        return super(DashboardPagesView, self).form_valid(form)


    def get_success_url(self):
        return self.request.path

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
            page_meta = page.data
            tpl_name = page.template
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
        kwargs['template'] = self.page.template
        kwargs['url'] = self.page.url or "/"
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
        kwargs['data'] = self.page.data
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
        kwargs['content'] = self.page.content
        return kwargs

    def get_form_kwargs(self):
        kwargs = super(DashboardEditPageContentView, self).get_form_kwargs()
        region_names = get_regions_from_template(self.page.template, load=True)
        kwargs['region_names'] = region_names
        fragments_schemas = get_contento_renderers_schemas()
        kwargs['fragments_schemas'] = fragments_schemas
        return kwargs

    def form_valid(self, form):

        if 'content' in form.changed_data:
            self.cms_backend.modify_page(
                self.label,
                template=None,
                url=None,
                page_data=None, page_content=form.cleaned_data["content"], language=None, key=None)

        return super(DashboardEditPageContentView, self).form_valid(form)


class DashboardCreatePage(FormView):
    template_name = "contento/dashboard/dashboard_page_add.html"
    form_class = PageEditBaseForm

    def __init__(self, *args, **kwargs):
        self.cms_backend = import_string(CONTENTO_BACKEND)()
        self.parent = None
        super(DashboardCreatePage, self).__init__(*args, **kwargs)

    def dispatch(self, *args, **kwargs):
        if self.kwargs.get('parent'):
            self.parent_meta = get_meta_from_path( self.kwargs.get('parent'))
            self.parent = self.cms_backend.get_page(*self.parent_meta)
            self.parent_label = self.parent["label"]

        return super(DashboardCreatePage, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super(DashboardCreatePage, self).get_context_data(**kwargs)
        if self.kwargs.get('parent'):
            ctx['parent'] = self.parent
        return ctx

    def get_initial(self):
        kwargs = super(DashboardCreatePage, self).get_initial()
        if self.parent:
            kwargs['parent'] = self.parent_label
        return kwargs

    def get_success_url(self):
        return reverse("dashboard-pages")

    def form_valid(self, form):
        url = form.cleaned_data["url"] or form.cleaned_data["label"]
        self.cms_backend.add_page(
            form.cleaned_data["label"],
            template=form.cleaned_data["template"],
            url=url,
            parent_label=form.cleaned_data["parent"],
            page_data={}, page_content={}, language=None, key=None)

        return super(DashboardCreatePage, self).form_valid(form)


class DashboardDropPageView(DeletionMixin, TemplateView):
    template_name = "contento/dashboard/dashboard_page_drop.html"

    def dispatch(self, *args, **kwargs):
        label = self.kwargs.get('label')
        language = self.kwargs.get('language', None)
        key = self.kwargs.get('key', None)
        self.cms_backend = import_string(CONTENTO_BACKEND)()
        self.page = self.cms_backend.get_page(label, language=language, key=key)
        return super(DashboardDropPageView, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        return reverse("dashboard-pages")

    def delete(self, request, *args, **kwargs):
        success_url = self.get_success_url()
        self.cms_backend.drop_page(self.page.label, self.page.language,
            self.page.key)
        return HttpResponseRedirect(success_url)
