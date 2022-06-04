# from python_gedcom_2.element.individual import IndividualElement


# from python_gedcom_2.parser import Parser

# # Path to your ".ged" file

import asyncio
import re
from tkinter.font import families

import psycopg2
import geograpy

file_path = "./tree/josh_wren_tree.ged"

# # Initialize the parser
# gedcom_parser = Parser()

# # Parse your file
# gedcom_parser.parse_file(file_path)

# root_child_elements = .get_root_child_elements()

# # Iterate through all root child elements
# for element in root_child_elements:

#     # Is the "element" an actual "IndividualElement"? (Allows usage of extra functions such as "surname_match" and "get_name".)
#     if isinstance(element, IndividualElement):

#         # Get all individuals whose surname matches "Doe"
#         import pdb

#         pdb.set_trace()
#         # Unpack the name tuple
#         (first, last) = element.get_name()

#         # Print the first and last name of the found individual
#         name = f"{first} {last}"

import ged4py.date
from ged4py.parser import GedcomReader
import db_config

# open GEDCOM file


def serialize_date(value):
    regex = r"[0-9]{4,7}(?![0-9])"
    if not value:
        return None
    if isinstance(value, ged4py.date.DateValuePhrase):

        new_value = value.phrase
        if new_value in ["DECEASED", "UNKNOWN", "unk"]:

            return (new_value, None)

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


import contextlib


async def build_person_record(family, serialize_date, count, family_ids, indi):
    print(f"{count}: {indi.name.format()}")

    if father := indi.father:
        dad = father.name.format()

    if mother := indi.mother:
        mom = mother.name.format()

    birth_date = indi.sub_tag_value("BIRT/DATE")

    birth_place = indi.sub_tag_value("BIRT/PLAC")

    death_date = indi.sub_tag_value("DEAT/DATE")

    death_place = indi.sub_tag_value("DEAT/PLAC")

    marriage_date = indi.sub_tag_value("MARR/DATE")

    marriage_place = indi.sub_tag_value("MARR/PLAC")

    count += 1
    death_country = None
    birth_country = None
    with contextlib.suppress(Exception):
        if death_place:
            death_country = geograpy.get_geoPlace_context(text=death_place).countries[0]
    with contextlib.suppress(Exception):
        if birth_place:
            birth_country = geograpy.get_geoPlace_context(text=birth_place).countries[0]
    person = {
        "id": count,
        "name": indi.name.format().title(),
        "father": father.name.format().title() if father else None,
        "mother": mother.name.format().title() if mother else None,
        "birth_date": serialize_date(birth_date),
        "birth_place": birth_place,
        "death_date": serialize_date(death_date),
        "death_place": death_place,
        "marriage_date": serialize_date(marriage_date),
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
    }

    for tags in indi.sub_records:
        if tags.tag in ("FAMC", "FAMS"):
            families[tags.tag].append({"xref_id": indi.xref_id, "value": tags.value})
            person[f"{tags.tag}_ID"] = tags.value
            if tags.value not in family_ids:
                family_ids.append(tags.value)
            # if tags.tag not in [
            #     "BIRT/DATE",
            #     "BIRT/PLAC",
            #     "DEAT/DATE",
            #     "DEAT/PLAC",
            #     "MARR/DATE",
            #     "MARR/PLAC",
            # ]:
            #     import pdb

            #     pdb.set_trace()
            #     pass


from asyncio import gather, create_task


async def main():
    with GedcomReader(file_path) as parser:
        family = []
        count = 0
        # The FAMC tag provides a pointer to a family where this person is a child.
        # The FAMS tag provides a pointer to a family where this person is a spouse or
        # parent.
        families = {"FAMC": [], "FAMS": []}
        family_ids = []
        # iterate over each INDI record in a file

        # Print a name (one of many possible representations)

        # person = await asyncio.gather(
        #     map(
        #         build_person_record(family, serialize_date, count, family_ids, indi),
        #         parser.records0("INDI"),
        #     )
        # )
        tasks = []
        for indi in parser.records0("INDI"):

            task = create_task(
                build_person_record(family, serialize_date, count, family_ids, indi)
            )
            tasks.append(task)

        family = await gather(*tasks)

    # for child in family:
    #     for parent in ["father", "mother"]:
    #         if child[f"{parent}_id"] == person["xref_id"]:
    #             person["children"].append(child["name"])

    family_ids = set(family_ids)
    family_relationships = []
    for _id in family_ids:
        new_family = {"family_id": _id, "children": [], "spouses": []}
        for child in families["FAMC"]:
            if child["value"] == _id:
                new_family["children"].append(child["xref_id"])
        for spouse in families["FAMS"]:
            if spouse["value"] == _id:
                new_family["spouses"].append(spouse["xref_id"])
        family_relationships.append(new_family)

    immigrants = []

    for person in family:
        if person["birth_country"] != person["death_country"]:
            immigrants.append(person)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
