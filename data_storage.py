import pandas as pd
from logger_setup import logger

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