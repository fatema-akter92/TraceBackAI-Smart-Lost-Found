from django.conf import settings
from django.db import models
from items.models import ItemReport


class MatchRecord(models.Model):
    STATUS_CHOICES = [
        ('suggested', 'Suggested AI Match'),
        ('accepted', 'Accepted by Seeker (In Verification)'),
        ('rejected', 'Dismissed / Not a Match'),
        ('recovered', 'Confirmed Recovery!'),
    ]

    lost_item = models.ForeignKey(ItemReport, on_delete=models.CASCADE, related_name='lost_matches')
    found_item = models.ForeignKey(ItemReport, on_delete=models.CASCADE, related_name='found_matches')
    
    # AI Multi-Dimensional Scores (0-100)
    similarity_score = models.FloatField(default=0.0, help_text="Total weighted match score")
    category_score = models.FloatField(default=0.0)
    text_score = models.FloatField(default=0.0)
    color_brand_score = models.FloatField(default=0.0)
    location_score = models.FloatField(default=0.0)
    time_score = models.FloatField(default=0.0)

    # Human Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='suggested')
    reviewed_by_seeker = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('lost_item', 'found_item')
        ordering = ['-similarity_score', '-created_at']

    def __str__(self):
        return f"AI Match ({self.similarity_score:.1f}%): Lost #{self.lost_item.id} <-> Found #{self.found_item.id}"


class MatchNotification(models.Model):
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    match = models.ForeignKey(MatchRecord, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=150)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Notification for {self.recipient.username}: {self.title}"
