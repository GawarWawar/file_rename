import pandas as pd
import pathlib
import zipfile


def rename_and_zip_photos_in_directory(
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
