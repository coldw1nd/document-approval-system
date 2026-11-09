from django.core.paginator import Paginator
from django.db.models import Count, F, Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render

from applications.models import Application, Status


def index(request: HttpRequest) -> HttpResponse:
    query = request.GET.get("q", "").strip()
    status_id = request.GET.get("status", "").strip()
    sort = request.GET.get("sort", "newest").strip()
    ordering = {
        "newest": "-created_at",
        "oldest": "created_at",
        "title": "title",
        "-title": "-title",
    }.get(sort, "-created_at")
    applications = Application.objects.with_related().all()
    if query:
        applications = applications.search(query)
    if status_id.isdigit():
        applications = applications.filter(status_id=int(status_id))
    applications = applications.annotate(
        documents_count=Count("documents", distinct=True),
        comments_count=Count("comments", distinct=True),
    ).order_by(ordering, "-pk")
    page_obj = Paginator(applications, 5).get_page(request.GET.get("page"))
    return render(
        request,
        "applications/index.html",
        {
            "applications": page_obj,
            "page_obj": page_obj,
            "statuses": Status.objects.order_by("id"),
            "query": query,
            "selected_status": status_id,
            "selected_sort": sort,
        },
    )


def detail(request: HttpRequest, application_id: int) -> HttpResponse:
    application = get_object_or_404(
        Application.objects.with_related(),
        pk=application_id,
    )
    return render(
        request, "applications/detail.html", {"application": application}
    )


def slug_detail(request: HttpRequest, slug: str) -> HttpResponse:
    application = get_object_or_404(
        Application.objects.with_related(),
        slug=slug,
    )
    return render(
        request, "applications/detail.html", {"application": application}
    )


def statistics(request: HttpRequest) -> HttpResponse:
    status_rows = list(
        Status.objects.annotate(
            application_count=Count("applications", distinct=True)
        ).order_by("id")
    )
    totals = Application.objects.aggregate(
        total=Count("pk"),
        active=Count(
            "pk",
            filter=Q(
                status__code__in=[Status.Code.DRAFT, Status.Code.REVIEW]
            ),
        ),
        final=Count(
            "pk",
            filter=Q(
                status__code__in=[Status.Code.APPROVED, Status.Code.REJECTED]
            ),
        ),
    )
    grouped = list(
        Application.objects.values(
            status_name=F("status__name"),
            status_code=F("status__code"),
        )
        .annotate(total=Count("pk"))
        .order_by("status_name")
    )
    return render(
        request,
        "applications/statistics.html",
        {"status_rows": status_rows, "totals": totals, "grouped": grouped},
    )
