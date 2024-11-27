import re
import csv

# Input and output file paths
input_file_path = 'objects_5_0.txt'
output_csv_path = 'object_group_children.csv'

# Read file content
with open(input_file_path, 'r') as file:
    content = file.read()

# Optimized regex for group and child extraction
object_group_pattern = re.compile(
    r':name\s+\((?P<group_name>[^\)]+)\).*?:type\s+\(group\).*?:ReferenceObject\s*\((?P<references>.*?)\)',
    re.DOTALL
)

# Extract group-child relationships
group_child_counts = []
for match in object_group_pattern.finditer(content):
    group_name = match.group("group_name")
    references = match.group("references")
    child_objects = re.findall(r':Name\s+\((?P<child_name>[^\)]+)\)', references)
    group_child_counts.append({"Group Name": group_name, "Child Object Count": len(child_objects)})

# Write to CSV
with open(output_csv_path, mode='w', newline='') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=["Group Name", "Child Object Count"])
    writer.writeheader()
    writer.writerows(group_child_counts)

print(f"Results saved to {output_csv_path}")