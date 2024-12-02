import json
import os
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
        - full Path to folder with picrutes (path_to_folder_with_pictures)

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
    
def rename_directory(
    path_to_directory: str, 
    ids_df: pd.DataFrame,
) -> None:
    """Find all files in path_to_directory and tries to copy them as images in png format with a new name.
    Name contain id: from ids DF; part_code: file should have a name which is composed of that part code; and file extension - png.
    So images will have a name as: id.part_code.png

    Args:
        path_to_directory (str): Absolute path to the directory
        name_of_file_with_ids (str): Name of file with ids
    """
    # Find all files in path_to_directory
    files = [f for f in pathlib.Path(path_to_directory).iterdir() if f.is_file()]
        
    # For every id we create a copy of each part
    for id in ids_df.iloc[0]:
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
    if config["start_mode"] == 0:
        config = get_config()
        ids_df = get_ids(config["name_of_file_with_ids"])
        rename_directory(
            config["path_to_folder_with_pictures"],
            ids_df
        )
     
    
                
if __name__ == "__main__":
    main()