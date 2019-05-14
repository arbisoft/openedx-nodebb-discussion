"""
Defines the URL routes for this app.
"""

from django.conf.urls import url

from .views import EdlyDiscussionDashboardView

urlpatterns = [
    url(r'', EdlyDiscussionDashboardView.as_view(), name='edly_discussion_dashboard'),
]
