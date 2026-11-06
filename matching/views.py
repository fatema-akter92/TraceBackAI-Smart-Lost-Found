from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import MatchNotification, MatchRecord


@login_required
def notifications_list(request):
    notifs = MatchNotification.objects.filter(recipient=request.user)
    # Mark all as read when opening page
    notifs.filter(is_read=False).update(is_read=True)
    return render(request, 'matching/notifications.html', {'notifications': notifs})


@login_required
def mark_notification_read(request, notification_id):
    notif = get_object_or_404(MatchNotification, id=notification_id, recipient=request.user)
    notif.is_read = True
    notif.save(update_fields=['is_read'])
    return redirect('notifications_list')


@login_required
def handle_match_action(request, match_id, action):
    match = get_object_or_404(MatchRecord, id=match_id)

    # Check if user owns either lost or found item
    if request.user != match.lost_item.user and request.user != match.found_item.user and not request.user.is_desk_staff:
        messages.error(request, "Permission denied.")
        return redirect('dashboard')

    if action == 'accept':
        match.status = 'accepted'
        match.save(update_fields=['status'])
        messages.success(
            request,
            "Match accepted! You can now proceed to submit SecretProof verification or contact the desk."
        )
        return redirect('submit_claim', item_id=match.found_item.id)

    elif action == 'reject':
        match.status = 'rejected'
        match.save(update_fields=['status'])
        messages.info(request, "Match dismissed.")

    return redirect('item_detail', item_id=match.lost_item.id)
