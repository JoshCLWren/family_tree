"""Model for a (nuclear) family."""

import psycopg2
import database

marriage_columns = (
    "id",
    "husband_id",
    "marriage_date",
    "marriage_place",
    "marriage_year",
    "wife_id",
    "tree_level",
    "is_divorced",
    "divorce_date",
)


class Marriage:
    """Class for a marriage"""

    def __init__(self, id=None, marriage_values=None):
        """Initialize a marriage."""
        self.id = None
        if id:
            self.id = id
        if marriage_values:
            for column in marriage_columns:
                setattr(self, column, self.tags[column])
        else:
            for column in marriage_columns:
                if column == "id":
                    continue
                setattr(self, column, None)
        if self.id:

            print(f"Marriage: {self.id} initialized.")

    def read(self, id=None, spouse_id=None):
        """Read a marriage from the db."""
        if id:
            with database.dict_cursor() as cursor:
                cursor.execute(
                    """
                    SELECT * FROM traditional_marriages WHERE id = %s;
                    """,
                    (self.id,),
                )
                return cursor.fetchone()

        if spouse_id:
            with database.dict_cursor() as cursor:
                cursor.execute(
                    """
                    SELECT * FROM traditional_marriages WHERE husband_id = %s OR wife_id = %s;
                    """,
                    (self.spouse_id,),
                )
                return cursor.fetchone()

    def create(self):
        """Create a marriage from an FAM record."""

        if fam := self.read(id=self.id):
            print(f"Marriage {fam['id']} already exists.")
            return fam

        insert_dictionary = {
            column: getattr(self, column) for column in marriage_columns
        }

        sql = database.insert_query_builder(
            columns=marriage_columns,
            table_name="traditional_marriages",
            insert_dict=insert_dictionary,
        )

        with psycopg2.connect(database.dsn) as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:

                cursor.execute(sql, insert_dictionary)

                marriage = cursor.fetchone()

        print(f"Marriage: {marriage['id']} created.")
        return marriage

    def read(self, id=None, spouse_id=None):
        """Read a marriage from the db."""
        if id:
            with database.dict_cursor() as cursor:
                cursor.execute(
                    """
                    SELECT * FROM traditional_marriages WHERE id = %s;
                    """,
                    (self.id,),
                )
                return cursor.fetchone()

        if spouse_id:
            with database.dict_cursor() as cursor:
                cursor.execute(
                    """
                    SELECT * FROM traditional_marriages WHERE husband_id = %s OR wife_id = %s;
                    """,
                    (self.spouse_id,),
                )
                return cursor.fetchone()

    def update(self, update_dictionary):
        """Update a marriage from an FAM record."""

        sql = database.dynamic_update(update_dictionary, "traditional_marriages")

        with database.dict_cursor() as cursor:
            cursor.execute(sql, update_dictionary)

            return cursor.fetchone()

    def delete(self):
        """Delete a marriage."""

        with database.dict_cursor() as cursor:
            cursor.execute(
                """
                DELETE FROM traditional_marriages WHERE id = %s;
                """,
                (self.id,),
            )

            return cursor.fetchone()

    def save(self):
        """Save a marriage."""

        return self.update(self.tags) if self.id else self.create()
