"""Module for Geographic based queries"""

import contextlib
import geograpy


def find_immigrants(family: list):
    """
    Assume that if a person dies in a foreign land they are an immigrant.
    iterate through a family tree and return a new family list with
    updated death country and a list of people who died in a different
    country than where they were born
    """
    immigrants = []
    new_family_list = []
    for person in family:
        with contextlib.suppress(Exception):
            if person["death_place"]:
                person["death_country"] = geograpy.get_geoPlace_context(
                    text=person["death_place"]
                ).countries[0]
        with contextlib.suppress(Exception):
            if person["birth_place"]:
                person["birth_country"] = geograpy.get_geoPlace_context(
                    text=person["birth_place"]
                ).countries[0]
        if person["birth_country"] != person["death_country"]:
            immigrants.append(person)
        new_family_list.append(person)
    return (immigrants, new_family_list)
