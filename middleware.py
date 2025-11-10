import requests
from django.core.cache import cache
from django.utils import timezone
from django.http import HttpResponseForbidden
from ipware import get_client_ip
from .models import RequestLog, BlockedIP

GEO_API_URL = "https://ipinfo.io/{ip}/json"
CACHE_TIMEOUT = 60 * 60 * 24  # 24 hours


class RequestLoggingMiddleware:
    """
    Logs IP details and uses geolocation to enrich data.
    Blocks blacklisted IPs and caches geolocation results.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def get_geolocation(self, ip):
        cached_data = cache.get(ip)
        if cached_data:
            return cached_data

        try:
            response = requests.get(GEO_API_URL.format(ip=ip), timeout=3)
            if response.status_code == 200:
                data = response.json()
                country = data.get("country", "")
                city = data.get("city", "")
                cache.set(ip, {"country": country, "city": city}, CACHE_TIMEOUT)
                return {"country": country, "city": city}
        except requests.RequestException:
            pass
        return {"country": "", "city": ""}

    def __call__(self, request):
        ip, _ = get_client_ip(request)

        if ip and BlockedIP.objects.filter(ip_address=ip).exists():
            return HttpResponseForbidden("Access denied: your IP has been blocked.")

        country = city = None
        if ip:
            geo = self.get_geolocation(ip)
            country, city = geo["country"], geo["city"]
            RequestLog.objects.create(
                ip_address=ip,
                path=request.path,
                timestamp=timezone.now(),
                country=country,
                city=city
            )

        return self.get_response(request)
