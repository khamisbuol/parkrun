import parkrun
import country
import location as lc


def main():

    # print(countries_dict['USA']['info'])
    # pk = parkrun.Parkrun()
    # df = pk.get_largest_clubs()
    # print(df)
    # df.to_csv("top_age_category.csv")
    # print(pk.get_runners_with_most_events())

    # name = 'Australia'
    # count = country.Country(name)
    # print(f"country url: {count.url}")
    # print(count.get_first_finishers())

    count = 'Australia'
    loc = 'parkville'
    location = lc.Location(count, loc)
    # print(location.url)
    print(location.get_latest_results())



if __name__ == '__main__':
    main()