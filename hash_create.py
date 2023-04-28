# The Direct3DKinematicEstimation paper was difficult to reproduce due to:
# Multiple preprocessing steps of ~550 GB of data that take a couple days on a $1500 PC
# In which errors like time-outs and storage errors can occur
# The processing doesn't check which files are already correct, and instead reprocesses everything
# This script hopes to alleviate some difficulties, by checking which files are correctly stored

# This script creates the hashes from selected folders
# In the "hash_check.py" script, the hashes can be checked to see which files are missing
# The hashes can be used to skip existing files from re-processing

import os
import json
import pathlib
import hashlib

# Define the directories to scan (ASSUMING SCRIPT IS IN MAIN FOLDER OF "Direct3DKinematicEstimation" )
main_directory = pathlib.Path(__file__).parent
hash_directory = os.path.join(main_directory, "hashes")
if not os.path.exists(hash_directory):
    os.makedirs(hash_directory)

# Paths to downloadable files (MODIFY WHERE NEEDED)
SMPL_DMPL_archives = os.path.join(main_directory, "ms_model_estimation", "resources")
AMASS_data = os.path.join(main_directory, "resources", "amass")
F_Subjects = os.path.join(main_directory, "resources", "V3D", "F")
BMLMovi_videos = os.path.join("D:", "Human Kinematics Data", "avi")
Pascal_VOC = os.path.join("D:", "Human Kinematics Data", "VOC")

# Paths to generated files
generated_dataset = os.path.join(main_directory, "resources", "opensim", "BMLmovi")
prepared_dataset = os.path.join("D:", "_dataset_full")

paths_hashable = [[SMPL_DMPL_archives, "SMPL_DMPL_archives"], 
                    [AMASS_data, "AMASS_data"], [F_Subjects, "F_Subjects"],
                    [BMLMovi_videos, "BMLMovi_videos"], [Pascal_VOC, "Pascal_VOC"],
                    [generated_dataset, "generated_dataset"], [prepared_dataset, "prepared_dataset"]]

# Function that hashes all files in a folder
def hash_files_in_folder(parent_folder):
    # Define a dictionary to store the file names and hashes
    file_dict = {}

    # Loop through all the files and folders in the parent folder
    for root, dirs, files in os.walk(parent_folder):
        for filename in files:
            # Get the full path of the file
            filepath = os.path.join(root, filename)

            # Open the file and read its contents
            with open(filepath, 'rb') as f:
                file_data = f.read()

            # Calculate the SHA256 hash of the file contents
            hash_value = hashlib.sha256(file_data).hexdigest()

            # Get the file name without the parent folder path
            rel_path = os.path.relpath(filepath, parent_folder)

            # Add the filename and hash to the dictionary
            file_dict[rel_path] = hash_value

    # Return the dictionary
    return file_dict

# Save the hash dictionary
for path, name in paths_hashable:
    if not os.path.exists(path):
        print(f"The following path from {name} does not exist: \n {path}")
        continue
    hash_dict = hash_files_in_folder(path)
    json_path = os.path.join(hash_directory, name + ".json")
    with open(json_path, 'w') as f:
        json.dump(hash_dict, f)
    print(f"Hashed files from: {name}")

print("Finished hashing")

