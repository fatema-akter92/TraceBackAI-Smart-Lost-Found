import uuid
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from django.utils import timezone

from .models import ItemReport, Category, ClaimRequest, Complaint
from .forms import LostItemReportForm, FoundItemReportForm, ClaimRequestForm, ComplaintForm
from .fraud import compute_image_hash, evaluate_report_fraud_risk
from matching.engine import run_ai_matching_for_item
from custody.models import LostFoundDesk, CustodyRecord, CustodyLog


def item_list(request):
    report_type = request.GET.get('type', '')
    category_id = request.GET.get('category', '')
    query = request.GET.get('q', '').strip()
    transit = request.GET.get('transit', '')
    status = request.GET.get('status', '')

    items = ItemReport.objects.filter(is_approved=True)

    if report_type in ['lost', 'found']:
        items = items.filter(report_type=report_type)

    if category_id:
        items = items.filter(category_id=category_id)

    if transit == '1':
        items = items.filter(is_transit_item=True)

    if status:
        items = items.filter(status=status)

    if query:
        items = items.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(location_name__icontains=query) |
            Q(brand__icontains=query) |
            Q(primary_color__icontains=query) |
            Q(transit_vehicle_name__icontains=query) |
            Q(tracking_code__icontains=query)
        )

    categories = Category.objects.all()

    context = {
        'items': items[:40],
        'categories': categories,
        'selected_type': report_type,
        'selected_category': category_id,
        'selected_query': query,
        'selected_transit': transit,
        'selected_status': status,
        'total_count': items.count(),
    }
    return render(request, 'items/item_list.html', context)


@login_required
def report_lost(request):
    if request.method == 'POST':
        form = LostItemReportForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.user = request.user
            item.report_type = 'lost'

            if 'image' in request.FILES:
                item.image_hash = compute_image_hash(request.FILES['image'])

            # Evaluate Fraud Risk
            is_suspicious, risk_score, reasons = evaluate_report_fraud_risk(item)
            item.fraud_risk_score = risk_score
            if is_suspicious:
                item.is_flagged_fraud = True
                item.fraud_reason = " ; ".join(reasons)

            item.save()

            # Execute AI Matching Engine
            matches = run_ai_matching_for_item(item)

            if is_suspicious:
                messages.warning(
                    request,
                    "Your report was submitted. Our system flagged it for brief administrative review."
                )
            else:
                messages.success(
                    request,
                    f"Lost item report created successfully! Tracking code: {item.tracking_code}."
                )

            if matches:
                messages.info(
                    request,
                    f"AI Smart Match: Found {len(matches)} potential matching item(s) already reported!"
                )

            return redirect('item_detail', item_id=item.id)
    else:
        form = LostItemReportForm()

    categories = Category.objects.all()
    return render(request, 'items/report_lost.html', {'form': form, 'categories': categories})


@login_required
def report_found(request):
    if request.method == 'POST':
        form = FoundItemReportForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.user = request.user
            item.report_type = 'found'

            if 'image' in request.FILES:
                item.image_hash = compute_image_hash(request.FILES['image'])

            # Evaluate Fraud Risk
            is_suspicious, risk_score, reasons = evaluate_report_fraud_risk(item)
            item.fraud_risk_score = risk_score
            if is_suspicious:
                item.is_flagged_fraud = True
                item.fraud_reason = " ; ".join(reasons)

            item.save()

            # If user deposited item at an institutional desk
            selected_desk = form.cleaned_data.get('handover_desk')
            if selected_desk:
                token = uuid.uuid4().hex[:12].upper()
                custody = CustodyRecord.objects.create(
                    item=item,
                    desk=selected_desk,
                    tracking_token=token,
                    current_status='deposited',
                    received_by=request.user
                )
                custody.generate_qr()
                custody.save()
                CustodyLog.objects.create(
                    custody_record=custody,
                    action="Item reported and registered at Institutional Desk",
                    actor=request.user,
                    notes=f"Reported by {request.user.username}. Stored at {selected_desk.name}."
                )

            # Execute AI Matching Engine
            matches = run_ai_matching_for_item(item)

            messages.success(
                request,
                f"Thank you for being a good citizen! Found item report logged with code: {item.tracking_code}."
            )

            if matches:
                messages.info(
                    request,
                    f"AI Smart Match: Found {len(matches)} open seeker reports that might match this item!"
                )

            return redirect('item_detail', item_id=item.id)
    else:
        form = FoundItemReportForm()

    categories = Category.objects.all()
    desks = LostFoundDesk.objects.filter(is_active=True)
    return render(request, 'items/report_found.html', {'form': form, 'categories': categories, 'desks': desks})


