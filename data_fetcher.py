import pandas as pd
from logger_setup import logger
from concurrent.futures import ThreadPoolExecutor

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
        self.chunk_size = 1000
        
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
            if self.chunk_size:
                logger.info(f"Loading data from {self.file_path} in chunks of {self.chunk_size} rows.")
                chunks = pd.read_csv(self.file_path, chunksize=self.chunk_size)
                self.data = pd.concat(chunks, ignore_index=True)
            else:
                logger.info(f"Loading data from {self.file_path}.")
                self.data = pd.read_csv(self.file_path)
            logger.info("Data successfully loaded from %s", self.file_path)
        except Exception as e:
            logger.error("Error loading data from %s: %s", self.file_path, e)
            self.data = None
        return self.data

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
        
    @staticmethod
    def load_multiple_files(file_paths):
        '''
        Load multiple files concurrently using ThreadPoolExecutor.

        :param file_paths: List of file paths to load
        :param chunk_size: Number of rows to read per chunk (for large datasets)
        :return: List of DataFetcher instances with loaded data
        '''
        def load_file(path):
            fetcher = DataFetcher(path)
            fetcher.import_data()
            return fetcher

        fetchers = []
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(load_file, path) for path in file_paths]
            for future in futures:
                try:
                    fetchers.append(future.result())
                except Exception as e:
                    logger.error("Error occurred while loading file: %s", e)
        return fetchers
