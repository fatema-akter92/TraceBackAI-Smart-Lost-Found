from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(
        choices=User.ROLE_CHOICES,
        required=True,
        initial='student',
        help_text="Choose your role to get appropriate access and features"
    )
    institution_name = forms.CharField(
        max_length=150,
        required=False,
        help_text="e.g. Daffodil International University (DIU), Dhaka University, Bangladesh Railway"
    )
    student_id_or_badge = forms.CharField(
        max_length=50,
        required=False,
        help_text="Student ID number or Employee / Staff ID badge"
    )
    phone = forms.CharField(
        max_length=20,
        required=False,
        help_text="Phone number for emergency desk contact (kept hidden from public)"
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'role', 'institution_name', 'student_id_or_badge', 'phone']


class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'phone', 'institution_name', 'student_id_or_badge', 'avatar']
