import json
import os
import zipfile
import pathlib
import pandas as pd
from PIL import Image, UnidentifiedImageError
import warnings

def get_config() -> dict[str]:
    """Read config.json into dictionary
    Config file contain: \n
        - starting mode of the program:
            - 0 - standart mode. Read ids from the same directory; look for the folder with images; copy images with new names into result folder.
        - name of csv file with all ids (name_of_file_with_ids)
        - full Path to folder in which program will be performing actions (path_to_folder_with_pictures)

    Returns:
        dict[str]: Return dict with configuration
    """
     
    with open("config.json") as file_config:
        return json.load(file_config)
    
    
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
        custom_zip_name (str | None, optional): Set which name will have zip file after creation. Defaults to None and zip name will be zip_path.name.
    """        
    
    # For every id we create a copy of each part
    if custom_zip_path is None:
        zip_path = pathlib.Path("result/")
    else:
        zip_path = custom_zip_path
    if custom_zip_name is None:
        zip_name = zip_path.name
    else:
        zip_name = custom_zip_name
    
    with zipfile.ZipFile(pathlib.Path(zip_path, f"{zip_name}.zip"), "a") as myzip:  
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
    if config["start_mode"] == 0:
        # Standart mode: read ids from the same directory; look for the folder with images; copy images with new names into result folder.
        ids_df = get_ids(config["name_of_file_with_ids"])
        file_pathes = get_directory(config["path_to_folder"], get_all=False)
        rename_directory(
            file_pathes,
            ids_df
        )
    elif config["start_mode"] >= 1:
        # Advanced mode: read directory with directories; in each directory look for the ids file; perform separate file rename on each directories.
        high_directory = get_directory(config["path_to_folder"])
        for item in high_directory:
            if item.is_dir():
                try:
                    ids_df = get_ids(pathlib.Path(item, config["name_of_file_with_ids"]))
                except FileNotFoundError:
                    print(f"{item} is a directory. How ever it does not contain file with {config["name_of_file_with_ids"]}")
                else:
                    file_pathes = get_directory(item, get_all=False)
                    rename_directory(
                        file_pathes,
                        ids_df,
                        custom_zip_name=file_pathes[0].parent.name
                    )   
     
    
                
if __name__ == "__main__":
    main()