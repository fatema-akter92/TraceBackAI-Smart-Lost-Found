from django.contrib import admin
from .models import MatchRecord, MatchNotification


@admin.register(MatchRecord)
class MatchRecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'lost_item', 'found_item', 'similarity_score', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('lost_item__title', 'found_item__title')


@admin.register(MatchNotification)
class MatchNotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipient', 'title', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('title', 'message', 'recipient__username')
