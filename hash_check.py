# The Direct3DKinematicEstimation paper was difficult to reproduce due to:
# Multiple preprocessing steps of ~550 GB of data that take a couple days on a $1500 PC
# In which errors like time-outs and storage errors can occur
# The processing doesn't check which files are already correct, and instead reprocesses everything
# This script hopes to alleviate some difficulties, by checking which files are correctly stored

# This script compares the generated hashes with the current files in the folder
# These hashes can be created in the "hash_create.py" script

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

# Function that checks if the files exist and have the correct hash
def check_files_in_folder(parent_folder, file_dict):
    # Loop through all the items in the file dictionary
    for filename, hash_value in file_dict.items():
        # Get the full path of the file
        filepath = os.path.join(parent_folder, filename)

        # Check if the file exists and its hash value matches the expected hash value
        if os.path.exists(filepath):
            with open(filepath, 'rb') as f:
                file_data = f.read()
                calculated_hash_value = hashlib.sha256(file_data).hexdigest()

                if calculated_hash_value == hash_value:
                    continue
                    print(f"File '{filename}' exists and has the expected hash value")
                else:
                    print(f"File '{filename}' exists but has a different hash value")
        else:
            print(f"File '{filename}' does not exist in the parent folder")


# Loop over each path in paths_hashable and check if the files exist in the parent folder
for path, name in paths_hashable:
    # Check if the parent folder exists
    if not os.path.exists(path):
        print(f"The following path from {name} does not exist: \n {path}")
        continue
    # Load the dictionary of hashed files
    json_path = os.path.join(hash_directory, name + ".json")
    with open(json_path, 'r') as f:
        hash_dict = json.load(f)
    # Check if each file in the dictionary exists in the parent folder
    check_files_in_folder(path, hash_dict)
    print(f"Finished checking hashes from: {name}")

print("Finished checking the hashes")

