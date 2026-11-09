from django.db import models


class Document(models.Model):
    application = models.ForeignKey(
        "applications.Application",
        on_delete=models.CASCADE,
        related_name="documents",
        verbose_name="Заявление",
    )
    name = models.CharField(max_length=255, verbose_name="Имя документа")
    description = models.TextField(blank=True, verbose_name="Описание")
    uploaded_at = models.DateField(verbose_name="Дата загрузки")

    class Meta:
        ordering = ["-uploaded_at", "-pk"]
        verbose_name = "Документ"
        verbose_name_plural = "Документы"

    def __str__(self) -> str:
        return self.name
