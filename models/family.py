"""Module for Family queries"""

import database


class Family:
    """Class for families"""

    def __init__(self):
        """Initializer"""

    def get_all(self):
        """Get all people from the db"""
        with database.dict_cursor() as cursor:
            cursor.execute(
                """
                SELECT * FROM people;
                """
            )
            return cursor.fetchall()
