from django.db import models
from django.db.models import Q
from django.db.models.functions import Length
from django.urls import reverse
from django.utils.text import slugify


class Status(models.Model):
    class Code(models.TextChoices):
        DRAFT = "draft", "Черновик"
        REVIEW = "review", "На рассмотрении"
        APPROVED = "approved", "Одобрено"
        REJECTED = "rejected", "Отклонено"

    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Название",
        help_text="Название этапа обработки электронного заявления.",
    )
    is_final = models.BooleanField(
        default=False, verbose_name="Конечный статус"
    )
    code = models.CharField(
        max_length=20,
        choices=Code.choices,
        unique=True,
        verbose_name="Код статуса",
        help_text="Стабильный код для проверок и ORM-фильтрации.",
    )

    class Meta:
        ordering = ["id"]
        verbose_name = "Статус заявления"
        verbose_name_plural = "Статусы заявлений"

    def __str__(self) -> str:
        return self.name


class ApplicationQuerySet(models.QuerySet):
    def active(self):
        return self.filter(
            status__code__in=[Status.Code.DRAFT, Status.Code.REVIEW]
        )

    def finalized(self):
        return self.filter(
            status__code__in=[Status.Code.APPROVED, Status.Code.REJECTED]
        )

    def exclude_finalized(self):
        return self.exclude(
            status__code__in=[Status.Code.APPROVED, Status.Code.REJECTED]
        )

    def draft(self):
        return self.filter(status__code=Status.Code.DRAFT)

    def in_review(self):
        return self.filter(status__code=Status.Code.REVIEW)

    def search(self, term: str):
        if not term:
            return self
        return self.filter(
            Q(title__icontains=term)
            | Q(description__icontains=term)
            | Q(applicant__full_name__icontains=term)
            | Q(applicant__email__icontains=term)
            | Q(comments__text__icontains=term)
        ).distinct()

    def with_related(self):
        return (
            self.select_related("applicant", "status")
            .prefetch_related("documents", "comments__author")
            .annotate(
                documents_count=models.Count("documents", distinct=True),
                comments_count=models.Count("comments", distinct=True),
            )
        )


class ApplicationManager(models.Manager.from_queryset(ApplicationQuerySet)):
    pass


class Application(models.Model):
    title = models.CharField(
        max_length=250,
        verbose_name="Название заявления",
        help_text="Кратко сформулируйте предмет обращения.",
    )
    description = models.TextField(
        blank=True,
        verbose_name="Описание",
        help_text="Подробности заявления и необходимые пояснения.",
    )
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
    slug = models.SlugField(
        max_length=255, unique=True, blank=True, verbose_name="Адрес"
    )
    description_length = models.GeneratedField(
        expression=Length("description"),
        output_field=models.PositiveIntegerField(),
        db_persist=True,
        verbose_name="Длина описания",
        help_text="Вычисляется базой данных по содержимому описания.",
    )
    objects = ApplicationManager()

    class Meta:
        ordering = ["-created_at", "-pk"]
        verbose_name = "Заявление"
        verbose_name_plural = "Заявления"

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title) or "application"
            candidate = base_slug
            suffix = 2
            while (
                Application.objects.filter(slug=candidate)
                .exclude(pk=self.pk)
                .exists()
            ):
                candidate = f"{base_slug}-{suffix}"
                suffix += 1
            self.slug = candidate
        super().save(*args, **kwargs)

    def get_absolute_url(self) -> str:
        return reverse("applications:slug_detail", kwargs={"slug": self.slug})

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
