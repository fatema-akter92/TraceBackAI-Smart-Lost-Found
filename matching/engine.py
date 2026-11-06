import math
import re
from datetime import datetime
from django.utils import timezone
from .models import MatchRecord, MatchNotification

# Common English and Bengali stopwords to filter out for clean text comparison
STOPWORDS = {
    'the', 'a', 'an', 'in', 'on', 'at', 'to', 'for', 'of', 'and', 'or', 'is', 'was', 'my', 'i', 'it',
    'lost', 'found', 'have', 'has', 'had', 'with', 'by', 'from', 'this', 'that', 'there', 'please', 'help',
    'campus', 'room', 'floor', 'around', 'near', 'yesterday', 'today', 'am', 'pm'
}


def tokenize_text(text: str) -> set:
    if not text:
        return set()
    words = re.findall(r'[a-zA-Z0-9]+', text.lower())
    return {w for w in words if len(w) > 2 and w not in STOPWORDS}


def calculate_haversine_km(lat1, lon1, lat2, lon2):
    try:
        lat1, lon1, lat2, lon2 = map(float, [lat1, lon1, lat2, lon2])
    except (ValueError, TypeError):
        return 50.0

    r = 6371.0  # Earth radius in kilometers
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2.0) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2.0) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return r * c


def compute_match_score(lost_item, found_item):
    # 1. Category Score (Weight: 25%)
    if lost_item.category_id == found_item.category_id:
        category_score = 100.0
    else:
        # Check if one category keywords overlap with another
        lost_kw = set(lost_item.category.ai_keywords.lower().split(',')) if lost_item.category.ai_keywords else set()
        found_kw = set(found_item.category.ai_keywords.lower().split(',')) if found_item.category.ai_keywords else set()
        if lost_kw and found_kw and len(lost_kw.intersection(found_kw)) > 0:
            category_score = 40.0
        else:
            category_score = 0.0

    # 2. Color & Brand Score (Weight: 20%)
    brand_score = 0.0
    lost_b = (lost_item.brand or '').strip().lower()
    found_b = (found_item.brand or '').strip().lower()
    if lost_b and found_b:
        if lost_b == found_b:
            brand_score = 100.0
        elif lost_b in found_b or found_b in lost_b:
            brand_score = 80.0
    elif not lost_b and not found_b:
        brand_score = 50.0  # Both unstated
    else:
        # Check if stated brand appears anywhere in description/title
        check_brand = lost_b or found_b
        target_text = f"{found_item.title} {found_item.description}".lower() if lost_b else f"{lost_item.title} {lost_item.description}".lower()
        if check_brand in target_text:
            brand_score = 75.0
        else:
            brand_score = 30.0

    color_score = 0.0
    lost_c = (lost_item.primary_color or '').strip().lower()
    found_c = (found_item.primary_color or '').strip().lower()
    if lost_c and found_c:
        if lost_c == found_c:
            color_score = 100.0
        elif lost_c in found_c or found_c in lost_c:
            color_score = 75.0
    else:
        color_score = 50.0

    color_brand_score = (brand_score + color_score) / 2.0

    # 3. Text Similarity (Weight: 25%)
    lost_tokens = tokenize_text(f"{lost_item.title} {lost_item.description}")
    found_tokens = tokenize_text(f"{found_item.title} {found_item.description}")
    if lost_tokens and found_tokens:
        intersection = lost_tokens.intersection(found_tokens)
        union = lost_tokens.union(found_tokens)
        jaccard = len(intersection) / len(union) if union else 0.0
        # Boost score if specific salient tokens match
        text_score = min(100.0, jaccard * 180.0 + (len(intersection) * 12.0))
    else:
        text_score = 20.0

    # 4. Location Proximity (Weight: 15%)
    location_score = 50.0
    # If both are transit items (JourneyTrace)
    if lost_item.is_transit_item and found_item.is_transit_item:
        transit_matches = 0
        if lost_item.transit_vehicle_name.lower().strip() == found_item.transit_vehicle_name.lower().strip():
            transit_matches += 2
        if lost_item.transit_route.lower().strip() == found_item.transit_route.lower().strip():
            transit_matches += 2
        if lost_item.transit_boarding_point.lower().strip() == found_item.transit_boarding_point.lower().strip():
            transit_matches += 1
        location_score = min(100.0, 40.0 + transit_matches * 15.0)
    else:
        km = calculate_haversine_km(lost_item.latitude, lost_item.longitude, found_item.latitude, found_item.longitude)
        if km <= 0.2:
            location_score = 100.0
        elif km <= 1.0:
            location_score = 90.0
        elif km <= 3.0:
            location_score = 75.0
        elif km <= 10.0:
            location_score = 55.0
        elif km <= 25.0:
            location_score = 35.0
        else:
            location_score = 15.0

    # 5. Time Proximity (Weight: 15%)
    day_diff = abs((found_item.incident_date - lost_item.incident_date).days)
    if day_diff == 0:
        time_score = 100.0
    elif day_diff <= 2:
        time_score = 90.0
    elif day_diff <= 7:
        time_score = 75.0
    elif day_diff <= 20:
        time_score = 50.0
    else:
        time_score = max(10.0, 100.0 - (day_diff * 2.0))

    # Total Weighted Score
    # Strict gating: if categories completely don't match, cap max total
    total_score = (
        0.25 * category_score +
        0.20 * color_brand_score +
        0.25 * text_score +
        0.15 * location_score +
        0.15 * time_score
    )

    if category_score == 0:
        total_score = min(35.0, total_score)

    total_score = round(min(100.0, max(0.0, total_score)), 1)

    return {
        'total': total_score,
        'category': round(category_score, 1),
        'color_brand': round(color_brand_score, 1),
        'text': round(text_score, 1),
        'location': round(location_score, 1),
        'time': round(time_score, 1),
    }


