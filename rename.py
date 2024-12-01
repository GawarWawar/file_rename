import json
import os
import pathlib
import pandas as pd
from PIL import Image, UnidentifiedImageError
import warnings


def main():
    with open("config.json") as file_config:
        config = json.load(file_config)
     

    files = [f for f in pathlib.Path(config["folder_with_pictures"]).iterdir() if f.is_file()]

    ids = pd.read_csv(config["file_with_ids"])
    for id in ids["ASIN"]:
        for file in files:
            part_code = file.name.removesuffix(".png")
            
            try:
                with Image.open(file, "r") as img:
                    img.save(f"result/{id}.{part_code}.png")
                    print(f"{id}.{part_code}.png")
            except UnidentifiedImageError:
                warnings.warn(f"{file.name} was not an image")
                
if __name__ == "__main__":
    main()