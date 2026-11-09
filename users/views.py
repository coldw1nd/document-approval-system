from django.db.models import Count
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render

from applications.models import Application
from users.models import User


def index(request: HttpRequest) -> HttpResponse:
    user_rows = User.objects.annotate(
        application_count=Count("applications", distinct=True)
    ).order_by("full_name")
    return render(request, "users/index.html", {"user_rows": user_rows})


def detail(request: HttpRequest, user_id: int) -> HttpResponse:
    user = get_object_or_404(User, pk=user_id)
    applications = Application.objects.with_related().filter(
        applicant=user
    ).order_by("-created_at", "-pk")
    return render(
        request,
        "users/detail.html",
        {"user": user, "applications": applications},
    )
