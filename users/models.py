from django.db import models


class User(models.Model):
    full_name = models.CharField(max_length=200, verbose_name="ФИО")
    email = models.EmailField(unique=True, verbose_name="Электронная почта")

    class Meta:
        ordering = ["full_name"]
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self) -> str:
        return self.full_name
