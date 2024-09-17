"""
Description: This script loads a CSV file into a pandas DataFrame, processes the data
through various actions (describe, head, plot), and saves the data in different formats
(CSV, JSON, or Excel) depending on the user's choice.
"""
import pandas as pd
from logger_setup import *
    
class DataFetcher:
    def __init__(self, file_path):
        '''
        Initialize the DataFetcher object with the file path
        
        Parameters:
        file_path (str): The path to the file.
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

        Returns:
        DataFrame: A DataFrame containing the data from weather file 
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
        print("Inside fetch_data_generator:")
        print("self.data:", self.data)  # Print self.data to check its content
        
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
            processor = DataProcessor(self.data)
            print("Data has been loaded and is ready for processing.")
            
            # Print the first row
            for row in self.fetch_data_generator():
                print(row)
                break
        else:
            print("Data failed to load.")

class DataProcessor:
    def __init__(self, data):
        '''
        Initialize the DataProcessor object with the data
        
        Parameters:
        data (DataFrame): The DataFrame containing the data.
        '''
        self.data = data
        
    def process_data(self, action="describe"):
        '''
        Processes the data by performing a specific action.

        Parameters:
        action (str): The action to perform on the data ('describe', 'head', 'plot').
        
        Returns:
        The result of the specified action.
        '''
        if self.data is not None:
            if action == "describe":
                return self.data.describe()
            elif action == "head":
                return self.data.head()
            elif action == "plot":
                self.data.plot()
            else:
                print(f"Unknown action: {action}")
        else:
            print("No data to process.")
            
class DataStorage:
    def __init__(self, data):
        '''
        Initialize the DataStorage object with the data
        
        Parameters:
        data (DataFrame): The DataFrame containing the data.
        '''
        self.data = data
        
    def save_data(self, file_path, file_type = 'csv'):
        '''
        Saves the data in the DataFrame to a CSV file.

        Parameters:
        file_path (str): The path to save the CSV file.
        file_format (str): The format to save the file in ('csv', 'json', or 'excel').
        '''
        if self.data is not None:
            try:
                if file_type == 'csv':
                    with open(file_path, 'w') as f:
                        self.data.to_csv(f, index=False)
                    print("Data saved to {file_path}")
                elif file_type == 'json':
                    with open(file_path, 'w') as f:
                        self.data.to_json(f)
                    print("Data saved to {file_path}")
                elif file_type == 'excel':
                    with pd.ExcelWriter(file_path, engine='xlsxwriter') as writer:
                        self.data.to_excel(writer, index=False)
                    print(f"Data saved to {file_path}")
                else:
                    print("Invalid file format")
            except Exception as e:
                print(f"Error saving data: {e}")
        else:
            print("No data available to save.")
