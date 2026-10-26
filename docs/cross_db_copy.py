from django.db import connections

def sql_native_table_copy():
    # 1. Get the absolute file path of your destination SQLite database
    # Django stores the file path in the 'NAME' setting field
    destination_db_path = connections['analytics'].settings_dict['NAME']

    table_name = "django_migrations"

    print(f"Attaching {destination_db_path} and copying '{table_name}'...")

    # 2. Execute native SQLite commands on the 'default' connection
    with connections['default'].cursor() as cursor:
        # Attach the destination database file to the current connection under the alias 'dest'
        cursor.execute("ATTACH DATABASE %s AS dest;", [str(destination_db_path)])

        try:
            # Recreate the exact table structure if it doesn't exist yet
            cursor.execute(f"CREATE TABLE IF NOT EXISTS dest.{table_name} AS SELECT * FROM main.{table_name} WHERE 1=0;")

            # Optional: Clear out destination rows if you want an exact mirror rewrite
            cursor.execute(f"DELETE FROM dest.{table_name};")

            # The ultra-fast, pure-SQL copy mechanism
            cursor.execute(f"INSERT INTO dest.{table_name} SELECT * FROM main.{table_name};")

            print(f"Table '{table_name}' successfully copied entirely inside SQLite!")

        finally:
            # Always detach the database when finished to free the file lock
            cursor.execute("DETACH DATABASE dest;")


# Run the function
sql_native_table_copy()
