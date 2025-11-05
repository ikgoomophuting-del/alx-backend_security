from .models import RequestLog
import logging

logger = logging.getLogger(__name__)

class RequestLoggingMiddleware:
    """
    Middleware to log the IP address, timestamp, and path
    of every incoming request.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip_address = self.get_client_ip(request)
        path = request.path

        # Log to database
        RequestLog.objects.create(ip_address=ip_address, path=path)

        # Log to console/file
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
