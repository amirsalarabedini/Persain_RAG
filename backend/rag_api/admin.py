from django.contrib import admin
from .models import Document, QueryHistory

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'file_name', 'file_type', 'upload_date', 'chunk_count')
    search_fields = ('title', 'file_name')
    list_filter = ('file_type', 'upload_date')

@admin.register(QueryHistory)
class QueryHistoryAdmin(admin.ModelAdmin):
    list_display = ('query_text_short', 'timestamp')
    search_fields = ('query_text', 'response_text')
    list_filter = ('timestamp',)
    filter_horizontal = ('documents_retrieved',)
    
    def query_text_short(self, obj):
        return obj.query_text[:50] + '...' if len(obj.query_text) > 50 else obj.query_text
    
    query_text_short.short_description = 'Query'