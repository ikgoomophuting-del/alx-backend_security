from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import RequestLog, SuspiciousIP

@shared_task
def detect_suspicious_activity():
    """
    Flag IPs that exceed 100 requests/hour or access sensitive paths.
    """
    one_hour_ago = timezone.now() - timedelta(hours=1)
    recent_logs = RequestLog.objects.filter(timestamp__gte=one_hour_ago)

    ip_counts = {}
    for log in recent_logs:
        ip_counts[log.ip_address] = ip_counts.get(log.ip_address, 0) + 1

        if "/admin" in log.path or "/login" in log.path:
            SuspiciousIP.objects.get_or_create(
                ip_address=log.ip_address,
                defaults={"reason": "Accessed sensitive endpoint"}
            )

    for ip, count in ip_counts.items():
        if count > 100:
            SuspiciousIP.objects.get_or_create(
                ip_address=ip,
                defaults={"reason": f"High request volume ({count}/hour)"}
            )
