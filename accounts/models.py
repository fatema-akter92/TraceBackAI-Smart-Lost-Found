from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = [
        ('general', 'General User'),
        ('student', 'Student / Campus Member'),
        ('transport', 'Transport Authority Officer'),
        ('staff', 'Institutional Desk Staff'),
        ('admin', 'System Administrator'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='general')
    phone = models.CharField(max_length=20, blank=True, null=True, help_text="Contact number (kept private)")
    institution_name = models.CharField(max_length=150, blank=True, null=True, help_text="University/Company/Organization name")
    student_id_or_badge = models.CharField(max_length=50, blank=True, null=True, help_text="Student ID or Staff Badge Number")
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    reputation_score = models.IntegerField(default=100)
    is_verified_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        role_label = self.get_role_display()
        return f"{self.username} ({role_label})"

    @property
    def is_desk_staff(self):
        return self.role in ['staff', 'transport', 'admin'] or self.is_superuser
