"""Module for Queries involving family units"""

from ged4py.parser import GedcomReader

import individual


def create_family_relationships(family_ids: list, families: list):
    """Create family relationships"""
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
    return family_relationships, family_ids


def create_fam_tags(families, family_ids, indi, person):
    """Create family tags"""
    for tags in indi.sub_records:
        if tags.tag in ("FAMC", "FAMS"):
            families[tags.tag].append({"xref_id": indi.xref_id, "value": tags.value})
            person[f"{tags.tag}_ID"] = tags.value
            if tags.value not in family_ids:
                family_ids.append(tags.value)
    return families, family_ids


def add_parents(family, person):
    """Add parents to the family tree"""
    for child in family:
        for parent in ["father", "mother"]:
            if child[f"{parent}_id"] == person["xref_id"]:
                person["children"].append(child["name"])
                print(f"{person['name']} has a child named {child['name']}")
    return family


def _parse_gedcom(file_path, family, count, families, family_ids):
    """Parse the gedcom file and create a family tree"""
    with GedcomReader(file_path) as parser:
        # iterate over each INDI record in a file
        for indi in parser.records0("INDI"):
            # Print a name (one of many possible representations)
            print(f"Processing record #{count}: {indi.name.format()}")

            (
                father,
                mother,
                birth_date,
                birth_place,
                death_date,
                death_place,
                marriage_date,
                marriage_place,
            ) = individual.create_tags(indi)

            count += 1

            person = individual._person_dict(
                count,
                indi,
                father,
                mother,
                birth_date,
                birth_place,
                death_date,
                death_place,
                marriage_date,
                marriage_place,
            )

            create_fam_tags(families, family_ids, indi, person)

            family.append(person)

            add_parents(family, person)


def family_tree(file_path, family=None, count=0, families=None, family_ids=None):
    """Create a family tree from the given gedcom file passed"""
    if family is None:
        family = []
    if families is None:
        families = {"FAMC": [], "FAMS": []}
    if family_ids is None:
        family_ids = []
    # The FAMC tag provides a pointer to a family where this person is a child.
    # The FAMS tag provides a pointer to a family where this person is a spouse or
    # parent.

    _parse_gedcom(file_path, family, count, families, family_ids)
    return family, families, family_ids


def _parse_gedcom(file_path, family, count, families, family_ids):
    """Parse the gedcom file and create a family tree"""
    with GedcomReader(file_path) as parser:
        # iterate over each INDI record in a file
        for indi in parser.records0("INDI"):
            # Print a name (one of many possible representations)
            print(f"Processing record #{count}: {indi.name.format()}")

            (
                father,
                mother,
                birth_date,
                birth_place,
                death_date,
                death_place,
                marriage_date,
                marriage_place,
            ) = individual.create_tags(indi)

            count += 1

            person = individual._person_dict(
                count,
                indi,
                father,
                mother,
                birth_date,
                birth_place,
                death_date,
                death_place,
                marriage_date,
                marriage_place,
            )

            create_fam_tags(families, family_ids, indi, person)

            family.append(person)

            add_parents(family, person)

        return family, families, family_ids
