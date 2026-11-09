from django.db import models
from django.db.models import Q


class Status(models.Model):
    name = models.CharField(
        max_length=100, unique=True, verbose_name="Название"
    )
    is_final = models.BooleanField(
        default=False, verbose_name="Конечный статус"
    )

    class Meta:
        ordering = ["id"]
        verbose_name = "Статус заявления"
        verbose_name_plural = "Статусы заявлений"

    def __str__(self) -> str:
        return self.name


class ApplicationQuerySet(models.QuerySet):
    def active(self):
        return self.filter(status__is_final=False)

    def finalized(self):
        return self.filter(status__is_final=True)

    def exclude_finalized(self):
        return self.exclude(status__is_final=True)

    def search(self, term: str):
        if not term:
            return self
        return self.filter(
            Q(title__icontains=term)
            | Q(description__icontains=term)
            | Q(applicant__full_name__icontains=term)
            | Q(applicant__email__icontains=term)
        )

    def with_related(self):
        return self.select_related("applicant", "status").prefetch_related(
            "documents", "comments__author"
        )


class ApplicationManager(models.Manager.from_queryset(ApplicationQuerySet)):
    pass


class Application(models.Model):
    title = models.CharField(max_length=250, verbose_name="Название заявления")
    description = models.TextField(blank=True, verbose_name="Описание")
    applicant = models.ForeignKey(
        "users.User",
        on_delete=models.PROTECT,
        related_name="applications",
        verbose_name="Заявитель",
    )
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        related_name="applications",
        verbose_name="Статус",
    )
    created_at = models.DateField(verbose_name="Дата создания")
    objects = ApplicationManager()

    class Meta:
        ordering = ["-created_at", "-pk"]
        verbose_name = "Заявление"
        verbose_name_plural = "Заявления"

    def __str__(self) -> str:
        return f"Заявление №{self.pk}: {self.title}"


class Comment(models.Model):
    application = models.ForeignKey(
        Application,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Заявление",
    )
    author = models.ForeignKey(
        "users.User",
        on_delete=models.PROTECT,
        related_name="comments",
        verbose_name="Автор",
    )
    text = models.TextField(verbose_name="Текст комментария")
    created_at = models.DateField(verbose_name="Дата создания")

    class Meta:
        ordering = ["created_at", "pk"]
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    def __str__(self) -> str:
        return f"{self.author}: {self.text[:60]}"
