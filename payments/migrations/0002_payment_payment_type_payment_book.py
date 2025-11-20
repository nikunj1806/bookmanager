from django.db import migrations, models
import django.db.models.deletion


def set_default_payment_type(apps, schema_editor):
    Payment = apps.get_model("payments", "Payment")
    Payment.objects.filter(payment_type__isnull=True).update(payment_type="membership")


class Migration(migrations.Migration):

    dependencies = [
        ("books", "0002_book_cover_image_alter_book_available_copies_and_more"),
        ("loans", "0001_initial"),
        ("payments", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="payment",
            name="payment_type",
            field=models.CharField(
                default="membership",
                choices=[("membership", "Membership"), ("buy", "Book Purchase")],
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name="payment",
            name="book",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="purchases",
                to="books.book",
            ),
        ),
        migrations.RunPython(set_default_payment_type, migrations.RunPython.noop),
    ]

