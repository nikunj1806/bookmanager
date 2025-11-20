from django.db import migrations


DROP_LIBRARY_TABLES = """
DROP TABLE IF EXISTS "library_membershippayment" CASCADE;
DROP TABLE IF EXISTS "library_borrow" CASCADE;
DROP TABLE IF EXISTS "library_book" CASCADE;
"""


class Migration(migrations.Migration):

    dependencies = [
        ("books", "0002_book_cover_image_alter_book_available_copies_and_more"),
    ]

    operations = [
        migrations.RunSQL(
            sql=DROP_LIBRARY_TABLES,
            reverse_sql=migrations.RunSQL.noop,
        ),
    ]

