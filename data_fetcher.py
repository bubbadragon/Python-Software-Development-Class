import pandas as pd
from logger_setup import logger

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
