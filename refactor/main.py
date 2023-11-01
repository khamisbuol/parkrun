import parkrun
import country


def main():

    # print(countries_dict['USA']['info'])
    pk = parkrun.Parkrun()
    df = pk.get_largest_clubs()
    print(df)
    # df.to_csv("top_age_category.csv")
    # print(pk.get_runners_with_most_events())

    name = 'Australia'
    count = country.Country(name)
    # print(f"country url: {count.url}")
    print(count.get_largest_clubs())


if __name__ == '__main__':
    main()