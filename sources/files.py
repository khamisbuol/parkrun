import json
import sys
import os


current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir  = os.path.dirname(current_dir)
sys.path.append(parent_dir)
from scripts.scrape import get_countries, get_locations
sys.path.remove(parent_dir)

ignore = ['Eswatini', 'Namibia']

def create_json_files():
    print('Generating JSON files for countries')
    countries = get_countries()

    # Write the dictionary to a JSON file
    # with open('countries.json', 'w', encoding='utf-8') as json_file:
    #     json.dump(countries, json_file, ensure_ascii=False, indent=4)
    
    for country, data in countries.items():
        print(country)
        print(data)
        if country not in ignore:
            locations = get_locations(country)
            # print(f'country: {country}')
            # print(f'data: {data}')
            countries[country]['locations'] = locations
            print(f'locations: {locations}')
        # print(countries[country])
        print('-----------------------------------------------------------')
    
    filename = 'parkrun.json'

    # Write the dictionary to a JSON file
    # with open(filename, 'w', encoding='utf-8') as json_file:
    #     json.dump(countries, json_file, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    create_json_files()