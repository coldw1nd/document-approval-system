from django.db.models import Count
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from applications.models import Application, Status
from users.models import User


def index(request: HttpRequest) -> HttpResponse:
    applications = Application.objects.with_related()
    context = {
        "users_count": User.objects.count(),
        "statuses_count": Status.objects.count(),
        "applications": applications.order_by("-created_at", "-pk")[:3],
        "applications_count": Application.objects.aggregate(
            total=Count("pk")
        )["total"],
    }
    return render(request, "homepage/index.html", context)


def page_not_found(request: HttpRequest, exception: Exception) -> HttpResponse:
    return render(request, "404.html", status=404)
