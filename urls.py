"""
Defines the URL routes for this app.
"""

from django.conf.urls import url

from .views import NodebbDashboardView

urlpatterns = [
    url(r'', NodebbDashboardView.as_view(), name='nodebb_dashboard'),
]
