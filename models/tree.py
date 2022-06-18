"""Model for a tree."""


from family import _parse_gedcom


class FamilyTree:
    """Family Tree class"""

    def __init__(
        self, file_path, family_list=None, count=0, families=None, family_ids=None
    ):
        """Initialize a Family Tree."""
        self.file_path = file_path
        self.family_list = family_list
        self.count = count
        self.families = families
        self.family_ids = family_ids

    def create(self):
        """Create a family tree from the given gedcom file passed"""
        if self.family_list is None:
            self.family_list = []
        if self.families is None:
            self.families = {"FAMC": [], "FAMS": []}
        if self.family_ids is None:
            self.family_ids = []
        # The FAMC tag provides a pointer to a family where this person is a child.
        # The FAMS tag provides a pointer to a family where this person is a spouse or
        # parent.

        _parse_gedcom(
            self.file_path, self.family_list, self.count, self.families, self.family_ids
        )

        return self.family_list, self.families, self.family_ids
