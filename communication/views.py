import random
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import ChatThread, ChatMessage
from items.models import ItemReport


@login_required
def inbox(request):
    threads = ChatThread.objects.filter(
        Q(initiator=request.user) | Q(recipient=request.user)
    ).select_related('item', 'initiator', 'recipient').order_by('-updated_at')

    return render(request, 'communication/inbox.html', {'threads': threads})


@login_required
def start_thread(request, item_id):
    item = get_object_or_404(ItemReport, id=item_id)

    if item.user == request.user:
        messages.info(request, "You cannot message yourself about your own report.")
        return redirect('item_detail', item_id=item.id)

    # Find existing thread between these two users regarding this item
    thread = ChatThread.objects.filter(
        item=item,
        initiator=request.user,
        recipient=item.user
    ).first()

    if not thread:
        thread = ChatThread.objects.filter(
            item=item,
            initiator=item.user,
            recipient=request.user
        ).first()

    if not thread:
        # Generate safe anonymized handles
        alias_init = f"Seeker #{random.randint(100, 999)}" if item.report_type == 'found' else f"Finder #{random.randint(100, 999)}"
        alias_recip = f"Report Owner #{random.randint(100, 999)}"
        thread = ChatThread.objects.create(
            item=item,
            initiator=request.user,
            recipient=item.user,
            alias_initiator=alias_init,
            alias_recipient=alias_recip
        )
        # Automatic system welcome message
        ChatMessage.objects.create(
            thread=thread,
            sender=request.user,
            content=f"Hello! I am reaching out regarding item: '{item.title}'. This is a privacy-protected channel."
        )

    return redirect('thread_detail', thread_id=thread.id)


@login_required
def thread_detail(request, thread_id):
    thread = get_object_or_404(ChatThread, id=thread_id)

    if request.user != thread.initiator and request.user != thread.recipient and not request.user.is_desk_staff:
        messages.error(request, "Access denied to this private conversation.")
        return redirect('inbox')

    if request.method == 'POST':
        body = request.POST.get('message', '').strip()
        if body:
            ChatMessage.objects.create(
                thread=thread,
                sender=request.user,
                content=body
            )
            thread.save()  # update updated_at
            return redirect('thread_detail', thread_id=thread.id)

    # Mark unread messages as read
    thread.messages.exclude(sender=request.user).filter(is_read=False).update(is_read=True)

    chat_messages = thread.messages.all()

    context = {
        'thread': thread,
        'chat_messages': chat_messages,
        'my_alias': thread.get_alias_for_user(request.user),
    }
    return render(request, 'communication/thread_detail.html', context)
