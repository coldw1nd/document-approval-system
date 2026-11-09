from applications.models import Application


def application_context(request):
    return {
        "site_name": "Сервис электронных заявлений",
        "applications_count": Application.objects.count(),
    }
