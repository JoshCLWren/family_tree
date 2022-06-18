"""Model for a person."""


import contextlib
import individual
import psycopg2
import database
from models import marriage

person_columns = (
    "id",
    "name",
    "father",
    "mother",
    "birth_date",
    "birth_year",
    "death_year",
    "death_date",
    "tree_level",
    "is_alive",
    "is_immigrant",
    "children",
    "birth_country",
    "death_country",
    "birth_place",
    "death_place",
)


class Person:
    """Model for a person."""

    def __init__(self, gedcom_record=None, id=None):
        """Initialize a person."""
        if id:
            self.id = id
            self.tags = self.read()
        if gedcom_record:

            if isinstance(gedcom_record, Person):
                self.id = gedcom_record.id
            else:
                self.id = gedcom_record["id"]
            try:
                human = self.read()
            except Exception:
                human = None
            if not isinstance(human, psycopg2.extras.RealDictRow):
                try:
                    self.tags = individual.create_tags(gedcom_record)
                except AttributeError:
                    self.tags = gedcom_record
            else:
                self.tags = human
        if self.tags:
            for column in person_columns:
                setattr(self, column, self.tags[column])

    def create(self):
        """Create a person from an INDI record."""

        with contextlib.suppress(AttributeError):
            if human := self.read():
                print(f"This human {human['id']} already exists.")
                return human

        insert_dictionary = {column: getattr(self, column) for column in person_columns}

        sql = database.insert_query_builder(person_columns, "people", insert_dictionary)

        with psycopg2.connect(database.dsn) as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:

                cursor.execute(sql, insert_dictionary)

                human = cursor.fetchone()

        return human

    def read(self):
        """Read a person from a file."""

        with database.dict_cursor() as cursor:
            cursor.execute(
                """
                SELECT * FROM people WHERE id = %s;
                """,
                (self.id,),
            )
            human = cursor.fetchone()

        return human

    def update(self, update_dictionary):
        """Update a person."""

        sql = database.dynamic_update(update_dictionary)

        with database.dict_cursor() as cursor:
            cursor.execute(sql, {"id": self.id, **update_dictionary})
            return cursor.fetchone()

    def delete(self):
        """Delete a person."""

        with database.dict_cursor() as cursor:
            cursor.execute(
                """
                DELETE FROM people WHERE id = %s RETURNING *;
                """,
                (self.id,),
            )
            return cursor.fetchone()

    def save(self):
        """Save a person."""

        return self.update(self.tags) if self.id else self.create()
