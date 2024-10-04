import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from functools import reduce
from logger_setup import logger

class DataVisualizer:
    """
    A class to process and visualize weather data from a DataFrame.
    The user can specify actions like 'describe', 'head', 'plot', 'filter', and more.
    """

    def __init__(self, data):
        """
        Initialize the WeatherDataProcessor with a pandas DataFrame.

        :param data: pandas DataFrame containing weather data
        """
        self.data = data
        logger.info("DataVisualizer initialized with data.")

    def visualize_data(self, action="describe", column=None, location=None):
        """
        Process and visualize the weather data based on the specified action.
        """
        
        logger.info(f"Performing action '{action}' with column '{column}' and location '{location}'.")
        
        actions = {
            "describe": self.data.describe,
            "head": self.data.head,
            "plot": lambda: self.plot_data(column, location),
            "filter": lambda: self.filter_data(column),
            "convert": lambda: self.unit_conversion(column),
            "sum": lambda: self.sum_column(column),
        }

        if action in actions:
            return actions[action]()
        else:
            print(f"Invalid action: {action}")
            logger.error(f"Invalid action specified: {action}")
            return None

    def plot_data(self, column, location):
        """
        Plot the data for a specific location using matplotlib or seaborn.

        :param column: The column to visualize (e.g., MaxTemp, Rainfall)
        :param location: The location to filter by (e.g., Albury)
        :return: None
        """
        if column and location:
            # Filter the data for the given location
            logger.info(f"Plotting '{column}' for location '{location}'.")
            location_data = self.data[self.data['Location'] == location]
            
            if location_data.empty:
                logger.warning(f"No data found for location: {location}")
                print(f"No data found for location: {location}")
                return
            
            plt.figure(figsize=(10, 6))
            sns.lineplot(data=location_data, x=location_data.index, y=location_data[column])
            plt.title(f"{column} Over Time for {location}")
            plt.xlabel("Index")
            plt.ylabel(column)
            plt.show()
        else:
            logger.warning("Please specify both a column and a location.")
            print("Please specify both a column and a location.")


    def filter_data(self, column=None, location=None):
        """
        Filter the data either by a column value (with greater than, less than, or equal to) or by location.

        :param column: The column to filter (e.g., MaxTemp, Rainfall)
        :param location: The location to filter (e.g., Albury)
        :return: Filtered DataFrame
        """
        if column:
            # Ask user to input the type of comparison they want (greater than, less than, or equal to)
            comparison = input("Enter comparison type (greater, less, equal): ").lower()
            threshold = input(f"Enter the threshold value for {column}: ")
            
            logger.info(f"Filtering '{column}' where values are '{comparison}' than {threshold}.")

            try:
                threshold = float(threshold)  # Convert the threshold to a numeric value

                if comparison == 'greater':
                    filtered_data = self.data[self.data[column] > threshold]
                elif comparison == 'less':
                    filtered_data = self.data[self.data[column] < threshold]
                elif comparison == 'equal':
                    filtered_data = self.data[self.data[column] == threshold]
                else:
                    logger.error(f"Invalid comparison type: {comparison}")
                    print(f"Invalid comparison type: {comparison}")
                    return None

                if filtered_data.empty:
                    logger.warning(f"No data matches the filter condition {column} {comparison} {threshold}.")
                    print(f"No data matches the filter condition {column} {comparison} {threshold}.")
                    return None
                return filtered_data

            except ValueError:
                logger.error(f"Invalid threshold value for {column}.")
                print(f"Invalid input. Please enter a valid numeric threshold for {column}.")

        elif location:
            # Filter for a specific location
            location_data = self.data[self.data['Location'] == location]
            if location_data.empty:
                logger.warning(f"No data found for location: {location}")
                print(f"No data found for location: {location}")
            return location_data

        else:
            logger.warning("Please specify either a column or a location for filtering.")
            print("Please specify either a column or a location for filtering.")
            return None


    def unit_conversion(self, column):
        """
        Map the data, applying a transformation to the specified column.
        Example: Convert temperature from Celsius to Fahrenheit.

        :param column: The column to apply the transformation (e.g., temperature)
        :return: Transformed DataFrame
        """
        if column:
            # Example: Convert temperature from Celsius to Fahrenheit
            try:
                logger.info(f"Converting '{column}' from Celsius to Fahrenheit.")
                self.data.loc[:, column] = self.data[column].map(lambda x: x * 9/5 + 32)
                return self.data[[column]]
            except KeyError:
                logger.error(f"Column '{column}' not found in the data.")
                print(f"Column '{column}' not found in the data.")
                return None
        else:
            logger.warning("No column specified for conversion.")
            print("No column specified for mapping.")


    def sum_column(self, column):
        """
        Use reduce to aggregate data. Example: Calculate total rainfall.
        
        :param column: The column to aggregate (e.g., rainfall)
        :return: Aggregated value (e.g., total rainfall)
        """
        if column:
            try:
                # Drop NaN values before reducing (summing) the data
                logger.info(f"Reducing column '{column}' to get total value.")
                total = reduce(lambda x, y: x + y, self.data[column].dropna())
                return total
            except KeyError:
                logger.error(f"Column '{column}' not found in the data.")
                print(f"Column '{column}' not found in the data.")
                return None
            except TypeError:
                logger.error(f"Column '{column}' contains non-numeric data.")
                print(f"Column '{column}' contains non-numeric data.")
                return None
        else:
            logger.warning("No column specified for reduction.")
            print("No column specified for reduction.")
            return None
