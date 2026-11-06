from django.contrib import admin
from .models import Category, ItemReport, ClaimRequest, Complaint


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'icon')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(ItemReport)
class ItemReportAdmin(admin.ModelAdmin):
    list_display = ('tracking_code', 'title', 'report_type', 'category', 'status', 'incident_date', 'location_name', 'is_flagged_fraud')
    list_filter = ('report_type', 'status', 'category', 'is_transit_item', 'is_flagged_fraud')
    search_fields = ('title', 'description', 'tracking_code', 'location_name', 'brand')
    readonly_fields = ('tracking_code', 'created_at', 'updated_at', 'image_hash')


@admin.register(ClaimRequest)
class ClaimRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'item', 'claimant', 'status', 'created_at', 'verified_by')
    list_filter = ('status', 'created_at')
    search_fields = ('item__title', 'claimant__username', 'claimant_secret_proof')


@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ('id', 'reporter', 'complaint_type', 'reported_item', 'status', 'created_at')
    list_filter = ('complaint_type', 'status')
    search_fields = ('description', 'reporter__username')
