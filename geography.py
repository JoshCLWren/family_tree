"""Module for Geographic based queries"""

import geograpy
from models.person import Person
import logging

logging.basicConfig(filename="geography.log", level=logging.DEBUG)


class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def find_immigrants(family_list):
    """
    Assume that if a human dies in a foreign land they are an immigrant.
    iterate through a family tree and return a new family list with
    updated death country and a list of people who died in a different
    country than where they were born
    """
    immigrants = []
    message = f"Total family members = {len(family_list)}"
    logging.warning(message)
    print(f"{bcolors.WARNING}{message}")
    for human in family_list:
        logging.info(f"Checking {human['name']}'s birth and death country")
        update_dict = {"is_immigrant": False}
        for event in ("birth", "death"):

            if human[f"{event}_place"]:
                logging.info(
                    f"{human['name']}'s {event} place: {human[f'{event}_place']}"
                )
                try:
                    logging.info(f"Finding what country {human['name']} was born in")
                    update_dict[f"{event}_country"] = find_country(
                        human[f"{event}_place"]
                    )
                    logging.info(f"Found country: update_dict[f'{event}_country']")

                    human[f"{event}_country"] = update_dict[f"{event}_country"]
                except IndexError:
                    message = f"Failed to find country for {human['name']} in {human[f'{event}_place']}"
                    logging.warning(message)
                    print(f"{bcolors.WARNING}{message}")
                    human[f"{event}_country"] = None

        if human["birth_place"] is None:
            message = f"{human['name']}'s birth place is None, not enough info to check"
            logging.warning(message)
            print(f"{bcolors.WARNING}{message}")
            continue
        if human["death_place"] is None:
            message = f"{human['name']}'s death place is None, not enough info to check"
            logging.warning(message)
            print(f"{bcolors.WARNING}{message}")
            continue
        if human["birth_country"] is None:
            message = (
                f"{human['name']}'s birth country is None, not enough info to check"
            )
            logging.warning(message)
            print(f"{bcolors.WARNING}{message}")
            continue
        if human["death_country"] is None:
            message = (
                f"{human['name']}'s death country is None, not enough info to check"
            )
            logging.warning(message)
            print(f"{bcolors.WARNING}{message}")
            continue
        if (
            str(human["birth_country"]) != str(human["death_country"])
            and str(human["birth_country"]) not in str(human["death_country"])
            and str(human["death_country"]) not in str(human["birth_country"])
        ):
            message = f"Immigrant found! {human['name']} was born in {human['birth_country']} and died in {human['death_country']}"
            logging.warning(message)
            print(f"{bcolors.OKGREEN}{message}")

            update_dict["is_immigrant"] = True
            if human["birth_country"] != "United States of America":
                immigrants.append(human)

        person_to_update = Person(id=human["id"])
        person_to_update.update(update_dictionary=update_dict)

    return immigrants


def find_country(place=None):
    """Find the country of a place"""

    if not place:
        return None
    common_origins = ("america", "england", "usa", "okc", "united states")
    for country in common_origins:
        if country in place.lower():
            if country == "okc":
                return "United States of America"
            return (
                "United States of America"
                if country in ["usa", "united states"]
                else country.title()
            )

    for state in united_states_of_america:
        if state.lower() in place.lower():
            return "United States of America"
    for state in state_abbreviations:
        if state.lower() in place.lower():
            return "United States of America"
    country = geograpy.get_geoPlace_context(text=place).countries[0]
    if country is None:
        logging.warning(f"Failed to find country for {place} using geograpy")
        return None
    return country.title()


united_states_of_america = (
    "Alabama",
    "Alaska",
    "Arizona",
    "Arkansas",
    "California",
    "Colorado",
    "Connecticut",
    "Delaware",
    "Florida",
    "Georgia",
    "Hawaii",
    "Idaho",
    "Illinois",
    "Indiana",
    "Iowa",
    "Kansas",
    "Kentucky",
    "Louisiana",
    "Maine",
    "Maryland",
    "Massachusetts",
    "Michigan",
    "Minnesota",
    "Mississippi",
    "Missouri",
    "Montana",
    "Nebraska",
    "Nevada",
    "New Hampshire",
    "New Jersey",
    "New Mexico",
    "New York",
    "North Carolina",
    "North Dakota",
    "Ohio",
    "Oklahoma",
    "Oregon",
    "Pennsylvania",
    "Rhode Island",
    "South Carolina",
    "South Dakota",
    "Tennessee",
    "Texas",
    "Utah",
    "Vermont",
    "Virginia",
    "Washington",
    "West Virginia",
    "Wisconsin",
    "Wyoming",
)

state_abbreviations = (
    "AL",
    "AK",
    "AZ",
    "AR",
    "CA",
    "CO",
    "CT",
    "DE",
    "FL",
    "GA",
    "HI",
    "ID",
    "IL",
    "IN",
    "IA",
    "KS",
    "KY",
    "LA",
    "ME",
    "MD",
    "MA",
    "MI",
    "MN",
    "MS",
    "MO",
    "MT",
    "NE",
    "NV",
    "NH",
    "NJ",
    "NM",
    "NY",
    "NC",
    "ND",
    "OH",
    "OK",
    "OR",
    "PA",
    "RI",
    "SC",
    "SD",
    "TN",
    "TX",
    "UT",
    "VT",
    "VA",
    "WA",
    "WV",
    "WI",
    "WY",
)
