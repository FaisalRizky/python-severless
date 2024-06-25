import logging
import os
import json
from os.path import dirname, abspath, join
from datetime import datetime

def setup_logger(filename):
    # Ensure the log directory exists
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    logging.basicConfig(
        filename=filename,  # Use the provided filename for the log file
        level=logging.DEBUG,  # Log level
        format='%(asctime)s %(levelname)s %(message)s',  # Log message format
        datefmt='%Y-%m-%d %H:%M:%S'  # Date format
    )
    logger = logging.getLogger()
    return logger

def write_response_from_scrap(data, calling_path):
    """
    Writes the scraped results to a file in the logger/calling_path/directory.json .
    The file is named based on the current date.
    """
    # Create the filename with the current date
    file_mock_data_path = get_path_logger(calling_path)

    # Ensure the directory exists
    directory = os.path.dirname(file_mock_data_path)
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    # Path to local HTML file in development environment
    file_path = os.path.join(file_mock_data_path)
    try:
         # Write the results to the JSON file, overwriting if it exists
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)
    except FileNotFoundError:
        print(f"Write File not found at {file_path}")
        return None
    except IOError as e:
        print(f"Error Writing file {file_path}: {e}")
        return None

def get_path_logger(calling_path):
    # Get the path of the current script file, this will use for mock data purpose
    current_dir = dirname(abspath(__file__))
    # Get Root Dir
    root_dir = os.path.dirname(current_dir)
    # Get Calling script Relative Path
    file_location = calling_path.replace(root_dir, "")
    file_location = file_location.replace(".py", "")

    # Join Final mock data location
    final_file_location = root_dir + "/logger" + file_location

    # Create the filename with the current date
    date_str = datetime.now().strftime("%Y-%m-%d")
    final_file_location = f"{final_file_location}_{date_str}.json"
    
    return final_file_location