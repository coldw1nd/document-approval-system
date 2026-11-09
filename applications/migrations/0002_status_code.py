from django.db import migrations, models


def fill_status_codes(apps, schema_editor):
    Status = apps.get_model("applications", "Status")
    mapping = {
        "Черновик": "draft",
        "На рассмотрении": "review",
        "Одобрено": "approved",
        "Отклонено": "rejected",
    }
    for status in Status.objects.all():
        status.code = mapping.get(status.name, f"status-{status.pk}")
        status.save(update_fields=["code"])


class Migration(migrations.Migration):
    dependencies = [("applications", "0001_initial")]
    operations = [
        migrations.AddField(
            model_name="status",
            name="code",
            field=models.CharField(
                blank=True,
                default="",
                max_length=20,
                verbose_name="Код статуса",
            ),
            preserve_default=False,
        ),
        migrations.RunPython(fill_status_codes, migrations.RunPython.noop),
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
                max_length=20,
                unique=True,
                verbose_name="Код статуса",
            ),
        ),
    ]