def item_detail(request, item_id):
    item = get_object_or_404(ItemReport, id=item_id)
    is_owner = request.user.is_authenticated and (item.user == request.user)
    is_staff = request.user.is_authenticated and request.user.is_desk_staff

    # Custody Record (QR code, desk custody)
    custody = getattr(item, 'custody_record', None)

    # Claims on this item
    claims = item.claims.all().order_by('-created_at') if (is_owner or is_staff) else []

    # Check if current user already submitted a claim on this found item
    user_claim = None
    if request.user.is_authenticated and not is_owner:
        user_claim = item.claims.filter(claimant=request.user).first()

    # AI Matches
    if item.report_type == 'lost':
        matches = item.lost_matches.filter(similarity_score__gte=35.0).order_by('-similarity_score')
    else:
        matches = item.found_matches.filter(similarity_score__gte=35.0).order_by('-similarity_score')

    context = {
        'item': item,
        'is_owner': is_owner,
        'is_staff': is_staff,
        'custody': custody,
        'claims': claims,
        'user_claim': user_claim,
        'matches': matches[:5],
    }
    return render(request, 'items/item_detail.html', context)


@login_required
def submit_claim(request, item_id):
    item = get_object_or_404(ItemReport, id=item_id, report_type='found')

    if item.user == request.user:
        messages.error(request, "You reported finding this item; you cannot claim it yourself.")
        return redirect('item_detail', item_id=item.id)

    # Check existing pending claim
    existing = ClaimRequest.objects.filter(item=item, claimant=request.user).first()
    if existing:
        messages.info(request, "You have already submitted a claim for this item. Check status below.")
        return redirect('item_detail', item_id=item.id)

    if request.method == 'POST':
        form = ClaimRequestForm(request.POST, request.FILES)
        if form.is_valid():
            claim = form.save(commit=False)
            claim.item = item
            claim.claimant = request.user

            # Look up if user has an open lost report of the same category
            linked_lost = ItemReport.objects.filter(
                user=request.user,
                report_type='lost',
                category=item.category,
                status__in=['open', 'potential_match']
            ).first()
            if linked_lost:
                claim.linked_lost_report = linked_lost

            claim.save()

            item.status = 'under_verification'
            item.save(update_fields=['status'])

            messages.success(
                request,
                "Your SecretProof claim has been submitted! Our desk staff/admin will privately verify your proof."
            )
            return redirect('item_detail', item_id=item.id)
    else:
        form = ClaimRequestForm()

    return render(request, 'items/submit_claim.html', {'item': item, 'form': form})