def run_ai_matching_for_item(target_item):
    """
    Triggered when a new report is created or updated.
    If target_item is 'lost', compares against all open 'found' items.
    If target_item is 'found', compares against all open 'lost' items.
    """
    from items.models import ItemReport

    if target_item.report_type == 'lost':
        candidates = ItemReport.objects.filter(
            report_type='found',
            status__in=['open', 'potential_match']
        ).exclude(user=target_item.user)
    else:
        candidates = ItemReport.objects.filter(
            report_type='lost',
            status__in=['open', 'potential_match']
        ).exclude(user=target_item.user)

    matches_found = []

    for candidate in candidates:
        lost = target_item if target_item.report_type == 'lost' else candidate
        found = candidate if target_item.report_type == 'lost' else target_item

        scores = compute_match_score(lost, found)

        if scores['total'] >= 35.0:
            match_rec, created = MatchRecord.objects.update_or_create(
                lost_item=lost,
                found_item=found,
                defaults={
                    'similarity_score': scores['total'],
                    'category_score': scores['category'],
                    'color_brand_score': scores['color_brand'],
                    'text_score': scores['text'],
                    'location_score': scores['location'],
                    'time_score': scores['time'],
                }
            )

            # Update statuses if high confidence
            if scores['total'] >= 50.0:
                if lost.status == 'open':
                    lost.status = 'potential_match'
                    lost.save(update_fields=['status'])
                if found.status == 'open':
                    found.status = 'potential_match'
                    found.save(update_fields=['status'])

                # Create Automatic Notification for Lost Item Owner
                MatchNotification.objects.get_or_create(
                    recipient=lost.user,
                    match=match_rec,
                    defaults={
                        'title': f"Potential AI Match Found ({scores['total']}%)!",
                        'message': f"A found item '{found.title}' matches your lost report '{lost.title}'. Check similarity and submit verification."
                    }
                )

                # Create Notification for Finder
                MatchNotification.objects.get_or_create(
                    recipient=found.user,
                    match=match_rec,
                    defaults={
                        'title': f"AI Match Candidate ({scores['total']}%)",
                        'message': f"Your found item '{found.title}' matches an open report '{lost.title}'."
                    }
                )

            matches_found.append((match_rec, scores['total']))

    return matches_found
