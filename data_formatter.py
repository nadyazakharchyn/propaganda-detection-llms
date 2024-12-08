import os
import pandas as pd
import re
from inference import calculate_similarity

res_data_path = 'results/phrased_temp_5'
prop_dev = pd.read_csv("csv/phrases/phrased_dev.csv")
prop_dev['manipulation_phrases'] = prop_dev['manipulation_phrases'].fillna('')


# List of allowed phrases
allowed_phrases = [
    'Appeal_to_Authority', 'Appeal_to_fear-prejudice', 'Bandwagon', 'Reductio_ad_hitlerum',
    'Black-and-White_Fallacy', 'Causal_Oversimplification', 'Doubt', 'Exaggeration,Minimisation',
    'Flag-Waving', 'Loaded_Language', 'Name_Calling,Labeling', 'Repetition', 'Slogans',
    'Thought-terminating_Cliches', 'Whataboutism', 'Straw_Men', 'Red_Herring'
]

# Regular expression pattern for allowed phrases
pattern = r'^(?:' + '|'.join(map(re.escape, allowed_phrases)) + r')'

# Function to process each value in the column
# def process_phrases(phrases):
#     # Split the value by '\n'
#     lines = phrases.split(', ')
#     merged_lines = []
    
#     for line in lines:
#         # If the line starts with an allowed phrase, add it as a new line
#         if re.match(pattern, line):
#             merged_lines.append(line)
#         else:
#             # Otherwise, merge it with the previous line
#             if merged_lines:
#                 merged_lines[-1] += f", {line}"
#             else:
#                 merged_lines.append(line)  # If no previous line, add it as is
#     return '\n'.join(merged_lines)


# # Function to parse model response
# def parse_response(response):
#     parsed_phrases = []
#     items = response.split("\n")  # Split by \n for each technique/phrase pair
#     items = list(set(items))
#     for item in items:
#         if ": " in item:
#             technique, phrase = item.split(": ", 1)
#             parsed_phrases.append((technique.strip(), phrase.strip()))
#     return parsed_phrases


phrased_dir = "results/phrased_gpt"

# Initialize an empty list to hold file names and their content
data = []

# # Iterate over all text files in the directory
# for file_name in os.listdir(phrased_dir):
#     if file_name.endswith(".txt"):  # Only process .txt files
#         file_path = os.path.join(phrased_dir, file_name)
#         with open(file_path, "r", encoding="utf-8") as file:
#             content = file.read().strip()  # Read the file and strip any leading/trailing whitespace
            
#         # Add an empty value if the content is "No propaganda found"
#         if content == "No propaganda found":
#             content = ""
        
#         # Append the file name and content to the data list
#         data.append({"name": file_name, "predicted_phrases": content})

# # Create a DataFrame from the data list
# df = pd.DataFrame(data)

# # Display the DataFrame (optional)
# df.to_csv("results_inference_temp_5.csv")

# Function to process the content of each file
def process_phrases(content):
    """Processes and parses content into structured data."""
    parsed_phrases = []
    if content.strip() == "No propaganda found":
        return []

    # Split by lines
    lines = content.split("\n")
    for line in lines:
        if not line.strip():
            continue  # Skip empty lines
        if ": " in line:
            technique, phrases = line.split(": ", 1)
            if re.match(pattern, technique.strip()):  # Ensure valid technique
                # Extract phrases within quotes
                phrase_list = re.findall(r'"([^"]+)"', phrases)
                for phrase in phrase_list:
                    parsed_phrases.append((technique.strip(), phrase.strip()))
    return parsed_phrases


# Iterate over all text files in the directory
for file_name in os.listdir(phrased_dir):
    if file_name.endswith(".txt"):  # Only process .txt files
        file_path = os.path.join(phrased_dir, file_name)
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read().strip()  # Read the file and strip any leading/trailing whitespace
            
        # Process the content to extract phrases
        parsed_content = process_phrases(content)
        
        # If "No propaganda found", use an empty value
        if not parsed_content:
            data.append({"name": file_name, "predicted_phrases": ""})
        else:
            # Convert parsed content into a structured string
            formatted_phrases = ", \n".join([f"{technique}: {phrase}" for technique, phrase in parsed_content])
            data.append({"name": file_name, "predicted_phrases": formatted_phrases})

# Convert data to a pandas DataFrame
df = pd.DataFrame(data)

# Save the DataFrame to a CSV file (optional)
output_csv_path = "results_inference_gpt.csv"
df.to_csv(output_csv_path, index=False, encoding="utf-8")

# Print the resulting DataFrame
print(df)