from django.urls import path
from ..views import (
    DocumentListView, 
    DocumentUploadView,
    QueryView,
    QueryHistoryView,
    SystemInfoView
)
from ..views_sources import QuerySourcesView

urlpatterns = [
    # Document endpoints
    path('documents/', DocumentListView.as_view(), name='document-list'),
    path('documents/upload/', DocumentUploadView.as_view(), name='document-upload'),
    
    # Query endpoints
    path('query/', QueryView.as_view(), name='query'),
    path('query/sources/', QuerySourcesView.as_view(), name='query-sources'),
    path('query/history/', QueryHistoryView.as_view(), name='query-history'),
    
    # System endpoints
    path('system/info/', SystemInfoView.as_view(), name='system-info'),
] 