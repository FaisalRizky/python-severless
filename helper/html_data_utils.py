import os
from os.path import dirname, abspath, join
import requests
from dotenv import load_dotenv
# from helper.logger_utils import setup_logger

# Load environment variables from .env file
load_dotenv()

# Setup logger with a specific log file path in the log directory
# log_file_path = 'log/logger_utils.log'  # This will place the log file in the log directory
# logger = setup_logger(log_file_path)

def get_data_url(url=None, calling_path=None):
    """
    Retrieves HTML content either from a local file (development environment)
    or from a specified URL (production environment), based on the ENVIRONMENT
    variable set in the .env file.

    Parameters:
    - url (str, optional): URL to retrieve HTML content from in production mode.
    - calling_path (str, optional): Path relative to the project root in development mode,
      where the local HTML file is located.

    Returns:
    - str or None: HTML content as a string if successfully retrieved,
      None if any error occurs during retrieval.
    """
    # Determine the environment from the ENVIRONMENT variable, defaulting to "DEVELOPMENT"
    environment = os.getenv("ENVIRONMENT", "DEVELOPMENT").upper()
    
    if environment != "PRODUCTION":
        if not calling_path:
            print("No calling_path provided for development environment.")
            return None
        
        file_mock_data_path = get_path_mock_data(calling_path)

        # logger.info(f"Fetch data from: {file_mock_data_path}")
        
        # Path to local HTML file in development environment
        file_path = os.path.join(file_mock_data_path)

        try:
            # Open the local file and read its contents
            with open(file_path, 'r', encoding='utf-8') as file:
                html_content = file.read()
            return html_content
        except FileNotFoundError:
            print(f"File not found at {file_path}")
            return None
        except IOError as e:
            print(f"Error reading file {file_path}: {e}")
            return None
    else:
        if not url:
            print("No URL provided for production environment.")
            return None
        
        try:
            # Make a GET request to the URL
            response = requests.get(url)
            
            # Raise an exception for HTTP errors (4xx or 5xx)
            response.raise_for_status()
            
            # Retrieve and return the content of the response
            html_content = response.content
            return html_content
        except requests.exceptions.RequestException as e:
            # Handle request exceptions (e.g., network errors)
            print(f"Failed to retrieve content from {url}: {e}")
            return None


def get_path_mock_data(calling_path):
    # Get the path of the current script file, this will use for mock data purpose
    current_dir = dirname(abspath(__file__))
    # Get Root Dir
    root_dir = os.path.dirname(current_dir)
    # Get Calling script Relative Path
    file_location = calling_path.replace(root_dir, "")
    file_location = file_location.replace(".py", ".html")
    # Join Final mock data location
    final_file_location = root_dir + "/data" + file_location
    return final_file_location
