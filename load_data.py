from see_data.see_pandas import import_csv_data


if __name__ == "__main__":
    data = import_csv_data('weather_data/Weather Test Data.csv')

    if data is not None:
        # print(data.head())
        print(data.describe())
