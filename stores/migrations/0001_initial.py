from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("books", "0004_book_sale_fields"),
    ]

    operations = [
        migrations.CreateModel(
            name="Store",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=255, unique=True)),
                ("location", models.CharField(max_length=255)),
                ("manager", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="managed_stores", to=settings.AUTH_USER_MODEL)),
            ],
            options={
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="StoreInventory",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("borrow_copies", models.PositiveIntegerField(default=0)),
                ("sale_copies", models.PositiveIntegerField(default=0)),
                ("sale_price", models.DecimalField(blank=True, decimal_places=2, help_text="Price per copy when sale copies are available.", max_digits=8, null=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("book", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="store_inventories", to="books.book")),
                ("store", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="inventory_items", to="stores.store")),
            ],
            options={
                "verbose_name_plural": "store inventory",
            },
        ),
        migrations.CreateModel(
            name="StoreStaff",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("role", models.CharField(choices=[("admin", "Admin"), ("staff", "Staff")], default="staff", max_length=20)),
                ("assigned_at", models.DateTimeField(auto_now_add=True)),
                ("store", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="store_staff", to="stores.store")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="store_memberships", to=settings.AUTH_USER_MODEL)),
            ],
            options={
                "verbose_name_plural": "store staff",
            },
        ),
        migrations.AddField(
            model_name="store",
            name="staff",
            field=models.ManyToManyField(blank=True, related_name="stores", through="stores.StoreStaff", to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name="storeinventory",
            unique_together={("store", "book")},
        ),
        migrations.AlterUniqueTogether(
            name="storestaff",
            unique_together={("store", "user")},
        ),
    ]

