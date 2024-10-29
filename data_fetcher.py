from pyspark.sql import SparkSession
from logger_setup import logger

class DataFetcher:
    """
    A class used to fetch data from a file and process it
    """
    def __init__(self, file_path=None):
        '''
        Initialize the DataFetcher object with the file path
        '''
        self.file_path = file_path
        self.data = None
        self.spark = SparkSession.builder.appName("DataFetcher").getOrCreate()

    def import_data(self, file_paths=None):
        '''
        Loads one or multiple files into a PySpark DataFrame.
        '''
        try:
            # Load files based on the presence of `file_paths` or `self.file_path`
            if file_paths:
                logger.info(f"Loading multiple files from {file_paths} with PySpark.")
                self.data = self.spark.read.csv(file_paths, header=True, inferSchema=True)
            else:
                logger.info(f"Loading data from {self.file_path} with PySpark.")
                self.data = self.spark.read.csv(self.file_path, header=True, inferSchema=True)
                
            logger.info("Data successfully loaded.")

        except Exception as e:
            logger.error("Error loading data: %s", e)
            self.data = None
        return self.data
   
    @classmethod
    def load_multiple_files(cls, file_paths):
        '''
        Class method to load multiple files into a single DataFetcher instance
        '''
        fetcher = cls()
        fetcher.import_data(file_paths=file_paths)
        return [fetcher]

    def apply_transformation(self, transformation_func):
        """Applies a user-defined transformation function to the data."""
        if self.data is not None:
            # Apply the user's transformation function
            self.data = transformation_func(self.data)
            return self.data
        else:
            raise ValueError("No data to transform")