from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("books", "0003_drop_library_tables"),
    ]

    operations = [
        migrations.AddField(
            model_name="book",
            name="applied_for_sale",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="book",
            name="copies_for_sale",
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="book",
            name="sale_price",
            field=models.DecimalField(
                blank=True, decimal_places=2, max_digits=8, null=True
            ),
        ),
    ]

