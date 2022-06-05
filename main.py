from models import tree, marriage, person
from ged4py.parser import GedcomReader
import geography

file_path = "./tree/josh_wren_tree.ged"


def main():
    """Script to seed the database."""

    family_tree = tree.FamilyTree(file_path)
    family_list, families, family_ids = family_tree.create()

    for _fam_id in family_ids:
        fam = marriage.Marriage(id=_fam_id)
        fam.create()

    for record in family_list:

        human = person.Person(gedcom_record=record)
        human.create()

    for _spouse in families["FAMS"]:
        fam = marriage.Marriage(id=_spouse["xref_id"])
        human = person.Person(id=_spouse["value"])
        spouse = "husband"
        if human.sex == "Female":
            spouse = "wife"
        fam.update(f"{spouse}_id")

    for record in family_list:
        fam = marriage.Marriage(spouse_id=record["xref_id"])
        fam.update(record)

    immigrants = geography.find_immigrants(family_list)

    for immigrant in immigrants:
        human = person.Person(id=immigrant["xref_id"])
        human.update({"is_immigrant": True})


main()
