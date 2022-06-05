from models import tree, marriage, person, family
from ged4py.parser import GedcomReader
import geography

file_path = "./tree/josh_wren_tree.ged"


class Menu:
    """Menu option interface"""

    def __init__(self):
        """initialize menu class"""
        self.use_default = input(
            f"""Press enter to use default file_path: {file_path}
                    Press q to quit
                    Press n to enter a new file path"""
        )
        if len(self.use_default) == 0:
            self.file_path = file_path
        if self.use_default.lower().startswith("q"):
            quit()
        if self.use_default.lower().startswith("n"):
            self.file_path = input(
                "Enter a valid file path followed by enter or press enter now to quit."
            )
            if self.file_path is None:
                quit()
        if self.file_path is None:
            quit()
        self.options = Options(file_path)

    def display_options(self):
        """display the different options user has"""
        print(
            """
        1. Create family tree
        2. Update Immigrant status
        3. Quit
        """
        )
        option_input = int(input("Enter an option from the menu"))
        options_dict = {
            1: self.options.create_tree,
            2: self.options.update_immigrants,
            3: quit,
        }

        return options_dict[option_input]()


def quit(self):
    """quit to terminal"""

    return False


class Options:
    """Scripts to seed the database."""

    def __init__(self, file_path):
        """initialize the menu options"""
        self.file_path = file_path
        self.family_list = []
        self.families = []
        self.family_ids = []

    def create_tree(self):
        """create a tree object"""
        try:
            family_tree = tree.FamilyTree(self.file_path)
        except Exception:
            print("Please enter a valid file path")
            return
        self.family_list, self.families, self.family_ids = family_tree.create()
        for _fam_id in self.family_ids:
            fam = marriage.Marriage(id=_fam_id)
            fam.create()
        for record in self.family_list:
            human = person.Person(gedcom_record=record)
            human.create()
        for _spouse in self.families["FAMS"]:
            fam = marriage.Marriage(id=_spouse["value"])
            human = person.Person(id=_spouse["xref_id"])
            human_dict = human.read()
            spouse = "wife"
            if human_dict["sex"] is not None:
                if human_dict["sex"] == "Female":
                    spouse = "husband"
                fam.update(f"{spouse}_id")

    def update_immigrants(self):
        """Update immigrant status of every person in family list"""

        everybody = family.Family()
        family_collection = everybody.get_all()
        self.immigrants = geography.find_immigrants(family_collection)

        print(f"Total possible immigrants found: {len(self.immigrants)}")
        print(f"here they are: {self.immigrants}")


def main():
    """Main function"""
    while True:
        main_menu = Menu()
        while True:
            main_menu.display_options()


main()
