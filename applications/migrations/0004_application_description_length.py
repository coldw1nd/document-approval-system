from django.db import migrations, models
from django.db.models.functions import Length


class Migration(migrations.Migration):
    dependencies = [("applications", "0003_application_slug")]
    operations = [
        migrations.AddField(
            model_name="application",
            name="description_length",
            field=models.GeneratedField(
                db_persist=True,
                expression=Length("description"),
                output_field=models.PositiveIntegerField(),
                verbose_name="Длина описания",
            ),
        ),
    ]
