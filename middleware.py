from django.utils import timezone
from django.http import HttpResponseForbidden
from ipware import get_client_ip
from .models import RequestLog, BlockedIP


class RequestLoggingMiddleware:
    """
    Middleware to log requests and block blacklisted IPs.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip, _ = get_client_ip(request)

        if ip and BlockedIP.objects.filter(ip_address=ip).exists():
            return HttpResponseForbidden("Access denied: your IP has been blocked.")

        if ip:
            RequestLog.objects.create(
                ip_address=ip,
                path=request.path,
                timestamp=timezone.now()
            )

        return self.get_response(request)
