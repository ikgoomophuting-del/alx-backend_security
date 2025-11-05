from django.http import HttpResponseForbidden
from .models import RequestLog, BlockedIP
import logging

logger = logging.getLogger(__name__)

class RequestLoggingMiddleware:
    """
    Middleware that logs incoming requests and blocks blacklisted IPs.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip_address = self.get_client_ip(request)
        path = request.path

        # Check if IP is blocked
        if BlockedIP.objects.filter(ip_address=ip_address).exists():
            logger.warning(f"Blocked request from IP: {ip_address}")
            return HttpResponseForbidden("Access denied: Your IP is blocked.")

        # Log request to DB
        RequestLog.objects.create(ip_address=ip_address, path=path)

        logger.info(f"Request from IP: {ip_address} to path: {path}")
        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        """Extract client IP address from request headers."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
