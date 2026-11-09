import pytest
from django.test import Client

from applications.models import Application, Comment, Status
from documents.models import Document
from users.models import User


@pytest.fixture
def seeded_records(db):
    user, _ = User.objects.get_or_create(
        email="test.applicant@example.test",
        defaults={"full_name": "Тестовый заявитель"},
    )
    status, _ = Status.objects.get_or_create(
        name="Тестовый статус",
        defaults={"is_final": False},
    )
    application, _ = Application.objects.get_or_create(
        pk=9001,
        defaults={
            "title": "Тестовое заявление",
            "description": "Проверка ORM и связей.",
            "applicant": user,
            "status": status,
            "created_at": "2026-10-01",
        },
    )
    Document.objects.get_or_create(
        application=application,
        name="test-document.pdf",
        defaults={
            "description": "Тестовый документ",
            "uploaded_at": "2026-10-01",
        },
    )
    Comment.objects.get_or_create(
        application=application,
        author=user,
        text="Тестовый комментарий",
        defaults={"created_at": "2026-10-02"},
    )
    return application


def test_main_routes_return_successful_responses(seeded_records) -> None:
    client = Client()
    paths = [
        "/",
        "/applications/",
        f"/applications/{seeded_records.pk}/",
        "/users/",
        f"/users/{seeded_records.applicant_id}/",
        "/documents/",
        "/applications/statistics/",
    ]
    for path in paths:
        response = client.get(path)
        assert response.status_code == 200, path


@pytest.mark.django_db
def test_unknown_application_returns_404() -> None:
    response = Client().get("/applications/999999/")
    assert response.status_code == 404


def test_application_search_returns_matching_record(seeded_records) -> None:
    response = Client().get("/applications/", {"q": "Тестовое"})
    assert response.status_code == 200
    assert "Тестовое заявление" in response.content.decode("utf-8")


def test_application_relations_are_available(seeded_records) -> None:
    application = Application.objects.with_related().get(pk=seeded_records.pk)
    assert application.applicant.full_name == "Тестовый заявитель"
    assert application.status.name == "Тестовый статус"
    assert application.documents.count() == 1
    assert application.comments.first().author_id == application.applicant_id
