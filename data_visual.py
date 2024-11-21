import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from logger_setup import logger

class DataVisualizer:
    """A class to process and visualize weather data from a Pandas DataFrame."""

    def __init__(self, data):
        """
        Initialize the DataVisualizer with a PySpark or Pandas DataFrame.
        Converts to Pandas if it’s a Spark DataFrame.
        """
        try:
            # Only convert if data is a PySpark DataFrame
            if not isinstance(data, pd.DataFrame):
                self.data = data.toPandas()
                logger.info("Data successfully converted to Pandas DataFrame.")
            else:
                self.data = data
        except Exception as e:
            logger.error(f"Error converting data to Pandas DataFrame: {e}")
            self.data = None

    def plot_data(self, column, log_scale=False):
        """Helper function to plot data using Seaborn and Matplotlib, rendered with Streamlit."""
        plt.figure(figsize=(10, 6))
        sns.histplot(self.data[column], log_scale=log_scale)
        plt.title(f"Distribution of {column}")
        st.pyplot(plt)  # Render the plot in Streamlit

    def filter_data(self, column=None, comparison=None, threshold=None, location=None):
        """
        Filter the data either by a column value (with greater than, less than, or equal to) or by location.

        :param column: The column to filter (e.g., MaxTemp, Rainfall)
        :param comparison: The type of comparison ('greater', 'less', 'equal')
        :param threshold: The threshold value for filtering
        :param location: The location to filter (e.g., Albury)
        :return: Filtered DataFrame
        """
        if column and comparison and threshold is not None:
            try:
                threshold = float(threshold)
                if comparison == 'greater':
                    filtered_data = self.data[self.data[column] > threshold]
                elif comparison == 'less':
                    filtered_data = self.data[self.data[column] < threshold]
                elif comparison == 'equal':
                    filtered_data = self.data[self.data[column] == threshold]
                else:
                    logger.error(f"Invalid comparison type: {comparison}")
                    return None

                if filtered_data.empty:
                    logger.warning(f"No data matches the filter condition {column} {comparison} {threshold}.")
                    st.warning(f"No data matches the filter condition {column} {comparison} {threshold}.")
                    return None
                return filtered_data

            except ValueError:
                logger.error(f"Invalid threshold value for {column}.")
                st.error(f"Invalid input. Please enter a valid numeric threshold for {column}.")
                return None

        elif location:
            # Filter for a specific location if `location` is provided
            location_data = self.data[self.data['Location'] == location]
            if location_data.empty:
                logger.warning(f"No data found for location: {location}")
                st.warning(f"No data found for location: {location}")
                return None
            return location_data

        else:
            logger.warning("Please specify either a column and filter criteria or a location for filtering.")
            st.warning("Please specify either a column and filter criteria or a location for filtering.")
            return None

    def visualize_data(self, action="describe", column=None, log_scale=False):
        """
        Handles actions like 'describe' and 'head' based on the 'action' parameter.
        
        :param action: The action to perform (e.g., 'describe' or 'head').
        :param column: Optional column to focus on for actions like 'plot'.
        :param log_scale: Whether to apply log scale for plotting.
        :return: Result of the action or None.
        """
        if action == "describe":
            return self.data.describe()
        elif action == "head":
            return self.data.head()  # You can specify the number of rows in the calling function
        else:
            raise ValueError(f"Action '{action}' is not supported in visualize_data.")

