from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_user_full_name_user_contact_number"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="full_name",
        ),
    ]

