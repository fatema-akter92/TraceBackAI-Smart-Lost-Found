import uuid
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import LostFoundDesk, CustodyRecord, CustodyLog
from items.models import ItemReport


def desk_list(request):
    desks = LostFoundDesk.objects.filter(is_active=True)
    return render(request, 'custody/desk_list.html', {'desks': desks})


def desk_detail(request, desk_id):
    desk = get_object_or_404(LostFoundDesk, id=desk_id)
    custody_items = CustodyRecord.objects.filter(desk=desk).select_related('item').order_by('-created_at')
    is_desk_manager = request.user.is_authenticated and (request.user == desk.manager or request.user.is_superuser)

    context = {
        'desk': desk,
        'custody_items': custody_items,
        'is_desk_manager': is_desk_manager,
    }
    return render(request, 'custody/desk_detail.html', context)


@login_required
def deposit_item(request, item_id):
    item = get_object_or_404(ItemReport, id=item_id)

    if hasattr(item, 'custody_record'):
        messages.info(request, "This item is already registered in desk custody.")
        return redirect('verify_item_qr', tracking_code=item.tracking_code)

    desks = LostFoundDesk.objects.filter(is_active=True)

    if request.method == 'POST':
        desk_id = request.POST.get('desk_id')
        shelf = request.POST.get('shelf', '')
        notes = request.POST.get('notes', '')

        desk = get_object_or_404(LostFoundDesk, id=desk_id)
        token = uuid.uuid4().hex[:12].upper()

        custody = CustodyRecord.objects.create(
            item=item,
            desk=desk,
            tracking_token=token,
            current_status='in_storage',
            storage_bin_or_shelf=shelf,
            received_by=request.user
        )
        custody.generate_qr()
        custody.save()

        CustodyLog.objects.create(
            custody_record=custody,
            action="Item deposited into desk storage",
            actor=request.user,
            notes=f"Stored in {shelf}. Note: {notes}"
        )

        messages.success(request, f"QR Custody Pass generated successfully! Item assigned tracking token {token}.")
        return redirect('verify_item_qr', tracking_code=item.tracking_code)

    return render(request, 'custody/deposit_form.html', {'item': item, 'desks': desks})


def qr_scanner(request):
    """
    Feature 8: QR Scanner interface using HTML5 / jsQR and manual code search.
    """
    return render(request, 'custody/qr_scanner.html')


def verify_item_qr(request, tracking_code):
    item = get_object_or_404(ItemReport, tracking_code=tracking_code)
    custody = getattr(item, 'custody_record', None)

    logs = custody.logs.all() if custody else []

    context = {
        'item': item,
        'custody': custody,
        'logs': logs,
    }
    return render(request, 'custody/verify_qr.html', context)


@login_required
def execute_handover(request, custody_id):
    custody = get_object_or_404(CustodyRecord, id=custody_id)

    if not request.user.is_desk_staff:
        messages.error(request, "Only authorized desk staff can record official item handover.")
        return redirect('verify_item_qr', tracking_code=custody.item.tracking_code)

    if request.method == 'POST':
        remarks = request.POST.get('remarks', '')
        owner_name = request.POST.get('owner_name', '')
        owner_id_proof = request.POST.get('owner_id_proof', '')

        # Check if an approved claimant is attached
        approved_claim = custody.item.claims.filter(status='approved').first()

        custody.current_status = 'returned'
        custody.handed_over_to = approved_claim.claimant if approved_claim else None
        custody.handover_date = timezone.now()
        custody.handover_remarks = f"Handed to: {owner_name} (ID: {owner_id_proof}). Remarks: {remarks}"
        custody.save()

        # Update item status to recovered
        custody.item.status = 'recovered'
        custody.item.save(update_fields=['status'])

        # Log custody event
        CustodyLog.objects.create(
            custody_record=custody,
            action="Official Handover to Verified Owner Completed",
            actor=request.user,
            notes=f"Delivered to {owner_name} by staff {request.user.username}."
        )

        messages.success(request, f"Item '{custody.item.title}' has been successfully handed over and closed!")
        return redirect('handover_receipt', custody_id=custody.id)

    return render(request, 'custody/handover_confirm.html', {'custody': custody})


def handover_receipt(request, custody_id):
    custody = get_object_or_404(CustodyRecord, id=custody_id)
    return render(request, 'custody/handover_receipt.html', {'custody': custody})
