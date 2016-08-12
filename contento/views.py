"""
Contento public views.
"""
import re
import json
from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.utils import translation
from contento.registry import Registry
from contento.helpers import get_current_backend
from django.views.decorators.csrf import csrf_exempt


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
    cms_backend = get_current_backend()

    page = cms_backend.get_page(
        page_meta["label"],
        language=page_meta["language"],
        key=page_meta["key"])

    context = {}
    context.update({"url_data" : url_params })
    context.update(page["content"])
    return render(
        request,
        page_meta["data"]["template"],
        context
    )


#TODO:ALLOW POSTING ALSO CONTENT TYPE (FOR NEW FRAGMENTS PREVIEW)
@csrf_exempt
def serve_single_fragment(
    request,
    label,
    language=None,
    key=None,
    fragment_path=None,
    single_fragment_template="contento/dashboard/single_fragment.html"
    ):
    """

    """
    cms_backend = get_current_backend()
    page = cms_backend.get_page(
        label,
        language=language,
        key=key)

    context = {}
    url_params = request.GET.get("url_params", {})
    context.update({"url_data" : url_params })
    region, order = request.GET.get("fragment_path").split(".")
    fragment = page["content"][region][int(order)]

    current_data = fragment.get("data")
    override_data = None
    if request.method == "POST" and request.POST.get("content_data"):
        print "POSTED!"
        override_data = json.loads(request.POST.get("content_data"))


    context.update({
        "content_type" : fragment.get("type"),
        "content_data" : override_data or current_data,
        "page" : page.get("page")
    })

    return render(
        request,
        single_fragment_template,
        context
    )
