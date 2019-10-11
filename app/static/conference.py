from __future__ import print_function
import xml.etree.cElementTree as ET


class Conference:
    """Stores information about name, number, date and year,
    description and additional information about the conference.
    """

    def __init__(self, name_en, name_ru,
                 add_info_en, add_info_ru,
                 number,
                 year,
                 date_en, date_ru,
                 desc_en, desc_ru):
        """Class constructor."""
        self.name_en = name_en
        self.name_ru = name_ru
        self.add_info_en = add_info_en
        self.add_info_ru = add_info_ru
        self.number = number
        self.year = year
        self.date_en = date_en
        self.date_ru = date_ru
        self.desc_en = desc_en
        self.desc_ru = desc_ru


def parse_conference_xml(conference_xmlfilename):
    """Gets information about the conference from XML file's root_conference.
    Returns object of Conference class."""

    tree_conference = ET.parse(conference_xmlfilename)
    root_conference = tree_conference.getroot()

    name_en = root_conference[0].text
    name_ru = root_conference[1].text
    add_info_en = root_conference[2].text
    add_info_ru = root_conference[3].text
    number = root_conference[4].text
    year = root_conference[5].text
    date_en = root_conference[6].text
    date_ru = root_conference[7].text
    desc_en = root_conference[8].text
    desc_ru = root_conference[9].text

    conference = Conference(name_en,
                            name_ru,
                            add_info_en,
                            add_info_ru,
                            number,
                            year,
                            date_en,
                            date_ru,
                            desc_en,
                            desc_ru)

    return conference
