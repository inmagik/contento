from django.conf.urls import url
from .dashboard_views import  (
    DashboardIndexView, DashboardPagesView, DashboardSettingsView,
    DashboardEditPageView,

    #form based views.
    DashboardEditPageBaseView,DashboardEditPageDataView,DashboardEditPageContentView,
    DashboardCreatePage,
    DashboardDropPageView,
)

from .views import serve_single_fragment
#NOT USED RIGHT NOW
#from .api_views import RenderersMetaView


urlpatterns = [
    url(r'^$', DashboardIndexView.as_view(), name="dashboard-index"),
    url(r'pages', DashboardPagesView.as_view(), name="dashboard-pages"),
    url(r'settings', DashboardSettingsView.as_view(), name="dashboard-settings"),


    url(r'edit/(?P<label>[/\w]+)/base/$',     DashboardEditPageBaseView.as_view(), name="dashboard-edit-page-base"),
    url(r'edit/(?P<label>[/\w]+)---(?P<key>\w+)/base/$',  DashboardEditPageBaseView.as_view(), name="dashboard-edit-page-base"),

    url(r'edit/(?P<label>[/\w]+)/data/$',     DashboardEditPageDataView.as_view(), name="dashboard-edit-page-data"),
    url(r'edit/(?P<label>[/\w]+)---(?P<key>\w+)/data/$',  DashboardEditPageDataView.as_view(), name="dashboard-edit-page-data"),

    url(r'edit/(?P<label>[/\w]+)/content/$',     DashboardEditPageContentView.as_view(), name="dashboard-edit-page-content"),
    url(r'edit/(?P<label>[/\w]+)---(?P<key>\w+)/content/$',  DashboardEditPageContentView.as_view(), name="dashboard-edit-page-content"),

    url(r'delete/(?P<label>[/\w]+)/$',     DashboardDropPageView.as_view(), name="dashboard-drop-page"),
    url(r'delete/(?P<label>[/\w]+)---(?P<key>\w+)/$',  DashboardDropPageView.as_view(), name="dashboard-drop-page"),

    url(r'edit/(?P<label>[/\w]+)/$', DashboardEditPageView.as_view(), name="dashboard-edit-page"),
    url(r'edit/(?P<label>[/\w]+)---(?P<key>\w+)/$', DashboardEditPageView.as_view(), name="dashboard-edit-page"),

    url(r'add-page/(?P<parent>[-_/\w]+)/$', DashboardCreatePage.as_view(), name="dashboard-add-page-with-parent"),
    url(r'add-page/$', DashboardCreatePage.as_view(), name="dashboard-add-page"),


    url(r'preview/(?P<label>.*)', serve_single_fragment, name="contento-cms-preview"),

    #url(r'api/renderers-meta/$', RenderersMetaView.as_view(), name="contento-renderers-meta"),

]
