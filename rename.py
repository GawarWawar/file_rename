import pathlib

from src.main_process import rename_and_zip_photos_in_directory
from src.set_up import get_config, get_directory, get_ids

config = get_config()
if config["start_mode"] == 1:
    # Standard mode. Read ids from the directory where script is; look for the folder with images; 
        # copy images with new names into result zip that will be located into result folder.

    ids_df = get_ids(config["name_of_file_with_ids"])
    file_pathes = get_directory(config["path_to_folder"], get_all=False)
    rename_and_zip_photos_in_directory(
        file_pathes,
        ids_df
    )
elif config["start_mode"] >= 2:
    # Advanced mode. Read directory with directories; in each child directory look for the ids file; 
        # perform separate rename_and_zip_photos_in_directory on each directory; resulting zips will be located in the result directory.
    
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
                    
                rename_and_zip_photos_in_directory(
                    file_pathes,
                    ids_df,
                    custom_zip_path=zip_save_location,
                    custom_zip_name=file_pathes[0].parent.name
                )   
        else:
            print(f"{item} is not a directory. SKIP")