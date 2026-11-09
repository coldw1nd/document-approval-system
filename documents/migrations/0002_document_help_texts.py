from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("documents", "0001_initial")]
    operations = [
        migrations.AlterField(
            model_name="document",
            name="name",
            field=models.CharField(
                help_text="Имя приложенного к заявлению документа.",
                max_length=255,
                verbose_name="Имя документа",
            ),
        ),
        migrations.AlterField(
            model_name="document",
            name="description",
            field=models.TextField(
                blank=True,
                help_text="Краткое описание содержимого документа.",
                verbose_name="Описание",
            ),
        ),
    ]
