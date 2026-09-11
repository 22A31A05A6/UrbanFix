from django.contrib import admin
from .models import Complaint


@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ('id', 'issue_type', 'user', 'location', 'status', 'created_at')
    list_filter = ('issue_type', 'status')
    search_fields = ('user__username', 'location', 'description')
