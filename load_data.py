"""
This script loads a CSV file into a pandas DataFrame, processes the data, 
and saves the data in different formats
"""
from data_fetcher import DataFetcher
from data_visual import DataVisualizer
from data_storage import DataStorage
from logger_setup import logger


if __name__ == "__main__":
    # Step 0: Start the logger
    logger.info("Starting the data processing workflow...")
   
    # Step 1: Load the data
    fetcher = DataFetcher("weather_data/Weather Training Data.csv")
    data = fetcher.import_data()
    fetcher.process_and_fetch()

    # Step 2: Ask the user whether to analyze a specific location or all data
    choice = input("Do you want to analyze a specific location or all data? Type 'location' or 'all': ").lower()

    if choice == 'location':
        location = input("Enter the location you want to analyze (e.g., Albury): ")
        # Filter the data for that location
        visual = DataVisualizer(data)
        location_data = visual.filter_data(location=location)

        if location_data is None or location_data.empty:
            print(f"No data found for location: {location}. Exiting the workflow.")
            logger.info(f"No data found for location: {location}. Workflow ended.")
            exit()  # Exit if no data is found for the location

        # Update the visualizer to work with the filtered location data
        visual = DataVisualizer(location_data)

    elif choice == 'all':
        # Use the entire dataset
        visual = DataVisualizer(data)
        LOCATION = None
        print("You are analyzing the entire dataset.")

    else:
        print("Invalid choice. Please start over and choose either 'location' or 'all'.")
        exit()

    # Step 3: Allow the user to perform actions on the filtered data or the full dataset
    while True:
        action = input("Enter the action you want to perform (describe, head, plot, filter, convert, sum) or type 'q' to quit: ").lower()

        if action == 'q':
            print("Exiting the data processing workflow.")
            logger.info("Data processing workflow ended by user.")
            break

        # Handling 'describe' and 'head' actions
        if action == 'describe' or action == 'head':
            result = visual.visualize_data(action=action)
            if result is not None:
                print(result)

        # Handling the 'plot' action
        elif action == 'plot':
            column = input("Enter the column to plot (e.g., MaxTemp, Rainfall): ")

            # Only ask for location if the user is analyzing the entire dataset
            if choice == 'all':
                location = input("Enter the location to plot (e.g., Albury): ")

            # Call the plot function with the provided column and location
            visual.visualize_data(action=action, column=column, location=location)

        # Handling the 'filter' action
        elif action == 'filter':
            column = input("Enter the column to filter (e.g., MaxTemp, Rainfall): ")
            result = visual.filter_data(column=column)
            if result is not None:
                print(result)

        # Handling the 'convert' action (for unit conversion)
        elif action == 'convert':
            column = input("Enter the column to convert (e.g., MaxTemp for Celsius to Fahrenheit conversion): ")
            result = visual.visualize_data(action=action, column=column)
            if result is not None:
                print(result)

        # Handling the 'sum' action (for summing up a column, e.g., total rainfall)
        elif action == 'sum':
            column = input("Enter the column to reduce (e.g., Rainfall to sum it up): ")
            result = visual.visualize_data(action=action, column=column)
            if result is not None:
                print(f"Total {column}: {result}")

        # Invalid action handling
        else:
            print(f"Invalid action: {action}. Please try again.")

    # Step 2: Save the data
    storage = DataStorage(data)
    storage.save_data("output.csv")            # Saves as CSV   
    logger.info("Data processing completed.")
    
    