from django.http import JsonResponse

def sensitive_view(request):
    return JsonResponse({"message": "Access granted!"})
