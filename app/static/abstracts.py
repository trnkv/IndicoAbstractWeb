# -*- coding: utf-8 -*-
from __future__ import print_function
import csv
import unicodedata as ud

import xml.etree.cElementTree as ET
import lxml.etree as LXML_ET


class Abstract:
    """Stores information about title, content, authors and track of the abstract."""

    def __init__(self, abstract_id, title, content, authors, track):
        """Class constructor."""
        self.abstract_id = abstract_id
        self.title = title
        self.content = content
        self.authors = authors
        self.track = track


class Person:
    """Stores information about first name, family name, email and affiliation
        of a person."""

    def __init__(self, first_name, family_name, email, affiliation, is_speaker):
        """Class constructor."""
        self.first_name = first_name
        self.family_name = family_name
        self.email = email
        self.affiliation = affiliation
        self.is_speaker = is_speaker

def create_dict_standarts(csv_file):
    """Creates a dictionary from CSV file."""
    standarts = {}

    #with open(csv_file, encoding='utf-8') as f_obj:
    reader = csv.DictReader(csv_file, delimiter=':')
    for line in reader:
        key = line["old_affiliation"]
        value = line["new_affiliation"]
        standarts[key] = value
    return standarts


def parse_abstracts_xml(abstracts_xmlfilename, abstracts_xmlfilename_copy, csv_file, status_string):
    """ Method for getting structured list containing all the abstracts from XML.
    Every abstract in the list is an object of Abstract class.
    It contains 4 main components:
    1. Track of abstract
    2. Title
    3. List of authors. Every author is an object of Person class
    4. Abstract itself (content)
    """
    tree_abstracts = ET.parse(abstracts_xmlfilename)
    root_abstracts = tree_abstracts.getroot()
    doc_abstracts = LXML_ET.parse(abstracts_xmlfilename_copy)
    count_abstracts = doc_abstracts.xpath('count(//abstract)')

    abstract_id = 0
    track = ""
    title = ""
    content = ""
    flag = False
    authors = []
    abstracts_list = []
    unknown_affiliations = []

    affiliation_standarts = create_dict_standarts(csv_file)
    

    status_string.append({"first":"Parsed all abstracts from XML"})
    for i in range(1, int(count_abstracts) + 1):
        for child in root_abstracts[i]:
            if child.tag == "Id":
                abstract_id = int(child.text.strip())
            if child.tag == "Title":
                title = child.text.strip()
                continue

            if child.tag == "Content":
                content = child.text.strip()
                continue

            if child.tag == "PrimaryAuthor" or child.tag == "Co-Author":
                # Bringing different affiliations to the same standard
                affiliation = str(child[3].text).strip()
                # If affiliation is in standards - bring affiliation to standard
                if affiliation in affiliation_standarts:
                    affiliation = affiliation_standarts[affiliation]
                else:
                    unknown_affiliations.append(affiliation)

                author = Person(first_name=str(child[0].text),
                                        family_name=str(child[1].text),
                                        email=str(child[2].text),
                                        affiliation=affiliation,
                                        is_speaker=False)
                authors.append(author)
                continue

            if child.tag == "Speaker":
                for author in authors:
                    if author.first_name == str(child[0].text) and author.family_name == str(child[1].text):
                        author.is_speaker=True
                continue

            if child.tag == "Track" and not flag:
                track = child.text
                flag = True
                continue

        abstract = Abstract(abstract_id, title, content, authors, track)
        abstracts_list.append(abstract)
        authors = []
        flag = False

    # Print unknown affiliations
    unknown_affiliations = list(set(unknown_affiliations))
    status_string.append({"second":"The following affiliations are unknown. Please add them to CSV file with standards."})
    status_string.append({"second_items":[]})
    for affiliation in unknown_affiliations:
        status_string[2]["second_items"].append(affiliation)
    #status_string.append("=======================================================")

    return abstracts_list, status_string

def get_language_of_string(input_string):
    # Threshold to determine language
    # If the ratio of one symbols required to define language.
    THRESHOLD = 0.6

    alphabet = {
        'LATIN': 0,
        'CYRILLIC': 0
    }

    for symbol in input_string:
        try:
            if 'LATIN' in ud.name(symbol):
                alphabet['LATIN'] += 1
            if 'CYRILLIC' in ud.name(symbol):
                alphabet['CYRILLIC'] += 1
        except ValueError:
            # If it is TAB
            if ord(symbol) == 9:
                continue
            # If it is New Line
            if ord(symbol) == 10:
                continue
            print(str(symbol) + "symbol not found. Code: " + str(ord(symbol)))

    if alphabet['LATIN'] == 0 and alphabet['CYRILLIC'] == 0:
        return "NONE"

    if alphabet['LATIN'] / (alphabet['CYRILLIC'] + alphabet['LATIN'])> THRESHOLD:
        return "LATIN"

    if alphabet['CYRILLIC'] / (alphabet['CYRILLIC'] + alphabet['LATIN'])> THRESHOLD:
        return "CYRILLIC"

    return "MIXED"

def check_abstracts_consistency(abstracts, status_string):
    j = 0
    for abstract in abstracts:
        # Check language consistency
        languages = {}
        languages['Title'] = get_language_of_string(abstract.title)
        languages['Content'] = get_language_of_string(abstract.content)
        for i in range(len(abstract.authors)):
            languages['Author' + str(i) + "_Name"] = get_language_of_string(abstract.authors[i].first_name + abstract.authors[i].family_name)
            languages['Author' + str(i) + "_Affiliation"] = get_language_of_string(abstract.authors[i].affiliation)


        languages_set = set(languages.values())
        if 'NONE' in languages_set:
            languages_set.remove('NONE')
        if len(languages_set) != 1:
            status_string[3]["mores"].append([])
            status_string[3]["mores"][j].append("More than one language is used in abstract with Id: " + str(abstract.abstract_id) + "\r\n")
            status_string[3]["mores"][j].append("Email to contact Speaker: " + str([author.email for author in abstract.authors if author.is_speaker]))
            status_string[3]["mores"][j].append("Speaker's name: " + str([author.first_name + " " + author.family_name for author in abstract.authors if author.is_speaker]))
            status_string[3]["mores"][j].append(languages)
            j += 1

            #status_string.append('_______________________________________________________')
    #status_string.append('=======================================================')
    return  status_string

def check_abstract_count_words(abstracts, status_string):
    for abstract in abstracts:

        # Check count of symbols in abstract's content
        words = len(set(abstract.content.split()))
        if words < 100:
            status_string[4]["warnings"].append('WARNING: too few words in content of abstract with Id= ' + str(abstract.abstract_id) + ': ' + str(words) + ' words')
        if words > 360:
            status_string[4]["warnings"].append('WARNING: too many words in content of abstract with Id= ' + str(abstract.abstract_id) + ': ' + str(words) + ' words')
        return status_string

