#!/usr/local/bin/python3

import re
import os
import glob

# Define the folder containing configuration files
config_folder = './fgt_conf'

# Define the folder to save sanitized files
output_folder = './fgt_pwdremoved'

# Ensure the output folder exists
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Find all .conf files in the folder
config_files = glob.glob(os.path.join(config_folder, '*.conf'))

# Process each .conf file
for file_path in config_files:
    # Extract the base filename (without the directory)
    base_name = os.path.basename(file_path)

    # Define the new file path in the output folder
    new_file_path = os.path.join(output_folder, base_name.replace('.conf', '_pwdremoved.conf'))

    # Define the keywords to search for
    password_keywords = ['set password', 'set private-key', 'set passwd']

    # Open the file and search for lines containing the specified keywords
    with open(file_path, 'r') as file, open(new_file_path, 'w') as new_file:
        inside_private_key_block = False  # Flag to skip lines within the private key block

        for line in file:
            if inside_private_key_block:
                # Check if we've reached the end of the private key block
                if "-----END ENCRYPTED PRIVATE KEY-----" in line or "-----END OPENSSH PRIVATE KEY-----" in line:
                    inside_private_key_block = False  # Stop skipping lines
                continue  # Skip all lines within the private key block

            # Check for keywords and process each line accordingly
            for keyword in password_keywords:
                if line.strip().startswith(keyword):
                    if keyword == 'set private-key' and ("-----BEGIN ENCRYPTED PRIVATE KEY-----" in line or "-----BEGIN OPENSSH PRIVATE KEY-----" in line):
                        # Start of private key block, replace line and start skipping
                        line = 'set private-key XXX\n'
                        inside_private_key_block = True  # Begin skipping until the end of the block
                    else:
                        # Replace anything following the keyword with 'XXX'
                        line = re.sub(f'({keyword}) .+', r'\1 XXX', line)
                    break  # Stop checking further keywords if a match is found

            new_file.write(line)

    print(f"Modified file saved as: {new_file_path}")