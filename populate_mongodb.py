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


def load_countries(cursor):
    db = Connection().geodict
    reader = csv.reader(open(geodict_config.source_folder+'countrypositions.csv', 'rb'))
    country_positions = {}

    for row in reader:
        try:
            country_code = row[0]
            lat = row[1]
            lon = row[2]
        except:
            continue

        country_positions[country_code] = { 'lat': lat, 'lon': lon }
        
    reader = csv.reader(open(geodict_config.source_folder+'countrynames.csv', 'rb'))

    for row in reader:
        try:
            country_code = row[0]
            country_names = row[1]
        except:
            continue    

        country_names_list = country_names.split(' | ')
        
        lat = country_positions[country_code]['lat']
        lon = country_positions[country_code]['lon']
        
        for country_name in country_names_list:
        
            country_name = country_name.strip()
            
            last_word, index, skipped = pull_word_from_end(country_name, len(country_name)-1, False)
            document = { "country": country_name,"country_code":country_code,"lat":lat,"lon":lon,"last_word": last_word }
            db.countries.insert(document)        


def load_regions():
    db = Connection().geodict
    reader = csv.reader(open(geodict_config.source_folder+'us_statepositions.csv', 'rb'))
    us_state_positions = {}

    for row in reader:
        try:
            region_code = row[0]
            lat = row[1]
            lon = row[2]
        except:
            continue

        us_state_positions[region_code] = { 'lat': lat, 'lon': lon }
    
    reader = csv.reader(open(geodict_config.source_folder+'us_statenames.csv', 'rb'))

    country_code = 'US'

    for row in reader:
        try:
            region_code = row[0]
            state_names = row[2]
        except:
            continue    

        state_names_list = state_names.split('|')
        
        lat = us_state_positions[region_code]['lat']
        lon = us_state_positions[region_code]['lon']

        for state_name in state_names_list:
    
            state_name = state_name.strip()
            
            last_word, index, skipped = pull_word_from_end(state_name, len(state_name)-1, False)
            document = {"region": state_name,"region_code":region_code,"country_code":country_code,"lat":lat,"lon":lon,"last_word":last_word}
            db.regions.insert(document)
        
load_cities({})
load_countries({})
load_regions({})
