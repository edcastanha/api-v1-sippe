from django.shortcuts import render
from django.contrib.auth.decorators import login_required # Login required to access private pagas
from django.views.decorators.cache import cache_control # Prevent back button (destroy the last section)

#Utils function Django
from django.db.models import Count
from django.db.models.functions import TruncDate
from django.db.models import Sum
from django.http import JsonResponse


# ======== Models ========
from core.cameras.models import Cameras, Processamentos, Faces

# Frontend
def frontend(request):
    return render(request, "frontend.html")


# Backend
@login_required(login_url="login")
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def backend(request):
    return render(request, "app/backend.html")


# ============ JSON ============
