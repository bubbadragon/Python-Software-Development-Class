from see_data.see_pandas import *


if __name__ == "__main__":
    # Step 1: Load the data
    fetcher = DataFetcher("weather_data/Weather Training Data.csv")
    data = fetcher.import_data()

    # Step 2: Process the data
    processor = DataProcessor(data)
    print(processor.process_data("describe"))  # Describes the data
    print(processor.process_data("head"))      # Displays first 5 rows

    # Step 3: Save the data
    storage = DataStorage(data)
    storage.save_data("output.csv")            # Saves as CSV
