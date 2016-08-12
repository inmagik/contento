from django.conf.urls import url
from .dashboard_views import  (
    DashboardIndexView, DashboardPagesView, DashboardSettingsView,
    DashboardEditPageView
)

from .views import serve_single_fragment
from .api_views import RenderersMetaView

#from rest_framework.routers import SimpleRouter
#router = SimpleRouter()


urlpatterns = [
    url(r'^$', DashboardIndexView.as_view(), name="dashboard-index"),
    url(r'pages', DashboardPagesView.as_view(), name="dashboard-pages"),
    url(r'settings', DashboardSettingsView.as_view(), name="dashboard-settings"),
    url(r'edit/(?P<label>[/\w]+)/$', DashboardEditPageView.as_view(), name="dashboard-edit-page"),
    url(r'edit/(?P<label>[/\w]+)---(?P<key>\w+)/$', DashboardEditPageView.as_view(), name="dashboard-edit-page"),
    url(r'preview/(?P<label>.*)', serve_single_fragment, name="contento-cms-preview"),
    url(r'api/renderers-meta/$', RenderersMetaView.as_view(), name="contento-renderers-meta"),

]
