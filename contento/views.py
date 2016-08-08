"""
Contento public views.
"""

from django.http import HttpResponse
from django.shortcuts import render
from django.utils.module_loading import import_string
from django.utils import translation
from contento.settings import CONTENTO_BACKEND
from contento.registry import Registry

def serve_page(request, page_url="/"):
    """
    Main view for serving cms pages.
    """
    page_url = page_url or "/"
    if not page_url.startswith("/"):
        page_url = "/" + page_url

    #TODO: we should load the global cached registry
    #we create a new one instead
    registry = Registry()

    page_meta = registry.content_by_url.get(page_url)
    cur_language = translation.get_language()
    cms_backend = import_string(CONTENTO_BACKEND)()

    page = cms_backend.get_page(
        page_meta["label"],
        language=page_meta["language"],
        key=page_meta["key"])

    return render(
        request,
        page_meta["data"]["template"],
        page["content"]
    )
