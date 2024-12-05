import json
import pathlib
import pandas as pd
from typing import Any

def get_config() -> dict[str, Any]:
    """Read config.json into a dictionary.

    Config file should contain:
    - start_mode (int|float):
        - 1: Standard mode. Read ids from the directory where script is; look for the folder with images; copy images with new names into result zip that will be located into result folder.
        - 2: Advanced mode. Read directory with directories; in each child directory look for the ids file; perform separate rename_and_zip_photos_in_directory on each directory; resulting zips will be located in the result directory.
        - 2.1: Advanced mode (different save location). Read directory with directories; in each directory look for the ids file; perform separate rename_and_zip_photos_in_directory on each directory; resulting zips will be located in the same folders as photos are processed.
    - name_of_file_with_ids (str): Name of the CSV file with all IDs.
    - path_to_folder (str): Full path to the folder for program actions.

    Returns:
        Dict[str, Any]: Dictionary with configuration settings.
    Raises:
        FileNotFoundError: If config.json is missing.
        KeyError: If required keys are missing.
        ValueError: If any configuration value is invalid.
    """
    try:
        with open("config.json") as file_config:
            config:dict[str, Any] = json.load(file_config)
        
        # Validate required keys
        required_keys = {"start_mode", "name_of_file_with_ids", "path_to_folder"}
        missing_keys = required_keys - set(config.keys())
        if missing_keys:
            raise KeyError(f"Missing required configuration keys: {missing_keys}")
        
        return config
    except FileNotFoundError:
        raise FileNotFoundError("The config.json file is missing.")
    except json.JSONDecodeError:
        raise ValueError("The config.json file contains invalid JSON.")
    
    
def get_ids(name_of_csv_with_ids: str) -> pd.DataFrame:
    """Make a list of ids from presented path to csv file.
    Column at 0 position - should be a column with all off ids. Only this column matter.
        CSV can contain other columns and it wont affect the process.

    Args:
        name_of_csv_with_ids (str): CSV file with ids of products

    Returns:
        pd.DataFrame: DF with ids
    """
    return pd.read_csv(name_of_csv_with_ids)
    
def get_directory(path_to_directory: str, get_all: bool = True) -> list[pathlib.Path]:
    """Get all items in the specified directory

    Args:
        path_to_directory (str): Absolute path to the directory

    Returns:
        list[pathlib.Path]: List of all files in the directory represented as pathlib.Path
    """
    # Find all files in path_to_directory
    return [
        file 
        for file in pathlib.Path(path_to_directory).iterdir() 
        if file.is_file() or get_all
    ]