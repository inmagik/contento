"""
Contento public views.
"""

from django.http import HttpResponse
from django.shortcuts import render
from django.utils.module_loading import import_string
from django.utils import translation
from contento.settings import CONTENTO_BACKEND

def serve_page(request, slug=None):
    """
    Main view for serving cms pages.
    """

    if not slug:
        slug = "/"

    print "Rendering", slug
    cur_language = translation.get_language()
    print "Rendering", slug, cur_language


    cms_backend = import_string(CONTENTO_BACKEND)()
    page = cms_backend.get_page(slug)
    page_data =  page.get("page")
    content =  page.get("content")


    return render(request, page_data["template"], content)
