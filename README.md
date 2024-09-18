# Python Programming Semester Project 

## Introduction
This project focuses on data handling using Python, including reading, processing, and saving a dataset using Object-Oriented Programming (OOP) principles. The script is designed to load weather data from a CSV file, process it by performing various operations, and save the processed data in different formats.

## Dataset
The dataset used for this project is the Weather Data from Kaggle, which includes a synthetic dataset that explores weather patterns and predictions across 10 locations.

## Setup
To run this project, you need to have Python and the following packages installed:
- pandas
- matplotlib

## File Structure
- see_pandas.py: This is the main script that handles data loading, processing, and saving using OOP principles.
- weather_data: The weather dataset used for this project.
- README.md: Documentation
- load_data.html: Automatically generated documentation for the project code.

## Usage
To load, process, and save the dataset, follow these steps:

1. **Load Data**:
   The `DataFetcher` class is responsible for loading the weather data from a CSV file. You can adjust the file path in the script to point to your data source.

2. **Process Data**:
   The `DataProcessor` class allows you to describe the dataset, show the first few rows, or generate visualizations.

3. **Save Data**:
   The `DataStorage` class saves the processed data to CSV, JSON, or Excel formats.


# MODULE UPDATES

## MOD 1 - Optimal Python Development Lifecycle
Refactored the code to load a CSV file into a `pandas` DataFrame and provided descriptive statistics (using `describe()`) as part of the data processing. 

## MOD 2 - Modularization
Followed best practices for structuring the code. Built and published this package to TestPyPI. Installed and used the package to load, process, and save data, mimicking official Python library usage.

## MOD 3 - Advanced OOP
Refactored the application using advanced OOP principles by creating three classes: `DataFetcher` for loading and iterating through the data, `DataProcessor` for performing actions like describe or head, and `DataStorage` for saving the processed data into different formats such as CSV, JSON, or Excel. Each class had a clear responsibility, and class methods were designed to encapsulate functionality such as loading data, iterating through rows, processing actions like describe(), and saving data to different formats.

## MOD 4 - Generators, Iterators, and Logging
Refactored the code to include generators and iterators for efficient data fetching and processing. Implemented a `fetch_data_generator()` method in the `DataFetcher` class to yield rows one at a time. Added robust error handling for file operations in the `import_data()` method and used logging (`logger_setup`) to log critical events such as data loading, file errors, and general exceptions. Enhanced the application with proper file handling and logging of actions for better traceability and debugging.