"""
Pytest tests for the see_pandas module.

Personal Use:
-> Run test with: PYTHONPATH=$(pwd) pytest --cov=see_data tests/ 
-> See what is missing with: PYTHONPATH=$(pwd) pytest --cov-report term-missing --cov=see_data tests/
"""
import pytest
import pandas as pd
from see_data.see_pandas import DataFetcher, DataProcessor, DataStorage

# Mock the DataFrame
mock_df = pd.DataFrame({
    "A": [1, 2, 3],
    "B": [4, 5, 6],
    "C": [7, 8, 9]
})

## DataFetcher Tests ##
def test_import_data(monkeypatch):
    """
    Test the import_data function of DataFetcher.
    """
    def mock_read_csv(file_path):
        return mock_df

    monkeypatch.setattr(pd, "read_csv", mock_read_csv)

    fetcher = DataFetcher("test.csv")
    data = fetcher.import_data()

    assert data.equals(mock_df)

def test_import_data_file_not_found(monkeypatch):
    """
    Test the import_data function of DataFetcher when the file is not found.
    """
    def mock_read_csv(file_path):
        raise FileNotFoundError

    monkeypatch.setattr(pd, "read_csv", mock_read_csv)

    fetcher = DataFetcher("non_existent.csv")
    data = fetcher.import_data()

    assert data is None

def test_import_data_empty_file(monkeypatch):
    """
    Test the import_data function of DataFetcher when the file is empty.
    """
    def mock_read_csv(file_path):
        raise pd.errors.EmptyDataError

    monkeypatch.setattr(pd, "read_csv", mock_read_csv)

    fetcher = DataFetcher("empty.csv")
    data = fetcher.import_data()

    assert data is None

def test_import_data_parser_error(monkeypatch):
    """
    Test the import_data function of DataFetcher when a parser error occurs.
    """
    def mock_read_csv(file_path):
        raise pd.errors.ParserError

    monkeypatch.setattr(pd, "read_csv", mock_read_csv)

    fetcher = DataFetcher("corrupt.csv")
    data = fetcher.import_data()

    assert data is None

def test_import_data_unexpected_error(monkeypatch):
    """
    Test the import_data function of DataFetcher when an unexpected error occurs.
    """
    def mock_read_csv(file_path):
        raise Exception("Unexpected error")

    monkeypatch.setattr(pd, "read_csv", mock_read_csv)

    fetcher = DataFetcher("error.csv")
    data = fetcher.import_data()

    assert data is None

def test_fetch_data_generator():
    """
    Test the fetch_data_generator function of DataFetcher.
    """
    fetcher = DataFetcher("test.csv")
    fetcher.data = mock_df

    gen = fetcher.fetch_data_generator()
    row = list(gen)

    assert len(row) == 3
    assert row[0]["A"] == 1

def test_datafetcher_iter():
    """
    Test that DataFetcher is iterable and __iter__ resets the index.
    """
    fetcher = DataFetcher("test.csv")
    fetcher.data = mock_df  # Use a mock DataFrame

    iter_obj = iter(fetcher)  # Calls __iter__() implicitly

    # Assert that the current_index is reset to 0 and the returned object is the DataFetcher instance itself
    assert fetcher.current_index == 0
    assert iter_obj is fetcher  # Ensure __iter__ returns self

def test_datafetcher_next():
    """
    Test that DataFetcher returns the next row of data and raises StopIteration when done.
    """
    fetcher = DataFetcher("test.csv")
    fetcher.data = mock_df  # Use a mock DataFrame

    # First call to next() should return the first row
    row = next(fetcher)
    assert row["A"] == 1  # First row, first column value should be 1
    assert fetcher.current_index == 1  # Ensure current_index has incremented

    # Second call to next() should return the second row
    row = next(fetcher)
    assert row["A"] == 2  # Second row, first column value should be 2
    assert fetcher.current_index == 2  # Ensure current_index has incremented again

    # Exhaust all rows and ensure StopIteration is raised at the end
    next(fetcher)  # Third row
    with pytest.raises(StopIteration):
        next(fetcher)  # Should raise StopIteration after the last row

def test_fetch_data_generator_empty_data():
    """
    Test the fetch_data_generator function of DataFetcher when the data is empty.
    """
    fetcher = DataFetcher("test.csv")
    fetcher.data = pd.DataFrame()

    gen = fetcher.fetch_data_generator()
    row = list(gen)

    assert len(row) == 0

