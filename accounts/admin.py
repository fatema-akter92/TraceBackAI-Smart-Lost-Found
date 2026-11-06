from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'institution_name', 'reputation_score', 'is_verified_staff', 'is_staff')
    list_filter = ('role', 'is_verified_staff', 'is_staff', 'is_superuser')
    fieldsets = UserAdmin.fieldsets + (
        ('TraceBack BD Profile', {
            'fields': ('role', 'phone', 'institution_name', 'student_id_or_badge', 'avatar', 'reputation_score', 'is_verified_staff')
        }),
    )
