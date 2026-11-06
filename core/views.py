import json
from django.shortcuts import render
from django.db.models import Count, Q
from items.models import ItemReport, Category, ClaimRequest
from matching.models import MatchRecord
from custody.models import CustodyRecord, LostFoundDesk


def home(request):
    total_lost = ItemReport.objects.filter(report_type='lost').count()
    total_found = ItemReport.objects.filter(report_type='found').count()
    total_recovered = ItemReport.objects.filter(status='recovered').count()
    total_matches = MatchRecord.objects.count()

    recent_lost = ItemReport.objects.filter(report_type='lost', is_approved=True).order_by('-created_at')[:4]
    recent_found = ItemReport.objects.filter(report_type='found', is_approved=True).order_by('-created_at')[:4]
    categories = Category.objects.all()[:8]
    desks = LostFoundDesk.objects.filter(is_active=True)[:4]

    recovery_rate = round((total_recovered / max(1, total_lost + total_found)) * 100, 1)

    context = {
        'total_lost': total_lost,
        'total_found': total_found,
        'total_recovered': total_recovered,
        'total_matches': total_matches,
        'recovery_rate': recovery_rate,
        'recent_lost': recent_lost,
        'recent_found': recent_found,
        'categories': categories,
        'desks': desks,
    }
    return render(request, 'core/index.html', context)


def map_view(request):
    """
    Feature 5: Interactive Location Map
    Provides approximate pins for lost & found reports to protect privacy.
    """
    items = ItemReport.objects.filter(is_approved=True).exclude(status='closed')
    
    pins = []
    for item in items:
        pins.append({
            'id': item.id,
            'title': item.title,
            'type': item.report_type,
            'category': item.category.name,
            'category_icon': item.category.icon,
            'location_name': item.safe_area_display or item.location_name,
            'lat': float(item.latitude),
            'lng': float(item.longitude),
            'status': item.get_status_display(),
            'date': item.incident_date.strftime('%b %d, %Y'),
            'detail_url': f"/items/{item.id}/",
            'is_transit': item.is_transit_item,
        })

    categories = Category.objects.all()

    context = {
        'pins_json': json.dumps(pins),
        'categories': categories,
        'total_items': len(pins),
    }
    return render(request, 'core/map.html', context)


def analytics_view(request):
    """
    Feature 13: Recovery Analytics Dashboard
    Calculates detailed metrics, charts data for Chart.js.
    """
    total_lost = ItemReport.objects.filter(report_type='lost').count()
    total_found = ItemReport.objects.filter(report_type='found').count()
    total_recovered = ItemReport.objects.filter(status='recovered').count()
    total_matches = MatchRecord.objects.count()
    pending_verifications = ClaimRequest.objects.filter(status='pending').count()
    items_in_custody = CustodyRecord.objects.count()

    recovery_rate = round((total_recovered / max(1, total_lost + total_found)) * 100, 1)

    # Category Breakdown
    cat_data = Category.objects.annotate(
        lost_count=Count('items', filter=Q(items__report_type='lost')),
        found_count=Count('items', filter=Q(items__report_type='found')),
        recovered_count=Count('items', filter=Q(items__status='recovered'))
    )

    category_labels = [c.name for c in cat_data]
    category_lost_counts = [c.lost_count for c in cat_data]
    category_found_counts = [c.found_count for c in cat_data]
    category_recovered_counts = [c.recovered_count for c in cat_data]

    # Status distribution
    status_counts = {
        'Open / Searching': ItemReport.objects.filter(status='open').count(),
        'Potential AI Matches': ItemReport.objects.filter(status='potential_match').count(),
        'Under Verification': ItemReport.objects.filter(status='under_verification').count(),
        'Recovered & Returned': total_recovered,
    }

    # Area Breakdown (top locations)
    area_qs = ItemReport.objects.values('safe_area_display').annotate(count=Count('id')).order_by('-count')[:6]
    area_labels = [a['safe_area_display'] or "Dhaka Central" for a in area_qs]
    area_counts = [a['count'] for a in area_qs]

    context = {
        'total_lost': total_lost,
        'total_found': total_found,
        'total_recovered': total_recovered,
        'total_matches': total_matches,
        'pending_verifications': pending_verifications,
        'items_in_custody': items_in_custody,
        'recovery_rate': recovery_rate,
        'category_labels_json': json.dumps(category_labels),
        'category_lost_json': json.dumps(category_lost_counts),
        'category_found_json': json.dumps(category_found_counts),
        'category_recovered_json': json.dumps(category_recovered_counts),
        'status_labels_json': json.dumps(list(status_counts.keys())),
        'status_values_json': json.dumps(list(status_counts.values())),
        'area_labels_json': json.dumps(area_labels),
        'area_counts_json': json.dumps(area_counts),
    }
    return render(request, 'core/analytics.html', context)


def about_view(request):
    desks = LostFoundDesk.objects.filter(is_active=True)
    return render(request, 'core/about.html', {'desks': desks})
