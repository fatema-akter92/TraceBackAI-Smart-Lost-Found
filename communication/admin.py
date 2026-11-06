from django.contrib import admin
from .models import ChatThread, ChatMessage


class ChatMessageInline(admin.TabularInline):
    model = ChatMessage
    extra = 0
    readonly_fields = ('timestamp',)


@admin.register(ChatThread)
class ChatThreadAdmin(admin.ModelAdmin):
    list_display = ('id', 'item', 'alias_initiator', 'alias_recipient', 'is_active', 'updated_at')
    inlines = [ChatMessageInline]


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'thread', 'sender', 'is_read', 'timestamp')
    list_filter = ('is_read', 'timestamp')
