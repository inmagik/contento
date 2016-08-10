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

def serve_page(
    request,
    page_url="/",
    fragment_path=None,
    single_fragment_template="contento/dashboard/single_fragment.html"
    ):
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

    context = {}
    context.update({"url_data" : url_params })

    if request.GET.get("fragment_path"):
        region, order = request.GET.get("fragment_path").split(".")
        fragment = page["content"][region][int(order)]
        context.update({
            "content_type" : fragment.get("type"),
            "content_data" : fragment.get("data"),
            "page" : page.get("page")
        })
        return render(
            request,
            single_fragment_template,
            context
        )

    context.update(page["content"])
    return render(
        request,
        page_meta["data"]["template"],
        context
    )
