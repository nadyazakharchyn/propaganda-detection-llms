import pandas as pd
import json
from prompts import prompt_base, prompt

# prop = pd.read_csv("csv/phrases/phrased_train_string.csv")
# prop_val = pd.read_csv("csv/phrases/phrased_val_string.csv")

prop = pd.read_csv("csv/prop_train_final.csv")
prop_val = pd.read_csv("csv/prop_val_final.csv")

prop['manipulations'] = prop['manipulations'].fillna('no propaganda detected')
prop_val['manipulations'] = prop_val['manipulations'].fillna('no propaganda detected')


# Open a file to write the jsonl content
with open('jsonl/prop_final_train.jsonl', 'w', encoding='utf-8') as f:
    # Iterate through each row of the DataFrame
    for index, row in prop.iterrows():
        # Create the JSON structure for each row
        
        json_obj = {
            "messages": [
                {"role": "system", "content": prompt},
                {"role": "user", "content": row['Content']},
                {"role": "assistant", "content": row['manipulations']}
            ]
        }
        # Write each JSON object as a line in the JSONL file
        f.write(json.dumps(obj = json_obj, ensure_ascii=False) + '\n')

with open('jsonl/prop_final_val.jsonl', 'w', encoding='utf-8') as f:
    # Iterate through each row of the DataFrame
    for index, row in prop_val.iterrows():
        # Create the JSON structure for each row
        
        json_obj = {
            "messages": [
                {"role": "system", "content": prompt},
                {"role": "user", "content": row['Content']},
                {"role": "assistant", "content": row['manipulations']}
            ]
        }
        # Write each JSON object as a line in the JSONL file
        f.write(json.dumps(obj = json_obj, ensure_ascii=False) + '\n')

import json


# Function to validate JSONL
def validate_jsonl(file_path):
    errors = 0
    with open(file_path, "r", encoding="utf-8") as file:
        for i, line in enumerate(file, 1):
            try:
                json.loads(line)  # Attempt to parse each line
            except json.JSONDecodeError as e:
                print(f"Invalid JSON on line {i}: {e}")
                errors += 1
    if errors == 0:
        print("Validation successful! All lines are valid JSON.")
    else:
        print(f"Validation failed with {errors} invalid lines.")

# Validate the escaped file
# escape_file("dataset_train_2.jsonl", "dataset_esc_2.jsonl")
# escape_file("dataset_val_2.jsonl", "dataset_esc_val_2.jsonl")
validate_jsonl("jsonl/prop_final_val.jsonl")
validate_jsonl("jsonl/prop_final_train.jsonl")