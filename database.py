import psycopg2
import psycopg2.extras

# Connect to your postgres DB
db_name = "joshwren"
db_user = "postgres"
db_port = "5431"
db_host = "localhost"


dsn = "postgres://localhost:5431/joshwren"


def connection():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect(dsn)


def dict_cursor():
    """Return a cursor that returns rows as dictionaries."""
    conn = connection()
    return conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)


def dynamic_update(update_dictionary, table_name="people"):
    """Update the database with the values in the dictionary."""

    sql = f"UPDATE {table_name} SET " + ",".join(
        [f"{column} = %({column})s" for column in update_dictionary]
    )

    sql += " WHERE id = %(id)s RETURNING *;"
    return sql


def insert_query_builder(columns, table_name, insert_dict, returning="*"):
    """Build the insert query."""
    columns_to_insert = [column for column in columns if column in insert_dict.keys()]
    sql = f"INSERT INTO {table_name} "
    sql += "(" + ", ".join(columns_to_insert) + ") VALUES ("

    for key in insert_dict:
        sql += f"%({key})s, "
    # remove the last comma and space
    sql = sql[:-2]
    sql += ")"
    sql += f" RETURNING {returning};"
    return sql
