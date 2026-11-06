import hashlib
from datetime import timedelta
from django.utils import timezone


def compute_image_hash(image_file):
    if not image_file:
        return ""
    hasher = hashlib.sha256()
    image_file.seek(0)
    for chunk in image_file.chunks():
        hasher.update(chunk)
    image_file.seek(0)
    return hasher.hexdigest()


def evaluate_report_fraud_risk(item_report):
    """
    Evaluates rule-based and behavioral fraud indicators for newly filed reports.
    Returns: (is_suspicious: bool, risk_score: int, reasons: list)
    """
    from items.models import ItemReport, ClaimRequest

    reasons = []
    risk_score = 0

    # 1. Duplicate Image Check
    if item_report.image_hash:
        duplicate_images = ItemReport.objects.filter(
            image_hash=item_report.image_hash
        ).exclude(id=item_report.id)

        if duplicate_images.exists():
            dup_count = duplicate_images.count()
            risk_score += 45
            reasons.append(f"Identical image detected across {dup_count} other report(s) (potential photo recycling).")

    # 2. Report velocity check (flooding)
    one_hour_ago = timezone.now() - timedelta(hours=1)
    recent_user_reports = ItemReport.objects.filter(
        user=item_report.user,
        created_at__gte=one_hour_ago
    ).exclude(id=item_report.id).count()

    if recent_user_reports >= 4:
        risk_score += 35
        reasons.append(f"High posting velocity: {recent_user_reports} reports filed in the past hour.")

    # 3. User reputation factor
    if item_report.user.reputation_score < 50:
        risk_score += 25
        reasons.append(f"Low account trust score ({item_report.user.reputation_score}/100).")

    # 4. Empty or suspicious placeholder description
    desc_words = len(item_report.description.split())
    if desc_words < 4:
        risk_score += 15
        reasons.append("Very short / vague description provided.")

    is_suspicious = risk_score >= 40
    return is_suspicious, min(100, risk_score), reasons
