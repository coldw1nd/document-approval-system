from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from documents.models import Document


def index(request: HttpRequest) -> HttpResponse:
    documents = Document.objects.select_related(
        "application", "application__applicant", "application__status"
    ).order_by("-uploaded_at", "-pk")
    return render(request, "documents/index.html", {"documents": documents})
