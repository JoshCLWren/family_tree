"""Module for transforming data from one type or format to another"""

import ged4py.date
import re


def serialize_date(value):
    """Serialize a date"""
    if not value:
        return (None, None)
    if isinstance(value, ged4py.date.DateValuePhrase):

        new_value = value.phrase
        if new_value in ["DECEASED", "UNKNOWN", "unk"]:

            return (new_value, None)

        regex = r"[0-9]{4,7}(?![0-9])"
        if years := re.search(regex, new_value):
            return new_value, int(years[0])

        birth_year = int(new_value[:4])
    if isinstance(value, ged4py.date.DateValueSimple):
        new_value = value.date.original
        birth_year = value.date.year
    if isinstance(
        value,
        (
            ged4py.date.DateValueAbout,
            ged4py.date.DateValueBefore,
            ged4py.date.DateValueAfter,
        ),
    ):
        new_value = str(value.date)
        try:
            birth_year = int(new_value)
        except ValueError:
            birth_year = None

    return (new_value, birth_year)
