import hashlib
from django.conf import settings
from django.db import models
from items.models import ItemReport


class ChatThread(models.Model):
    item = models.ForeignKey(ItemReport, on_delete=models.CASCADE, related_name='chat_threads')
    initiator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='initiated_threads')
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_threads')
    
    # Anonymized safety handles to avoid leaking phone / email
    alias_initiator = models.CharField(max_length=60, default="Seeker")
    alias_recipient = models.CharField(max_length=60, default="Finder")
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f"Safe Channel #{self.id} for {self.item.title}"

    def get_alias_for_user(self, user):
        if user == self.initiator:
            return self.alias_initiator
        elif user == self.recipient:
            return self.alias_recipient
        elif user.is_desk_staff:
            return f"Official Desk Staff ({user.username})"
        return "Anonymous Member"


class ChatMessage(models.Model):
    thread = models.ForeignKey(ChatThread, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"Msg from {self.sender.username} at {self.timestamp.strftime('%H:%M')}"

    @property
    def sender_alias(self):
        return self.thread.get_alias_for_user(self.sender)
