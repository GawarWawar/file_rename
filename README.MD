# File rename

## General
Program copies, changes names and compresses photos into zip. 

## Config
To change a behavior of the program, config.json should be used. It has next parameters:
- start_mode:
    - 1: Standard mode. Read ids from the directory where script is; look for the folder with images; copy images with new names into result zip that will be located into result folder.
    - 2: Advanced mode. Read directory with directories; in each child directory look for the ids file; perform separate rename_and_zip_photos_in_directory on each directory; resulting zips will be located in the result directory.
    - 2.1: Advanced mode (different save location). Read directory with directories; in each directory look for the ids file; perform separate rename_and_zip_photos_in_directory on each directory; resulting zips will be located in the same folders as photos are processed.  
- name_of_file_with_ids (str): Name of the CSV file with all IDs.
- path_to_folder (str): Full path to the folder for program actions.

## Instalation and usage
To use this script python 3.12+ is needed. It should be able to start on earlier versions, but no guarantee :D
All dependences are in the requirements.txt file.
So steps are:
- Install python 3.12
- Configure it for your system (optionl)
- `python -m pip install -r requirements.txt`
- `python rename.py`

<!-- WILL BE IMPLIMENTED IN THE NEAR FUTURE -->
<!-- If you are on windows machine, rename.exe could be used. -->
