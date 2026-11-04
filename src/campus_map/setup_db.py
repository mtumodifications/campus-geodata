import psycopg

from config import DB_CONFIG, DATABASE_DIR


def execute_sql_file(cursor, file_path):
    """Read and execute an SQL file."""
    print(f"Executing: {file_path.name}")

    with open(file_path, "r", encoding="utf-8") as sql_file:
        sql = sql_file.read()

    cursor.execute(sql)


def setup_database():
    connection = None

    try:
        print("Connecting to database...")

        connection = psycopg.connect(**DB_CONFIG)
        cursor = connection.cursor()

        print("Connected successfully!")

        # Execute SQL files in the correct order
        sql_files = [
            DATABASE_DIR / "extensions/postgis.sql",
            DATABASE_DIR / "queries/create_table_main_building_rooms.sql",
            DATABASE_DIR / "functions/get_building_rooms.sql"
        ]

        for sql_file in sql_files:
            if not sql_file.exists():
                raise FileNotFoundError(
                    f"SQL file not found: {sql_file}"
                )

            execute_sql_file(cursor, sql_file)

        connection.commit()

        print("\nDatabase setup completed successfully!")

        cursor.close()

    except Exception as error:
        if connection:
            connection.rollback()

        print(f"\nDatabase setup failed: {error}")
        raise

    finally:
        if connection:
            connection.close()
            print("Database connection closed.")


if __name__ == "__main__":
    setup_database()
