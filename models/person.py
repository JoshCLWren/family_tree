"""Model for a person."""

import transform
import individual


class Person:
    """Model for a person."""

    def __init__(self, gedcom_record):
        self.gedcom_record = gedcom_record
        self.tags = individual.create_tags(self.gedcom_record)

    def create(self):
        """Create a person from an INDI record."""
