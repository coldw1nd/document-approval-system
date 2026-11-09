from django.db import migrations, models
from django.utils.text import slugify


def fill_application_slugs(apps, schema_editor):
    Application = apps.get_model("applications", "Application")
    used = set()
    for application in Application.objects.order_by("pk"):
        base_slug = slugify(application.title) or "application"
        candidate = base_slug
        suffix = 2
        while candidate in used:
            candidate = f"{base_slug}-{suffix}"
            suffix += 1
        application.slug = candidate
        application.save(update_fields=["slug"])
        used.add(candidate)


class Migration(migrations.Migration):
    dependencies = [("applications", "0002_status_code")]
    operations = [
        migrations.AddField(
            model_name="application",
            name="slug",
            field=models.SlugField(
                blank=True,
                default="",
                max_length=255,
                verbose_name="Адрес",
            ),
            preserve_default=False,
        ),
        migrations.RunPython(
            fill_application_slugs,
            migrations.RunPython.noop,
        ),
        migrations.AlterField(
            model_name="application",
            name="slug",
            field=models.SlugField(
                blank=True,
                max_length=255,
                unique=True,
                verbose_name="Адрес",
            ),
        ),
    ]
