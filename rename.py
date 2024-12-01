import json
import os
import pathlib
import pandas as pd
from PIL import Image, UnidentifiedImageError
import warnings


def main():
    # Config file with: 
        # name of csv file with all ids (file_with_ids)
        # full Path to folder with picrutes (folder_with_pictures)
    with open("config.json") as file_config:
        config = json.load(file_config)
     
    # Find all files in config["folder_with_pictures"]
    files = [f for f in pathlib.Path(config["folder_with_pictures"]).iterdir() if f.is_file()]

    # Make a list of ids from config["file_with_ids"]
    ids = pd.read_csv(config["file_with_ids"])
    # ASIN - column with all off ids. Only this column matter
        # CSV can contin other columns and it wont affect process 
        
    # For every id we create a copy of each part
    for id in ids["ASIN"]:
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
                
if __name__ == "__main__":
    main()