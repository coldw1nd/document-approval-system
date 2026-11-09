from django.db import migrations, models
from django.db.models.functions import Length


class Migration(migrations.Migration):
    dependencies = [("applications", "0004_application_description_length")]
    operations = [
        migrations.AlterField(
            model_name="status",
            name="name",
            field=models.CharField(
                help_text="Название этапа обработки электронного заявления.",
                max_length=100,
                unique=True,
                verbose_name="Название",
            ),
        ),
        migrations.AlterField(
            model_name="status",
            name="code",
            field=models.CharField(
                choices=[
                    ("draft", "Черновик"),
                    ("review", "На рассмотрении"),
                    ("approved", "Одобрено"),
                    ("rejected", "Отклонено"),
                ],
                help_text="Стабильный код для проверок и ORM-фильтрации.",
                max_length=20,
                unique=True,
                verbose_name="Код статуса",
            ),
        ),
        migrations.AlterField(
            model_name="application",
            name="title",
            field=models.CharField(
                help_text="Кратко сформулируйте предмет обращения.",
                max_length=250,
                verbose_name="Название заявления",
            ),
        ),
        migrations.AlterField(
            model_name="application",
            name="description",
            field=models.TextField(
                blank=True,
                help_text="Подробности заявления и необходимые пояснения.",
                verbose_name="Описание",
            ),
        ),
        migrations.AlterField(
            model_name="application",
            name="description_length",
            field=models.GeneratedField(
                db_persist=True,
                expression=Length("description"),
                help_text="Вычисляется базой данных по содержимому описания.",
                output_field=models.PositiveIntegerField(),
                verbose_name="Длина описания",
            ),
        ),
    ]
