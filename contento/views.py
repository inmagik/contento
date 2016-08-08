"""
Contento public views.
"""

from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.utils.module_loading import import_string
from django.utils import translation
from contento.settings import CONTENTO_BACKEND
from contento.registry import Registry
import re

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

    #
    available_urls = registry.content_by_url.keys()

    page_meta = None
    for k in available_urls:
        r = re.compile(k+"/?$")
        m = r.match(page_url)
        if m:
            url_params = m.groupdict()
            page_meta = registry.content_by_url.get(k)

    if not page_meta:
        raise Http404

    cur_language = translation.get_language()
    cms_backend = import_string(CONTENTO_BACKEND)()

    page = cms_backend.get_page(
        page_meta["label"],
        language=page_meta["language"],
        key=page_meta["key"])

    context = page["content"]
    context.update({"url_data" : url_params })

    return render(
        request,
        page_meta["data"]["template"],
        context
    )
