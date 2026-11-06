from django.contrib import admin
from .models import LostFoundDesk, CustodyRecord, CustodyLog


@admin.register(LostFoundDesk)
class LostFoundDeskAdmin(admin.ModelAdmin):
    list_display = ('name', 'organization', 'desk_type', 'location_details', 'contact_phone', 'is_active')
    list_filter = ('desk_type', 'is_active')
    search_fields = ('name', 'organization', 'location_details')


class CustodyLogInline(admin.TabularInline):
    model = CustodyLog
    extra = 0
    readonly_fields = ('timestamp',)


@admin.register(CustodyRecord)
class CustodyRecordAdmin(admin.ModelAdmin):
    list_display = ('tracking_token', 'item', 'desk', 'current_status', 'storage_bin_or_shelf', 'received_by', 'created_at')
    list_filter = ('current_status', 'desk')
    search_fields = ('tracking_token', 'item__title', 'storage_bin_or_shelf')
    inlines = [CustodyLogInline]
