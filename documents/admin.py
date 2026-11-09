from django.contrib import admin

from documents.models import Document


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "application", "uploaded_at")
    list_display_links = ("id", "name")
    list_filter = ("uploaded_at",)
    search_fields = ("name", "description", "application__title")
    ordering = ("-uploaded_at", "-id")
    list_per_page = 25
    list_select_related = ("application",)
