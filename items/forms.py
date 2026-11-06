from django import forms
from .models import ItemReport, ClaimRequest, Complaint, Category
from custody.models import LostFoundDesk


class LostItemReportForm(forms.ModelForm):
    incident_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-input'}),
        help_text="When did you lose the item?"
    )
    incident_time = forms.TimeField(
        required=False,
        widget=forms.TimeInput(attrs={'type': 'time', 'class': 'form-input'}),
        help_text="Approximate time"
    )

    class Meta:
        model = ItemReport
        fields = [
            'title', 'category', 'primary_color', 'brand', 'description', 'image',
            'incident_date', 'incident_time', 'location_name', 'latitude', 'longitude',
            'is_transit_item', 'transit_vehicle_name', 'transit_route',
            'transit_boarding_point', 'transit_drop_point', 'transit_seat_number',
            'secret_proof_details'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Describe visible features, stickers, marks, case, scratches...'}),
            'secret_proof_details': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'CONFIDENTIAL: Enter serial number digits, private scratches, wallpaper image, or unique marks that only you know. Admin will use this to verify ownership claims.'
            }),
            'latitude': forms.HiddenInput(),
            'longitude': forms.HiddenInput(),
        }


class FoundItemReportForm(forms.ModelForm):
    handover_desk = forms.ModelChoiceField(
        queryset=LostFoundDesk.objects.filter(is_active=True),
        required=False,
        empty_label="Select Institutional Desk (Optional / Recommended)",
        help_text="If you deposited this at a campus or station desk, select it here."
    )
    incident_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-input'}),
        help_text="When did you find the item?"
    )
    incident_time = forms.TimeField(
        required=False,
        widget=forms.TimeInput(attrs={'type': 'time', 'class': 'form-input'})
    )

    class Meta:
        model = ItemReport
        fields = [
            'title', 'category', 'primary_color', 'brand', 'description', 'image',
            'incident_date', 'incident_time', 'location_name', 'latitude', 'longitude',
            'is_transit_item', 'transit_vehicle_name', 'transit_route',
            'transit_boarding_point', 'transit_drop_point', 'transit_seat_number'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Describe general appearance. Do not reveal private serial numbers or unlock passwords!'}),
            'latitude': forms.HiddenInput(),
            'longitude': forms.HiddenInput(),
        }


class ClaimRequestForm(forms.ModelForm):
    class Meta:
        model = ClaimRequest
        fields = ['claimant_secret_proof', 'proof_document']
        widgets = {
            'claimant_secret_proof': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Provide conclusive proof of ownership: partial serial number, unique scratches, receipt purchase date/store, lock screen wallpaper, or contents of the wallet/bag.'
            }),
        }


class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['complaint_type', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Explain why you are reporting this item or user...'}),
        }
