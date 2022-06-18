"""Module for queries that pertain to a single human"""

import transform
import geography
from models.person import Person
import psycopg2


def create_tags(human):
    """Create tags for a human in the family tree"""

    if father := human.father:
        dad = father.name.format()
        print(f"{human.name.format()}'s father is {dad}")

    if mother := human.mother:
        mom = mother.name.format()
        print(f"{human.name.format()}'s mother is {mom}")

    birth_date = human.sub_tag_value("BIRT/DATE")
    print(f"{human.name.format()}'s birth date is {birth_date}")

    birth_place = human.sub_tag_value("BIRT/PLAC")
    print(f"{human.name.format()}'s birth place is {birth_place}")

    death_date = human.sub_tag_value("DEAT/DATE") or False

    death_place = human.sub_tag_value("DEAT/PLAC") or None

    marriage_date = human.sub_tag_value("MARR/DATE") or None
    print(f"{human.name.format()}'s marriage date is {marriage_date}")

    marriage_place = human.sub_tag_value("MARR/PLAC") or None
    print(f"{human.name.format()}'s marriage place is {marriage_place}")

    is_alive = not death_date and not death_place

    if is_alive:
        death_date = None
        death_place = None

        print(f"{human.name.format()} is alive")
    else:
        print(f"{human.name.format()} is dead as of {death_date}")
    if death_place:
        print(f"{human.name.format()}'s died in {death_place}")

    child = Person(id=human.xref_id)
    if isinstance(child.tags, psycopg2.extras.RealDictRow):
        print(f"{human.name.format()} is already in the database")
        return child

    child = Person(
        _human_dict(
            human,
            father,
            mother,
            birth_date,
            birth_place,
            death_date,
            death_place,
            marriage_date,
            marriage_place,
            is_alive,
        )
    )
    child.create()

    return child


def _human_dict(
    indi,
    father,
    mother,
    birth_date,
    birth_place,
    death_date,
    death_place,
    marriage_date,
    marriage_place,
    is_alive,
    death_country=None,
    birth_country=None,
):
    is_immigrant = False
    if death_country is None and death_place is not None:
        try:
            death_country = geography.find_country(death_place)
        except IndexError:
            death_country = None
    if birth_country is None and birth_place is not None:
        try:
            birth_country = geography.find_country(birth_place)
        except IndexError:
            birth_country = None
    if birth_country and death_country and birth_country != death_country:
        print(
            f"{indi.name.format()} was born in {birth_country} and died in {death_country}"
        )
        is_immigrant = True
    birth = transform.serialize_date(birth_date)
    death = transform.serialize_date(death_date)
    marriage = transform.serialize_date(marriage_date)

    return {
        "name": indi.name.format().title(),
        "father": father.name.format().title() if father else None,
        "mother": mother.name.format().title() if mother else None,
        "birth_date": birth[0],
        "birth_year": birth[1],
        "birth_place": birth_place,
        "death_date": death[0],
        "death_year": death[1],
        "death_place": death_place,
        "marriage_date": marriage[0],
        "marriage_year": marriage[1],
        "marriage_place": marriage_place,
        "children": [],
        "father_id": indi.father.xref_id if father else None,
        "mother_id": indi.mother.xref_id if mother else None,
        "spouse_id": None,
        "id": indi.xref_id,
        "sex": indi.sex or None,
        "FAMC_ID": None,
        "FAMS_IDs": None,
        "spouse": None,
        "tree_level": indi.level,
        "birth_country": birth_country,
        "death_country": death_country,
        "is_alive": is_alive,
        "is_immigrant": is_immigrant,
    }
