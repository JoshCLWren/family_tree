"""Module for queries that pertain to a single person"""

import transform


def create_tags(person):
    """Create tags for a person in the family tree"""

    if father := person.father:
        dad = father.name.format()

    if mother := person.mother:
        mom = mother.name.format()

    birth_date = person.sub_tag_value("BIRT/DATE")

    birth_place = person.sub_tag_value("BIRT/PLAC")

    death_date = person.sub_tag_value("DEAT/DATE") or False

    death_place = person.sub_tag_value("DEAT/PLAC")

    marriage_date = person.sub_tag_value("MARR/DATE")

    marriage_place = person.sub_tag_value("MARR/PLAC")

    is_alive = not death_date and not death_place

    if is_alive:
        death_date = None
        death_place = None

    print(f"{person.name.format()}'s father is {dad}")
    print(f"{person.name.format()}'s mother is {mom}")
    print(f"{person.name.format()}'s birth date is {birth_date}")
    print(f"{person.name.format()}'s birth place is {birth_place}")
    print(f"{person.name.format()}'s marriage date is {marriage_date}")
    print(f"{person.name.format()}'s marriage place is {marriage_place}")
    if is_alive:
        print(f"{person.name.format()} is alive")
    else:
        print(f"{person.name.format()} is dead as of {death_date}")
    if death_place:
        print(f"{person.name.format()}'s died in {death_place}")

    return _person_dict(
        person,
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


def _person_dict(
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
    return {
        "name": indi.name.format().title(),
        "father": father.name.format().title() if father else None,
        "mother": mother.name.format().title() if mother else None,
        "birth_date": transform.serialize_date(birth_date),
        "birth_place": birth_place,
        "death_date": transform.serialize_date(death_date),
        "death_place": death_place,
        "marriage_date": transform.serialize_date(marriage_date),
        "marriage_place": marriage_place,
        "children": [],
        "father_id": indi.father.xref_id if father else None,
        "mother_id": indi.mother.xref_id if mother else None,
        "spouse_id": None,
        "xref_id": indi.xref_id,
        "sex": indi.sex or None,
        "FAMC_ID": None,
        "FAMS_ID": None,
        "spouse": None,
        "tree_level": indi.level,
        "birth_country": birth_country or None,
        "death_country": death_country or None,
        "is_alive": is_alive,
    }
