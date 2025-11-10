from django.utils import timezone
from ipware import get_client_ip
from .models import RequestLog


class RequestLoggingMiddleware:
    """
    Middleware to log IP, path, and timestamp of each incoming request.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip, _ = get_client_ip(request)
        if ip:
            RequestLog.objects.create(
                ip_address=ip,
                path=request.path,
                timestamp=timezone.now()
            )

        response = self.get_response(request)
        return response
