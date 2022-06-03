import psycopg2
import psycopg2.extras

# Connect to your postgres DB
db_name = "joshwren"
db_user = "postgres"
db_pass = "secret"
db_port = "5431"
# db_string = f"postgres://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"

# conn = psycopg2.connect(
#     f"dbname={db_name} user={db_user} password={db_pass} host={db_host} port={db_port}"
# )
# cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

# Open a cursor to perform database operations


# # Create a table

connection_string = f"dbname={db_name} user={db_user} password={db_pass} port={db_port}"


def migration_create_table():
    with psycopg2.connect(
        f"dbname={db_name} user={db_user} password={db_pass} port={db_port}"
    ) as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:

            cursor.execute(
                """

            """
            )


# Connect to to the database
