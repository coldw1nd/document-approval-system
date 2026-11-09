from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("users", "0001_initial")]
    operations = [
        migrations.AlterField(
            model_name="user",
            name="full_name",
            field=models.CharField(
                help_text="Укажите фамилию, имя и отчество пользователя.",
                max_length=200,
                verbose_name="ФИО",
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="email",
            field=models.EmailField(
                help_text="Адрес используется для связи с заявителем.",
                max_length=254,
                unique=True,
                verbose_name="Электронная почта",
            ),
        ),
    ]
