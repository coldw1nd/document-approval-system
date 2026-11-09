from django.conf import settings
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(("homepage.urls", "homepage"), namespace="homepage")),
    path(
        "applications/",
        include(
            ("applications.urls", "applications"),
            namespace="applications",
        ),
    ),
    path("users/", include(("users.urls", "users"), namespace="users")),
    path(
        "documents/",
        include(("documents.urls", "documents"), namespace="documents"),
    ),
]

if settings.DEBUG and "debug_toolbar" in settings.INSTALLED_APPS:
    urlpatterns += [path("__debug__/", include("debug_toolbar.urls"))]

handler404 = "homepage.views.page_not_found"
