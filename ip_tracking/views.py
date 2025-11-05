from django.http import JsonResponse
from ratelimit.decorators import ratelimit

# Anonymous: 5 req/min, Authenticated: 10 req/min
@ratelimit(key='ip', rate='5/m', block=True)
@ratelimit(key='user', rate='10/m', block=True)
def sensitive_view(request):
    return JsonResponse({"message": "Access granted!"})
