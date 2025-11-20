from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("stores", "0002_update_inventory_fields"),
        ("loans", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="loan",
            name="store",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="loans",
                to="stores.store",
            ),
        ),
        migrations.AddField(
            model_name="loan",
            name="store_inventory",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="loans",
                to="stores.storeinventory",
            ),
        ),
    ]

