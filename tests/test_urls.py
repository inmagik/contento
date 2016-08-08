"""
Test urls configuration
"""
from django.conf.urls import url
from contento.routers import CMSRouter

urlpatterns = []

cms_router = CMSRouter()
cms_urls = cms_router.mount(r'cms/')
urlpatterns += cms_urls
