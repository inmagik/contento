from django.conf.urls import url
from .dashboard_views import  (
    DashboardIndexView, DashboardPagesView, DashboardSettingsView
)

urlpatterns = [
    url(r'^$', DashboardIndexView.as_view(), name="dashboard-index"),
    url(r'pages', DashboardPagesView.as_view(), name="dashboard-pages"),
    url(r'settings', DashboardSettingsView.as_view(), name="dashboard-settings"),
]
