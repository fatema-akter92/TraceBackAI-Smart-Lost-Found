import hashlib
import uuid
from django.conf import settings
from django.db import models


def generate_tracking_code():
    return f"TB-{uuid.uuid4().hex[:8].upper()}"


class Category(models.Model):
    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(max_length=80, unique=True)
    icon = models.CharField(max_length=50, default='fas fa-cube', help_text="FontAwesome icon class")
    description = models.TextField(blank=True)
    ai_keywords = models.TextField(
        blank=True,
        help_text="Comma-separated keywords for AI categorization (e.g., laptop, macbook, hp, dell, computer)"
    )

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name


class ItemReport(models.Model):
    REPORT_TYPE_CHOICES = [
        ('lost', 'Lost Item (I lost something)'),
        ('found', 'Found Item (I found something)'),
    ]

    STATUS_CHOICES = [
        ('open', 'Open / Searching'),
        ('potential_match', 'Potential AI Match Found'),
        ('under_verification', 'Ownership Verification In Progress'),
        ('recovered', 'Successfully Recovered & Closed'),
        ('closed', 'Closed / Archived'),
    ]

    tracking_code = models.CharField(max_length=20, unique=True, default=generate_tracking_code, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reports')
    report_type = models.CharField(max_length=10, choices=REPORT_TYPE_CHOICES)
    title = models.CharField(max_length=200, help_text="Brief item title (e.g., Black HP Pavilion Laptop 15-inch)")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='items')
    primary_color = models.CharField(max_length=50, blank=True, help_text="e.g. Black, Silver, Navy Blue, Red")
    brand = models.CharField(max_length=100, blank=True, help_text="e.g. HP, Apple, Samsung, Lenovo, Casio, etc.")
    description = models.TextField(help_text="Detailed description of features, markings, case, etc.")
    image = models.ImageField(upload_to='item_photos/', blank=True, null=True)
    image_hash = models.CharField(max_length=64, blank=True, help_text="Hash for duplicate image fraud detection")

    # Time & Location (Privacy-Safe Approximate Map)
    incident_date = models.DateField(help_text="Date lost or found")
    incident_time = models.TimeField(blank=True, null=True, help_text="Approximate time")
    location_name = models.CharField(max_length=255, help_text="General location, campus, or landmark")
    latitude = models.DecimalField(max_digits=9, decimal_places=6, default=23.875900, help_text="Approximate latitude")
    longitude = models.DecimalField(max_digits=9, decimal_places=6, default=90.323500, help_text="Approximate longitude")
    safe_area_display = models.CharField(max_length=200, blank=True, help_text="Sanitized public display area (e.g. DIU Main Campus Area)")

    # JourneyTrace — Feature 9: Transport Recovery
    is_transit_item = models.BooleanField(default=False, help_text="Lost or found on public transit / transport?")
    transit_vehicle_name = models.CharField(max_length=100, blank=True, help_text="Bus, Train, Shuttle, Metro name or vehicle plate")
    transit_route = models.CharField(max_length=150, blank=True, help_text="e.g. Uttara to Motijheel, Mohakhali to DIU Campus")
    transit_boarding_point = models.CharField(max_length=100, blank=True, help_text="Station/Stop where you boarded")
    transit_drop_point = models.CharField(max_length=100, blank=True, help_text="Station/Stop where you got off")
    transit_seat_number = models.CharField(max_length=50, blank=True, help_text="Seat / Compartment / Bogie number")

    # Feature 7: SecretProof — Hidden Ownership Verification Data
    secret_proof_details = models.TextField(
        blank=True,
        help_text="PRIVATE: Secret details only real owner knows (e.g., sticker under battery, partial serial number, lock wallpaper, hidden tear). Never shown publicly."
    )

    # Status & Moderation
    status = models.CharField(max_length=25, choices=STATUS_CHOICES, default='open')
    is_approved = models.BooleanField(default=True)
    is_flagged_fraud = models.BooleanField(default=False)
    fraud_risk_score = models.IntegerField(default=0, help_text="0-100 calculated risk")
    fraud_reason = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"[{self.get_report_type_display().split()[0].upper()}] {self.title} ({self.tracking_code})"

    @property
    def display_image_url(self):
        """Returns image URL with automatic mtime cache buster so replacing files on disk updates immediately in browser."""
        if self.image:
            try:
                mtime = int(self.image.storage.get_modified_time(self.image.name).timestamp())
                return f"{self.image.url}?v={mtime}"
            except Exception:
                return self.image.url
        return ""

    def save(self, *args, **kwargs):
        if not self.safe_area_display and self.location_name:
            # Mask or sanitize area to protect user's specific address
            self.safe_area_display = self.location_name.split(',')[0].strip()
        super().save(*args, **kwargs)


class ClaimRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Verification Review'),
        ('approved', 'Ownership Approved - Awaiting Handover'),
        ('rejected', 'Claim Rejected'),
        ('completed', 'Handover Completed'),
    ]

    item = models.ForeignKey(ItemReport, on_delete=models.CASCADE, related_name='claims')
    claimant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='submitted_claims')
    linked_lost_report = models.ForeignKey(
        ItemReport,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='matching_claims',
        help_text="Optional linked lost report created earlier by this claimant"
    )
    claimant_secret_proof = models.TextField(
        help_text="Secret proof provided by claimant (serial number part, scratch details, purchase receipt info, identifying quirks)"
    )
    proof_document = models.FileField(upload_to='proof_documents/', blank=True, null=True, help_text="Receipt, warranty card, or photo proof")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    admin_notes = models.TextField(blank=True, help_text="Official verification audit notes")
    verified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='verified_claims'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Claim #{self.id} on {self.item.title} by {self.claimant.username} [{self.status}]"


class Complaint(models.Model):
    COMPLAINT_TYPES = [
        ('fake_report', 'Suspected Fake or Prank Report'),
        ('duplicate_spam', 'Duplicate Spam Posting'),
        ('false_claim', 'Someone Making False Ownership Claim'),
        ('inappropriate', 'Offensive or Inappropriate Content'),
        ('other', 'Other Issue'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('investigating', 'Under Investigation'),
        ('resolved', 'Resolved'),
        ('dismissed', 'Dismissed'),
    ]

    reporter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='filed_complaints')
    reported_item = models.ForeignKey(ItemReport, on_delete=models.CASCADE, blank=True, null=True, related_name='complaints')
    complaint_type = models.CharField(max_length=30, choices=COMPLAINT_TYPES)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    admin_action_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Complaint #{self.id} ({self.get_complaint_type_display()})"
