from django.contrib import admin, messages

from applications.models import Application, Comment, Status
from documents.models import Document


class DocumentInline(admin.TabularInline):
    model = Document
    extra = 0
    fields = ("name", "description", "uploaded_at")


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    fields = ("author", "text", "created_at")


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "code", "is_final")
    list_display_links = ("id", "name")
    list_filter = ("is_final",)
    search_fields = ("name", "code")
    ordering = ("id",)
    list_per_page = 20


@admin.action(description="Перевести выбранные заявления на рассмотрение")
def mark_in_review(modeladmin, request, queryset):
    review_status = Status.objects.get(code=Status.Code.REVIEW)
    updated = queryset.update(status=review_status)
    modeladmin.message_user(
        request,
        f"Обновлено заявлений: {updated}",
        messages.SUCCESS,
    )


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = (
        "id", "title", "applicant", "status", "created_at",
        "description_length"
    )
    list_display_links = ("id", "title")
    list_editable = ("status",)
    list_filter = ("status", "created_at", "status__is_final")
    search_fields = (
        "title", "description", "applicant__full_name",
        "applicant__email"
    )
    ordering = ("-created_at", "-id")
    list_per_page = 20
    list_select_related = ("applicant", "status")
    readonly_fields = ("slug", "description_length")
    fieldsets = (
        (
            "Заявление",
            {"fields": ("title", "slug", "description", "description_length")},
        ),
        (
            "Заявитель и обработка",
            {"fields": ("applicant", "status", "created_at")},
        ),
    )
    inlines = (DocumentInline, CommentInline)
    actions = (mark_in_review,)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "application", "author", "created_at")
    list_display_links = ("id", "application")
    list_filter = ("created_at",)
    search_fields = ("text", "application__title", "author__full_name")
    ordering = ("-created_at", "-id")
    list_per_page = 25
    list_select_related = ("application", "author")
