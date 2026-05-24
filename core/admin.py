from django.contrib import admin
from .models import Report


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('report_type', 'location', 'status', 'priority', 'created_at')
    list_filter = ('status', 'report_type', 'priority')
    search_fields = ('location', 'description')


admin.site.site_header = "Smart Campus Admin"
admin.site.site_title = "Smart Campus"
admin.site.index_title = "Welcome Admin"