import parkrun
import country
import location as lc
import datetime
import os

def main():

    data_folder = os.path.join(os.path.dirname(__file__), '..', 'data')

    # print(countries_dict['USA']['info'])
    timestamp = datetime.datetime.now().strftime('%y%m%d')
    pk = parkrun.Parkrun()
    df = pk.get_largest_clubs()
    # print(df)
    filename = f"get_largest_clubs_{timestamp}.csv"
    filepath = os.path.join(data_folder, filename.replace('get_', ''))

    df.to_csv(filepath)


    # df.to_csv(f"sub_seventeen_runners{timestamp}.csv")
    # print(pk.get_runners_with_most_events())

    # name = 'Australia'
    # count = country.Country(name)
    # print(f"country url: {count.url}")
    # print(count.get_first_finishers())

    # count = 'Australia'
    # loc = 'parkville'
    # location = lc.Location(count, loc)
    # # print(location.url)
    # print(location.get_latest_results())



if __name__ == '__main__':
    main()