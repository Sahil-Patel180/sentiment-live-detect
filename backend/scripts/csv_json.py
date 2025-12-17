import csv
import json

# Define file paths
csv_file_path = 'combined_emotion.csv'
json_file_path = 'combined_emotion.json'

# Read CSV and convert to list of dictionaries
data = []
with open(csv_file_path, encoding='utf-8') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        data.append(row)

# Write to JSON file
with open(json_file_path, 'w', encoding='utf-8') as json_file:
    json.dump(data, json_file, indent=4)

print("Conversion complete!")