@login_required
def review_claim(request, claim_id, action):
    claim = get_object_or_404(ClaimRequest, id=claim_id)

    if not (request.user.is_desk_staff or request.user == claim.item.user):
        messages.error(request, "You are not authorized to review this claim.")
        return redirect('item_detail', item_id=claim.item.id)

    if action == 'approve':
        claim.status = 'approved'
        claim.verified_by = request.user
        claim.resolved_at = timezone.now()
        claim.save()

        # Update item status
        claim.item.status = 'under_verification'
        claim.item.save(update_fields=['status'])

        # If custody record exists, update to owner_verified
        if hasattr(claim.item, 'custody_record'):
            custody = claim.item.custody_record
            custody.current_status = 'owner_verified'
            custody.save(update_fields=['current_status'])
            CustodyLog.objects.create(
                custody_record=custody,
                action="Claim Approved via SecretProof",
                actor=request.user,
                notes=f"Claim #{claim.id} approved by {request.user.username}. Ready for item collection."
            )

        messages.success(request, f"Claim #{claim.id} APPROVED! The claimant can now collect the item.")

    elif action == 'reject':
        claim.status = 'rejected'
        claim.verified_by = request.user
        claim.resolved_at = timezone.now()
        claim.save()
        messages.info(request, f"Claim #{claim.id} rejected.")

    return redirect('item_detail', item_id=claim.item.id)


@login_required
def update_item_status(request, item_id, new_status):
    item = get_object_or_404(ItemReport, id=item_id)

    if not (item.user == request.user or request.user.is_desk_staff):
        messages.error(request, "Permission denied.")
        return redirect('item_detail', item_id=item.id)

    valid_statuses = dict(ItemReport.STATUS_CHOICES).keys()
    if new_status in valid_statuses:
        item.status = new_status
        item.save(update_fields=['status'])
        messages.success(request, f"Item status updated to '{item.get_status_display()}'.")

    return redirect('item_detail', item_id=item.id)


def item_matches(request, item_id):
    item = get_object_or_404(ItemReport, id=item_id)
    if item.report_type == 'lost':
        matches = list(item.lost_matches.all().order_by('-similarity_score'))
        for m in matches:
            m.candidate = m.found_item
    else:
        matches = list(item.found_matches.all().order_by('-similarity_score'))
        for m in matches:
            m.candidate = m.lost_item

    return render(request, 'matching/match_results.html', {'item': item, 'matches': matches})


@login_required
def file_complaint(request):
    item_id = request.GET.get('item_id')
    reported_item = None
    if item_id:
        reported_item = get_object_or_404(ItemReport, id=item_id)

    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
            comp = form.save(commit=False)
            comp.reporter = request.user
            comp.reported_item = reported_item
            comp.save()
            messages.success(request, "Your report has been submitted to the moderation team.")
            return redirect('item_list')
    else:
        form = ComplaintForm()

    return render(request, 'items/file_complaint.html', {'form': form, 'reported_item': reported_item})


@login_required
def admin_fraud_review(request):
    if not request.user.is_desk_staff:
        messages.error(request, "Access restricted to administrators and authorized staff.")
        return redirect('home')

    flagged_items = ItemReport.objects.filter(is_flagged_fraud=True).order_by('-fraud_risk_score')
    complaints = Complaint.objects.filter(status='pending').order_by('-created_at')

    return render(request, 'items/fraud_alerts.html', {
        'flagged_items': flagged_items,
        'complaints': complaints,
    })


def ai_category_suggest(request):
    """
    Feature 4: AI Image Recognition & Automatic Category Suggestion
    Takes text keywords, title, or filename and scores candidate categories.
    """
    text = request.GET.get('text', '').lower()
    filename = request.GET.get('filename', '').lower()
    combined = f"{text} {filename}"

    best_category = None
    best_score = 0

    for cat in Category.objects.all():
        score = 0
        keywords = [k.strip().lower() for k in cat.ai_keywords.split(',') if k.strip()]
        for kw in keywords:
            if kw in combined:
                score += 15
        if cat.name.lower() in combined:
            score += 30

        if score > best_score:
            best_score = score
            best_category = cat

    if best_category and best_score >= 15:
        return JsonResponse({
            'status': 'success',
            'category_id': best_category.id,
            'category_name': best_category.name,
            'confidence': min(98, 50 + best_score),
        })

    return JsonResponse({'status': 'none', 'category_id': None})
