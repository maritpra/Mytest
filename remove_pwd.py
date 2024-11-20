#/usr/bin/python3
import re
import os

# Define the parameters
file_path = '/Users/maritprachyabrued/Documents/data/Noen_Phlap_Wan_7-4_2702_202411131002.conf'

# Define the new file path with "_pwdremoved" added to the original filename
base_name, ext = os.path.splitext(file_path)
new_file_path = f"{base_name}_pwdremoved{ext}"

# Define the keywords to search for
password_keywords = ['set password', 'set private-key', 'set public-key', 'set certificate', 'set passwd', 'set ca']

# Open the file and search for lines containing the specified keywords
with open(file_path, 'r') as file, open(new_file_path, 'w') as new_file:
    inside_private_key_block = False  # Flag to skip lines within the private key block
    inside_certificate_block = False  # Flag to skip lines within the certificate block

    for line in file:
        if inside_private_key_block:
            # Check if we've reached the end of the private key block
            if "-----END ENCRYPTED PRIVATE KEY-----" in line or "-----END OPENSSH PRIVATE KEY-----" in line:
                inside_private_key_block = False  # Stop skipping lines
            continue  # Skip all lines within the private key block

        if inside_certificate_block:
            # Check if we've reached the end of the certificate block
            if "-----END CERTIFICATE-----" in line:
                inside_certificate_block = False  # Stop skipping lines
            continue  # Skip all lines within the certificate block

        # Check for keywords and process each line accordingly
        for keyword in password_keywords:
            if line.strip().startswith(keyword):
                if keyword == 'set private-key' and ("-----BEGIN ENCRYPTED PRIVATE KEY-----" in line or "-----BEGIN OPENSSH PRIVATE KEY-----" in line):
                    # Start of private key block, replace line and start skipping
                    line = 'set private-key XXX\n'
                    inside_private_key_block = True  # Begin skipping until the end of the block
                elif keyword == ('set certificate' or 'set ca') and "-----BEGIN CERTIFICATE-----" in line:
                    # Start of certificate block, replace line and start skipping
                    line = 'set certificate XXX\n'
                    inside_certificate_block = True  # Begin skipping until the end of the certificate block
                else:
                    # Replace anything following the keyword with 'XXX'
                    line = re.sub(f'({keyword}) .+', r'\1 XXX', line)
                break  # Stop checking further keywords if a match is found

        new_file.write(line)

# Write the modified line to the new file by appending _pwdremoved to filename
print(f"Modified file saved as: {new_file_path}")