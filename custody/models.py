import io
import qrcode
from django.conf import settings
from django.core.files.base import ContentFile
from django.db import models
from items.models import ItemReport


class LostFoundDesk(models.Model):
    DESK_TYPES = [
        ('university', 'University / Campus Desk'),
        ('transport', 'Transport Station / Bus Terminal'),
        ('hospital', 'Hospital Reception / Security Desk'),
        ('mall', 'Shopping Mall / Public Center'),
        ('police', 'Security / Lost & Found Center'),
    ]

    name = models.CharField(max_length=150)
    organization = models.CharField(max_length=150, help_text="e.g. Daffodil International University, Bangladesh Railway")
    desk_type = models.CharField(max_length=20, choices=DESK_TYPES, default='university')
    location_details = models.CharField(max_length=255, help_text="Building, room number, or floor")
    contact_phone = models.CharField(max_length=30)
    contact_email = models.EmailField(blank=True)
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='managed_desks')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.organization}"


class CustodyRecord(models.Model):
    CUSTODY_STATUS = [
        ('deposited', 'Deposited at Desk'),
        ('in_storage', 'Stored Safely in Locker/Shelf'),
        ('owner_verified', 'Owner Verified via SecretProof'),
        ('returned', 'Handed Over & Returned to Owner'),
        ('transferred', 'Transferred to Central Depot'),
    ]

    item = models.OneToOneField(ItemReport, on_delete=models.CASCADE, related_name='custody_record')
    desk = models.ForeignKey(LostFoundDesk, on_delete=models.CASCADE, related_name='items_in_custody')
    tracking_token = models.CharField(max_length=32, unique=True, editable=False)
    qr_image = models.ImageField(upload_to='qr_codes/', blank=True, null=True)
    current_status = models.CharField(max_length=25, choices=CUSTODY_STATUS, default='deposited')
    storage_bin_or_shelf = models.CharField(max_length=80, blank=True, help_text="e.g., Locker A3, Bin 12")
    received_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='received_custodies'
    )
    handed_over_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='recovered_items'
    )
    handover_date = models.DateTimeField(blank=True, null=True)
    handover_remarks = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Custody [{self.tracking_token}] - {self.item.title} ({self.get_current_status_display()})"

    def generate_qr(self):
        # Generates a QR Code containing a verification URL
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=8,
            border=3,
        )
        # Content format: Verification URL / code
        verify_data = f"TRACEBACK_BD_ITEM:{self.item.tracking_code}:{self.tracking_token}"
        qr.add_data(verify_data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="#0891b2", back_color="#ffffff")
        
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        filename = f"qr_{self.item.tracking_code}.png"
        self.qr_image.save(filename, ContentFile(buffer.getvalue()), save=False)


class CustodyLog(models.Model):
    custody_record = models.ForeignKey(CustodyRecord, on_delete=models.CASCADE, related_name='logs')
    action = models.CharField(max_length=150)
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    notes = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.action} on {self.timestamp.strftime('%Y-%m-%d %H:%M')}"
