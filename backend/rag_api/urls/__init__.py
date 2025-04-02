from django.urls import path, include

urlpatterns = [
    path('', include('rag_api.urls.api_urls')),
] 