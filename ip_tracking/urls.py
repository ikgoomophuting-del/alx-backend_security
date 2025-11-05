from django.urls import path
from .views import sensitive_view

urlpatterns = [
    path("test/", sensitive_view, name="test_view"),
]
