import json
import os
import pathlib
import pandas as pd
from PIL import Image, UnidentifiedImageError
import warnings

def get_config() -> dict[str]:
    """Read config.json into dictionary
    Config file contain: 
        - name of csv file with all ids (name_of_file_with_ids)
        - full Path to folder with picrutes (path_to_folder_with_pictures)

    Returns:
        dict[str]: Return dict with configuration
    """
     
    with open("config.json") as file_config:
        return json.load(file_config)
    
def rename_directory(
    path_to_directory: str, 
    name_of_file_with_ids: str
) -> None:
    """Find all files in path_to_directory and tries to copy them as images in png format

    Args:
        path_to_directory (str): Absolute path to the directory
        name_of_file_with_ids (str): Name of file with ids
    """
    # Find all files in config["folder_with_pictures"]
    files = [f for f in pathlib.Path(path_to_directory).iterdir() if f.is_file()]

    # Make a list of ids from config["file_with_ids"]
    ids = pd.read_csv(name_of_file_with_ids)
    # ASIN - column with all off ids. Only this column matter
        # CSV can contain other columns and it wont affect the process 
        
    # For every id we create a copy of each part
    for id in ids.iloc[0]:
        for file in files:
            # Each image should have a part code as a name 
            part_code = file.name.removesuffix(".png")
            
            try:
                # Crate copy of the image with a new name
                with Image.open(file, "r") as img:
                    img.save(f"result/{id}.{part_code}.png")
                    print(f"{id}.{part_code}.png")
            except UnidentifiedImageError:
                # Make a warning if file was not an image
                warnings.warn(f"{file.name} was not an image")

def main():
    config = get_config()
    rename_directory(
        config["path_to_folder_with_pictures"],
        config["name_of_file_with_ids"]
    )
     
    
                
if __name__ == "__main__":
    main()