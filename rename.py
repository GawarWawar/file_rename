import json
import os
import zipfile
import pathlib
import pandas as pd
from typing import Any
import warnings


def get_config() -> dict[str, Any]:
    """Read config.json into a dictionary.

    Config file should contain:
    - start_mode (int|float):
        - 1: Standard mode. Read ids from the directory where script is; look for the folder with images; copy images with new names into result zip that will be located into result folder.
        - 2: Advanced mode. Read directory with directories; in each child directory look for the ids file; perform separate rename_directory on each directory; resulting zips will be located in the result directory.
        - 2.1: Advanced mode (different save location). Read directory with directories; in each directory look for the ids file; perform separate rename_directory on each directory; resulting zips will be located in the same folders as photos are processed.
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
    
def rename_directory(
    file_pathes: list[pathlib.Path], 
    ids_df: pd.DataFrame,
    custom_zip_path: pathlib.Path|None = None,
    custom_zip_name: str|None = None,
) -> None:
    """Find all files in path_to_directory and tries to compress them into zip. Process only images in png format with a new name.
    New name will contain id: from ids DF; part_code: image should have a name which is composed of that part code; and file extension - .png.
    So images will have a name as: id.part_code.png

    Args:
        files (list[pathlib.Path]): List of all files in the directory represented as pathlib.Path
        name_of_file_with_ids (str): Name of file with ids
        custom_zip_path (pathlib.Path | None, optional): Set in which location zip file will be created. Defaults to None and zip will be located at result folder.
        custom_zip_name (str | None, optional): Set which name will have zip file after creation. Be careful specifing absolute pass. It will change zip location too. Defaults to None and zip name will be zip_path.name.
    """        
    
    # For every id we create a copy of each part
    if custom_zip_path is None:
        custom_zip_path = pathlib.Path("result/")

    if custom_zip_name is None:
        custom_zip_name = custom_zip_path.name
    
    with zipfile.ZipFile(pathlib.Path(custom_zip_path, f"{custom_zip_name}.zip"), "a") as myzip:  
        for id in ids_df.iloc[:, 0]:
            for path in file_pathes:
                # Process only .png image. 
                    # Each image should have part_code as a name;
                    # It will be used as a part of new name.
                part_code = path.name.removesuffix(".png")
                if len(path.name) - len(part_code) > 0:
                    try:
                        # Insert copy of the file with a new name in the zip
                        myzip.write(path, f"{id}.{part_code}.png")
                        # Log which file was added to zip.
                        print(f"'{id}.{part_code}.png' added to {myzip.filename}")
                    
                    except PermissionError:
                        print("Operation not permitted.")
                else:
                    # Log which file was not an image.
                    print(f"{path.name} is not an png image.")

def main():
    config = get_config()
    if config["start_mode"] == 1:
        # Standard mode. Read ids from the directory where script is; look for the folder with images; 
            # copy images with new names into result zip that will be located into result folder.

        ids_df = get_ids(config["name_of_file_with_ids"])
        file_pathes = get_directory(config["path_to_folder"], get_all=False)
        rename_directory(
            file_pathes,
            ids_df
        )
    elif config["start_mode"] >= 2:
        # Advanced mode. Read directory with directories; in each child directory look for the ids file; 
            # perform separate rename_directory on each directory; resulting zips will be located in the result directory.
        
        high_directory = get_directory(config["path_to_folder"])
        for item in high_directory:
            if item.is_dir():
                try:
                    ids_df = get_ids(pathlib.Path(item, config["name_of_file_with_ids"]))
                except FileNotFoundError:
                    print(f"{item} is a directory. How ever it does not contain file with {config["name_of_file_with_ids"]}")
                else:
                    file_pathes = get_directory(item, get_all=False)
                    
                    zip_save_location = None
                    if config["start_mode"] >= 2.1:
                        #-Advanced mode (different save location). Resulting zips will be located in the same folders as photos are processed.
                        
                        zip_save_location = file_pathes[0].parent
                        
                    rename_directory(
                        file_pathes,
                        ids_df,
                        custom_zip_path=zip_save_location,
                        custom_zip_name=file_pathes[0].parent.name
                    )   
            else:
                print(f"{item} is not a directory. SKIP")
     
    
                
if __name__ == "__main__":
    main()