import csv, os, os.path,pymongo
import geodict_config


def load_cities():
    reader = csv.reader(open(geodict_config.source_folder+'worldcitiespop.csv', 'rb'))
    
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
        dict = { "coountry":country,"city":city,"region_code":region_code,"lat":lat,"lon":lon,"last_word":last_word    }
