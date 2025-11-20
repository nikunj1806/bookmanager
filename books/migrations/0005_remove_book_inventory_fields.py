from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("books", "0004_book_sale_fields"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="book",
            name="applied_for_sale",
        ),
        migrations.RemoveField(
            model_name="book",
            name="available_copies",
        ),
        migrations.RemoveField(
            model_name="book",
            name="copies_for_sale",
        ),
        migrations.RemoveField(
            model_name="book",
            name="sale_price",
        ),
        migrations.RemoveField(
            model_name="book",
            name="total_copies",
        ),
    ]