def test_fetch_data_generator_no_data():
    """
    Test the fetch_data_generator function of DataFetcher when no data is fetched.
    """
    fetcher = DataFetcher("test.csv")

    with pytest.raises(ValueError, match="No data to fetch"):
        list(fetcher.fetch_data_generator())

def test_process_and_fetch(monkeypatch):
    """
    Test the process_and_fetch function of DataFetcher.
    """
    def mock_read_csv(file_path):
        return mock_df

    monkeypatch.setattr(pd, "read_csv", mock_read_csv)

    fetcher = DataFetcher("test.csv")
    row = fetcher.process_and_fetch()

    assert row["A"] == 1

def test_process_and_fetch_no_data(monkeypatch):
    """
    Test the process_and_fetch function of DataFetcher when no data is fetched.
    """
    def mock_read_csv(file_path):
        raise FileNotFoundError

    monkeypatch.setattr(pd, "read_csv", mock_read_csv)
    fetcher = DataFetcher("test.csv")
    row = fetcher.process_and_fetch()

    assert row is None

## DataProcessor Tests ##
def test_process_data():
    """
    Test the process_data function of DataProcessor.
    """
    processor = DataProcessor(mock_df)
    result = processor.process_data("describe")

    assert isinstance(result, pd.DataFrame)

def test_process_data_head():
    """
    Test the process_data function with the "head" action.
    """
    processor = DataProcessor(mock_df)
    result = processor.process_data("head")

    assert len(result) == 3

def test_process_data_plot(monkeypatch):
    """
    Test the process_data function with the "plot" action.
    """
    # Mock the plot method to accept any arguments
    def mock_plot(*args, **kwargs):
        pass  # Do nothing when plot is called

    monkeypatch.setattr(pd.DataFrame, "plot", mock_plot)

    processor = DataProcessor(mock_df)
    result = processor.process_data("plot")

    assert result is None  # Plot returns None, so check if the method completes

def test_process_data_invalid_action():
    """
    Test the process_data function with an invalid action.
    """
    processor = DataProcessor(mock_df)
    result = processor.process_data("invalid_action")

    assert result is None

def test_process_data_no_data_logging(caplog):
    """
    Test the process_data function when data is None and ensure logging is done.
    """
    processor = DataProcessor(None)  # No data available

    # Capture the log output for no data case
    with caplog.at_level("ERROR"):
        result = processor.process_data("describe")

    assert result is None
    assert "No data available to process." in caplog.text  # Check that the error was logged


## DataStorage Tests ##
def test_save_data_csv(monkeypatch):
    """
    Test the save_data function of DataStorage with CSV format.
    """
    def mock_to_csv(file_path, index):
        pass

    monkeypatch.setattr(pd.DataFrame, "to_csv", mock_to_csv)

    storage = DataStorage(mock_df)
    storage.save_data("test.csv")

    assert True  # Ensure no errors

def test_save_data_json(monkeypatch):
    """
    Test the save_data function of DataStorage with JSON format.
    """
    def mock_to_json(file_path):
        pass

    monkeypatch.setattr(pd.DataFrame, "to_json", mock_to_json)

    storage = DataStorage(mock_df)
    storage.save_data("test.json", file_type="json")

    assert True  # Ensure no errors

def test_save_data_excel(monkeypatch):
    """
    Test the save_data function of DataStorage with Excel format.
    """
    def mock_to_excel(writer, index):
        pass

    class MockExcelWriter:
        """
        A mock class for ExcelWriter.
        """
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            pass

    monkeypatch.setattr(pd, "ExcelWriter", lambda *args, **kwargs: MockExcelWriter())

    storage = DataStorage(mock_df)
    storage.save_data("test.xlsx", file_type="excel")

    assert True  # Ensure no errors

def test_save_data_invalid_format():
    """
    Test the save_data function of DataStorage with an invalid format.
    """
    storage = DataStorage(mock_df)

    with pytest.raises(ValueError, match="Invalid file type"):
        storage.save_data("test.txt", file_type="txt")

def test_save_data_no_data_logging(caplog):
    """
    Test the save_data function when no data is available and ensure logging is done.
    """
    storage = DataStorage(None)  # No data available

    # Capture the log output for no data case
    with caplog.at_level("ERROR"):
        storage.save_data("test.csv")  # Try to save with no data

    # Ensure that the logger recorded the correct error message
    assert "No data available to save." in caplog.text

