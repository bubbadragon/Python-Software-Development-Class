from logger_setup import logger

class DataStorage:
    """
    A class to save data from a Spark DataFrame to various file formats (CSV, JSON)
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
            try:
                if file_type == 'csv':
                    self.data.write.mode("overwrite").csv(file_path, header=True)
                elif file_type == 'json':
                    self.data.write.mode("overwrite").json(file_path)
                elif file_type == 'excel':
                    # Convert to Pandas for Excel format
                    pd_data = self.data.toPandas()
                    pd_data.to_excel(file_path, index=False)
                else:
                    logger.error(f"Unsupported file type: {file_type}")
                logger.info(f"Data successfully saved as {file_type} to {file_path}")
            except Exception as e:
                logger.error("Error saving data: %s", e)
        else:
            logger.error("No data available to save.")

    def save_multiple_formats(self, save_paths):
        """Saves data to multiple formats specified in save_paths."""
        for file_type, file_path in save_paths.items():
            self.save_data(file_path, file_type)