from django.db import models


class User(models.Model):
    full_name = models.CharField(
        max_length=200,
        verbose_name="ФИО",
        help_text="Укажите фамилию, имя и отчество пользователя.",
    )
    email = models.EmailField(
        unique=True,
        verbose_name="Электронная почта",
        help_text="Адрес используется для связи с заявителем.",
    )

    class Meta:
        ordering = ["full_name"]
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self) -> str:
        return self.full_name
