import csv, os, os.path,pymongo
import geodict_config


def load_cities():
    reader = csv.reader(open(geodict_config.source_folder+'worldcitiespop.csv', 'rb'))
    
