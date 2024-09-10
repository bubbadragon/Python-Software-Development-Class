"""
Description: This script loads a CSV file into a pandas DataFrame, processes the data
through various actions (describe, head, plot), and saves the data in different formats
(CSV, JSON, or Excel) depending on the user's choice.
"""
import pandas as pd
    
class DataFetcher:
    def __init__(self, file_path):
        '''
        Initialize the DataFetcher object with the file path
        
        Parameters:
        file_path (str): The path to the file.
        '''
        self.file_path = file_path
        
    def import_data(self):
        '''
        Loads a file into a pandas DataFrame.

        Returns:
        DataFrame: A DataFrame containing the data from weather file 
        '''
        try:
            df = pd.read_csv(self.file_path)
            print("Data successfully loaded")
            return df
        except FileNotFoundError:
            print("File not found")
            return None

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
                    self.data.to_csv(file_path, index=False)
                    print("Data saved to CSV file")
                elif file_type == 'json':
                    self.data.to_json(file_path)
                    print("Data saved to JSON file")
                elif file_type == 'excel':
                    self.data.to_excel(file_path, index=False)
                    print("Data saved to Excel file")
                else:
                    print("Invalid file format")
            except Exception as e:
                print(f"Error saving data: {e}")
        else:
            print("No data available to save.")
