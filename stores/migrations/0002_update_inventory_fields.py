from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("stores", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="storeinventory",
            name="borrow_copies",
        ),
        migrations.RemoveField(
            model_name="storeinventory",
            name="sale_copies",
        ),
        migrations.AddField(
            model_name="storeinventory",
            name="applied_for_sale",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="storeinventory",
            name="available_copies",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name="storeinventory",
            name="copies_for_sale",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name="storeinventory",
            name="total_copies",
            field=models.PositiveIntegerField(default=0),
        ),
    ]

