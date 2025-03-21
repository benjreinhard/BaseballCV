import pytest
import multiprocessing as mp
from unittest.mock import Mock
import requests
from baseballcv.functions import DataTools, LoadTools, BaseballSavVideoScraper, BaseballTools

@pytest.fixture(scope="session", autouse=True)
def setup_multiprocessing() -> None:
    """
    Ensures that the multiprocessing start method is set to 'spawn' for tests.
    """
    if mp.get_start_method(allow_none=True) != 'spawn':
        mp.set_start_method('spawn', force=True)
    
    return None
        
@pytest.fixture
def data_tools() -> DataTools:
    """
    Provides a DataTools instance for testing.

    Returns:
        DataTools: An instance of DataTools with max_workers set to 2.
    """
    return DataTools(max_workers=2)

@pytest.fixture
def load_tools() -> LoadTools:
    """
    Provides a LoadTools instance for testing.

    Returns:
        LoadTools: An instance of LoadTools.
    """
    return LoadTools()

@pytest.fixture
def scraper() -> BaseballSavVideoScraper:
    """
    Provides a BaseballSavVideoScraper instance for testing.

    Returns:
        BaseballSavVideoScraper: An instance of BaseballSavVideoScraper.
    """
    return BaseballSavVideoScraper()

@pytest.fixture
def baseball_tools() -> BaseballTools:
    """
    Provides a BaseballTools instance for testing.

    Returns:
        BaseballTools: An instance of BaseballTools.
    """
    return BaseballTools()

@pytest.fixture
def mock_responses() -> tuple:
    """
    Creates both success and error mock responses.

    Returns:
        tuple: A tuple containing the success and error mock responses.
    """
    # Create success response
    success = Mock()
    success.status_code = 200
    success.content = b"mock file content"
    success.headers = {"Content-Disposition": "attachment; filename=model.pt"}
    success.raise_for_status.return_value = None  

    # Create error response
    error = Mock()
    error.status_code = 404
    error.json.return_value = {"error": "File not found"}
    http_error = requests.exceptions.HTTPError("404 Client Error: Not Found")
    http_error.response = error  
    error.raise_for_status.side_effect = http_error  

    return success, error

