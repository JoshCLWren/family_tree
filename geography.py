"""Module for Geographic based queries"""

import geograpy


def find_immigrants(family: list):
    """
    Assume that if a person dies in a foreign land they are an immigrant.
    iterate through a family tree and return a new family list with
    updated death country and a list of people who died in a different
    country than where they were born
    """
    immigrants = []
    for person in family:
        person["death_country"] = find_country["death_place"]
        person["birth_country"] = find_country["birth_place"]
        if person["birth_country"] != person["death_country"]:
            immigrants.append(person)
    return immigrants


def find_country(place=None):
    """Find the country of a place"""
    if place:
        return geograpy.get_geoPlace_context(text=place).countries[0]
    else:
        return None
