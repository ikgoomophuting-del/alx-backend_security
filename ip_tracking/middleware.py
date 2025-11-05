from django.http import HttpResponseForbidden
from django.core.cache import cache
from .models import RequestLog, BlockedIP
import logging
import requests

logger = logging.getLogger(__name__)

class RequestLoggingMiddleware:
    """
    Middleware to log requests and block blacklisted IPs,
    with geolocation enrichment and caching.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip_address = self.get_client_ip(request)
        path = request.path

        # Block if IP is blacklisted
        if BlockedIP.objects.filter(ip_address=ip_address).exists():
            logger.warning(f"Blocked request from {ip_address}")
            return HttpResponseForbidden("Access denied: Your IP is blocked.")

        # Get cached geolocation or fetch it
        geo_data = cache.get(ip_address)
        if not geo_data:
            geo_data = self.get_geolocation(ip_address)
            cache.set(ip_address, geo_data, 60 * 60 * 24)  # cache 24h

        country = geo_data.get("country")
        city = geo_data.get("city")

        # Log to DB
        RequestLog.objects.create(
            ip_address=ip_address,
            path=path,
            country=country,
            city=city
        )

        logger.info(f"Request from {ip_address} ({city}, {country}) to {path}")
        return self.get_response(request)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def get_geolocation(self, ip):
        """
        Fetch geolocation info using ipapi.co or ipinfo.io (no API key needed).
        """
        try:
            response = requests.get(f"https://ipapi.co/{ip}/json/", timeout=3)
            data = response.json()
            return {
                "country": data.get("country_name"),
                "city": data.get("city"),
            }
        except Exception as e:
            logger.error(f"Geolocation lookup failed for {ip}: {e}")
            return {"country": None, "city": None}
