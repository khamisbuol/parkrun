import parkrun
import country


def main():

    # print(countries_dict['USA']['info'])
    # pk = parkrun.Parkrun()
    # df = pk.get_freedom_finishers()
    # print(df)
    # df.to_csv("top_age_category.csv")
    # print(pk.get_runners_with_most_events())

    name = 'united kingdom'
    count = country.Country(name)
    # print(count.url)

    print(count.get_attendance_records())


if __name__ == '__main__':
    main()