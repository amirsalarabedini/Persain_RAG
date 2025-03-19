from django.urls import path
from . import views
from . import views_sources

urlpatterns = [
    path('documents/', views.DocumentListView.as_view(), name='document-list'),
    path('documents/upload/', views.DocumentUploadView.as_view(), name='document-upload'),
    path('query/', views.QueryView.as_view(), name='query'),
    path('query/sources/', views_sources.QuerySourcesView.as_view(), name='query-sources'),
    path('query/history/', views.QueryHistoryView.as_view(), name='query-history'),
    path('system/info/', views.SystemInfoView.as_view(), name='system-info'),
]