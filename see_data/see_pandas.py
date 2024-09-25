"""
Description: This script loads a CSV file into a pandas DataFrame, processes the data
through various actions (describe, head, plot), and saves the data in different formats
(CSV, JSON, or Excel) depending on the user's choice.
"""
import pandas as pd
from logger_setup import *
    
class DataFetcher:
    """
    A class used to fetch data from a file and process it
    """
    def __init__(self, file_path):
        '''
        Initialize the DataFetcher object with the file path
        '''
        self.file_path = file_path
        self.data = None
        self.current_index = 0
        
    def __iter__(self):
        '''
        Makes the DataFetcher object iterable
        '''
        self.current_index = 0
        return self
    
    def __next__(self):
        '''
        Returns the next row of data
        '''
        if self.data is not None and self.current_index < len(self.data):
            row = self.data.iloc[self.current_index]
            self.current_index += 1
            return row
        else:
            raise StopIteration
        
        return self
        
    def import_data(self):
        '''
        Loads a file into a pandas DataFrame.
        '''
        try:
            self.data = pd.read_csv(self.file_path)
            logger.info("Data successfully loaded from %s", self.file_path)
            return self.data
        except FileNotFoundError:
            logger.error("Error - File not found: %s", self.file_path)
            return None
        except pd.errors.EmptyDataError:
            logger.error("Error - The file %s is empty", self.file_path)
            return None
        except pd.errors.ParserError:
            logger.error("Error - Error parsing the file: %s", self.file_path)
            return None
        except Exception as e:
            logger.error("Error - An unexpected error occured: %s", e)
            return None

    def fetch_data_generator(self):
        '''
        Generator function to yield data one row at a time
        '''
        if self.data is not None:
            for index, row in self.data.iterrows():
                yield row # Yield = generator
        else:
            raise ValueError("No data to fetch")

    def process_and_fetch(self):
        '''
        Process the data and fetch it one row at a time 
        '''
        # Check if data is loaded and print first row
        self.import_data()
        if self.data is not None:
            logger.info("Data has been loaded and is ready for processing.")

            # Print the first row
            for row in self.fetch_data_generator():
                return row
        else:
            logger.error("No data available to process.")
            return None

class DataProcessor:
    """
    A class used to process data in a DataFrame
    """
    def __init__(self, data):
        '''
        Initialize the DataProcessor object with the data
        '''
        self.data = data
        
    def process_data(self, action="describe"):
        '''
        Processes the data by performing a specific action.
        '''
        if self.data is not None:
            if action == "describe":
                return self.data.describe()
            elif action == "head":
                return self.data.head()
            elif action == "plot":
                self.data.plot()
            else:
                logger.error("Invalid action: %s", action)
        else:
            logger.error("No data available to process.")
        return None
            
class DataStorage:
    """
    A class to save data from a DataFrame to various file formats (CSV, JSON, Excel)
    """
    def __init__(self, data):
        '''
        Initialize the DataStorage object with the data
        '''
        self.data = data
        
    def save_data(self, file_path, file_type='csv'):
        '''
        Saves the data in the DataFrame to a file.
        '''
        if self.data is not None:
            if file_type == 'csv':
                try:
                    self.data.to_csv(file_path, index=False)
                except Exception as e:
                    logger.error("Error saving data: %s", e)
            elif file_type == 'json':
                try:
                    self.data.to_json(file_path)
                except Exception as e:
                    logger.error("Error saving data: %s", e)
            elif file_type == 'excel':
                try:
                    with pd.ExcelWriter(file_path, engine='xlsxwriter') as writer:
                        self.data.to_excel(writer, index=False)
                except Exception as e:
                    logger.error("Error saving data: %s", e)
            else:
                logger.error("Invalid file type: %s", file_type)
                raise ValueError(f"Invalid file type: {file_type}")
            logger.info("Data successfully saved to %s", file_path)
        else:
            logger.error("No data available to save.")
