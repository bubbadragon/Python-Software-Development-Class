"""
Description: This script loads a CSV file into a pandas DataFrame.
"""


import pandas as pd


def load_data(file_path):
    """
    Loads a CSV file into a pandas DataFrame.

    Parameters:
    file_path (str): The path to the CSV file.

    Returns:
    DataFrame: A DataFrame containing the data from weather file 

    """
    try:
        df = pd.read_csv(file_path)
        print("Data succesfully loaded")
        return df
    except FileNotFoundError:
        print("File not found")
        return None


data = load_data('weather_data.csv')

if data is not None:
    print(data.head())
