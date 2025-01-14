# Python Programming Semester Project 

## Introduction
This project focuses on data handling using Python, including reading, processing, and saving a dataset using Object-Oriented Programming (OOP) principles. The script is designed to load weather data from a CSV file, process it by performing various operations, and save the processed data in different formats. Additionally, users can now predict whether it will rain tomorrow using a pre-trained machine learning model.

## Dataset
The dataset used for this project is the Weather Data from Kaggle, which includes a synthetic dataset that explores weather patterns and predictions across 10 locations.

## Setup
To run this project, you need to have Python and the following packages installed:
- pandas
- matplotlib
- pytest (for testing)
- pytest-cov (for coverage reporting)
- streamlit
- pyspark
- joblib
- numpy
- scikit-learn
- imbalanced-learn

## File Structure
- `see_data/see_pandas.py`: This is the main script that handles data loading, processing, and saving using OOP principles.
- `weather_data`: The weather dataset used for this project.
- `README.md`: Documentation
- `load_data.html`: Interactive Streamlit application for data visualization and prediction.
- `tests/`: Contains pytest test files for testing the functionality of `see_pandas.py`
- `ml.py`: Script for training the machine learning model.

## Usage
To load, process, and save the dataset, follow these steps:

1. **Load Data**:
   The `DataFetcher` class is responsible for loading the weather data from a CSV file. You can adjust the file path in the script to point to your data source.

2. **Process Data**:
   The `DataProcessor` class allows you to describe the dataset, show the first few rows, or generate visualizations.

3. **Save Data**:
   The `DataStorage` class saves the processed data to CSV, JSON, or Excel formats.

4. **Predict Rain**:
   The `DataStorage` Use a pre-trained machine learning model to predict whether it will rain tomorrow based on weather data.

# Interactive Streamlit App
The Streamlit application provides a user-friendly interface to visualize and analyze the dataset or predict rain.

## Main Page
- Select and analyze data for a specific location or all locations.
- Perform actions such as:
   - Describe dataset statistics.
   - Display the first few rows (head()).
   - Generate visualizations for selected columns.
   - Filter data based on column values.
- Save filtered or processed data in CSV, JSON, or Excel formats.

## Prediction Page
- Navigate to the prediction page via a sidebar button.
- Enter weather feature values to predict whether it will rain tomorrow.
- The prediction uses a pre-trained Random Forest model, ensuring accuracy and reliability.
- Displays the prediction result (Rain or No Rain) and associated probabilities.

# MODULE UPDATES

## MOD 1 - Optimal Python Development Lifecycle
Refactored the code to load a CSV file into a `pandas` DataFrame and provided descriptive statistics (using `describe()`) as part of the data processing. 

## MOD 2 - Modularization
Followed best practices for structuring the code. Built and published this package to TestPyPI. Installed and used the package to load, process, and save data, mimicking official Python library usage.

## MOD 3 - Advanced OOP
Refactored the application using advanced OOP principles by creating three classes: `DataFetcher` for loading and iterating through the data, `DataProcessor` for performing actions like describe or head, and `DataStorage` for saving the processed data into different formats such as CSV, JSON, or Excel. Each class had a clear responsibility, and class methods were designed to encapsulate functionality such as loading data, iterating through rows, processing actions like describe(), and saving data to different formats.

## MOD 4 - Generators, Iterators, and Logging
Refactored the code to include generators and iterators for efficient data fetching and processing. Implemented a `fetch_data_generator()` method in the `DataFetcher` class to yield rows one at a time. Added robust error handling for file operations in the `import_data()` method and used logging (`logger_setup`) to log critical events such as data loading, file errors, and general exceptions. Enhanced the application with proper file handling and logging of actions for better traceability and debugging.

## MOD 5 - Unit Testing
Enhanced the project with unit testing using pytest to ensure the reliability of key functionalities. Developed comprehensive test cases for the `DataFetcher`, `DataProcessor`, and `DataStorage` classes, covering both normal operations and edge cases. Implemented tests for critical actions such as data loading, processing, and saving, along with robust error handling scenarios. Incorporated pytest-cov to measure test coverage and ensure that all major components are thoroughly tested. This refactoring ensures that the application functions correctly across various use cases while maintaining high code quality and reliability.

## MOD 6 - Data Patterns, Trends, Visualize 
Refactored the code to allow users to analyze specific locations or the entire dataset. Added functionality to plot weather data (e.g., temperature, rainfall) over time, filter data by column values or location, and convert units from Celsius to Fahrenheit. Introduced a sum function to aggregate data (e.g., total rainfall) with handling for missing values. Enhanced the user experience with robust logging, tracking actions like data loading, filtering, plotting, conversions, and error handling, providing better traceability throughout the data analysis workflow.

## Mod 7 - Multithreading Concurrency
Refactored the code to load data concurrently from multiple files using the DataFetcher. `load_multiple_files()` method, leveraging `ThreadPoolExecutor` for improved data ingestion efficiency. Introduced chunked data loading with a default size of 1000 rows in DataFetcher to optimize memory usage when handling large datasets, allowing for smoother performance and preventing memory overload. Implemented data saving enhancements in the DataStorage class, with default CSV saving and an optional prompt for saving in additional formats (JSON, Excel) using the `save_multiple_formats()` method. Also optimized the `unit_conversion` and `sum_column` functions within `data_visual` to use `ProcessPoolExecutor` for improved speed.

## Mod 8 - PySpark Integration and Streamlit Interface Update
### PySpark Integration
Refactored the code to load data into a PySpark DataFrame using the `DataFetcher class`, leveraging PySpark’s distributed computing capabilities for improved scalability and memory efficiency. Adjusted data loading in `DataFetcher` to allow for multiple files to be ingested concurrently with `load_multiple_files()`, enhancing data ingestion and processing speed. For data analysis actions, we convert the PySpark DataFrame to a Pandas DataFrame when needed, ensuring compatibility with downstream operations and visualizations.
### Streamlit Interface 
Replaced command-line inputs with a fully interactive Streamlit interface. Users can:

+ **Choose Location Scope:** Select either a specific location or all locations as the initial scope for analysis.
+ **Perform Data Actions:** Conduct various data actions (e.g., `describe`, `head`, `plot`, and `filter`) on the selected dataset subset, with dynamic input  options through Streamlit widgets for each action.
+ **Plotting and Visualization:** Integrated st.pyplot() to render visualizations directly within Streamlit, making data insights easily accessible.
+ **Data Saving Options:** Included an option to save the final dataset in multiple formats (CSV, JSON, Excel) using the `DataStorage` class, ensuring that any filtered or transformed data can be exported as needed.

## Mod 9 - Rain Prediction and Enhanced Navigation
### Rain Prediction
Integrated a pre-trained Random Forest model with preprocessing capabilities to predict whether it will rain tomorrow based on user inputs. The prediction page features:
- Automatic handling of missing data.
- User-friendly input fields with default values prefilled based on training data.

### Enhanced Navigation
Refactored the Streamlit app to include:
- A sidebar navigation system with buttons to switch between the main analysis page and the prediction page.
- Clear separation between data visualization and prediction functionalities.
