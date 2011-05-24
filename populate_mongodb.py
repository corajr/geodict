#!/usr/bin/env python

import csv, os, os.path
import geodict_config
from pymongo import Connection
from geodict_lib import *

def load_cities(cursor):
    db = Connection().geodict
    reader = csv.reader(open(geodict_config.source_folder+'worldcitiespop.csv', 'rb'))
    enc = "latin-1"
    for row in reader:
        try:
            country = row[0]
            city = row[1]
            region_code = row[3]
            population = row[4]
            lat = row[5]
            lon = row[6]
        except:
            continue

        if population is '':
            population = 0

        city = city.strip()

        last_word, index, skipped = pull_word_from_end(city, len(city)-1, False)
        document = { "coountry":country.decode(enc),"city":city.decode(enc),"region_code":region_code.decode(enc),"lat":lat,"lon":lon,"last_word":last_word.decode(enc)    }
        db.cities.insert(document)


load_cities({})
