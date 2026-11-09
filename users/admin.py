from django.contrib import admin

from applications.models import Application
from users.models import User


class ApplicationInline(admin.TabularInline):
    model = Application
    extra = 0
    fields = ("title", "status", "created_at")
    readonly_fields = ("title", "status", "created_at")
    show_change_link = True
    can_delete = False


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "full_name", "email")
    list_display_links = ("id", "full_name")
    search_fields = ("full_name", "email")
    ordering = ("full_name",)
    list_per_page = 25
    inlines = (ApplicationInline,)
