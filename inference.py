from openai import OpenAI
import os
from dotenv import load_dotenv
import re
import pandas as pd
from prompts import prompt

load_dotenv()
api_key = os.environ.get("OPENAI_API_KEY")
os.environ['OPENAI_API_KEY'] = api_key
client = OpenAI()
dev_data_path = 'mantis+emnlp'
prop_dev = pd.read_csv("csv/phrases/phrased_dev.csv")
# model_name = 'ft:gpt-4o-mini-2024-07-18:personal::AVIkMPT1'
# model_name = 'gpt-4o-mini-2024-07-18'
model_name = 'ft:gpt-4o-mini-2024-07-18:personal::AW8HKdcw' # final with spans



def respond(input_text):    

    response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": input_text}
              ]
            # messages= [ {'role': 'assistant', 'content': f"""{prompt1}"""},],
            
        )
    response_message = response.choices[0].message.content
    return response_message

allowed_phrases = [
    'Appeal_to_Authority', 'Appeal_to_fear-prejudice', 'Bandwagon', 'Reductio_ad_hitlerum',
    'Black-and-White_Fallacy', 'Causal_Oversimplification', 'Doubt', 'Exaggeration,Minimisation',
    'Flag-Waving', 'Loaded_Language', 'Name_Calling,Labeling', 'Repetition', 'Slogans',
    'Thought-terminating_Cliches', 'Whataboutism', 'Straw_Men', 'Red_Herring'
]

# Regular expression pattern for allowed phrases
pattern = r'^(?:' + '|'.join(map(re.escape, allowed_phrases)) + r')'

# Function to process each value in the column
def process_phrases(phrases):
    # Split the value by '\n'
    lines = phrases.split(', ')
    merged_lines = []
    
    for line in lines:
        # If the line starts with an allowed phrase, add it as a new line
        if re.match(pattern, line):
            merged_lines.append(line)
        else:
            # Otherwise, merge it with the previous line
            if merged_lines:
                merged_lines[-1] += f", {line}"
            else:
                merged_lines.append(line)  # If no previous line, add it as is
    return '\n'.join(merged_lines)


# Function to parse model response
def parse_response(response):
    parsed_phrases = []
    items = response.split("\n")  # Split by \n for each technique/phrase pair
    for item in items:
        if ": " in item:
            technique, phrase = item.split(": ", 1)
            parsed_phrases.append((technique.strip(), phrase.strip()))
    return parsed_phrases

def run_inference():
    # create folder for results 
    if not os.path.exists(os.path.join('results/', 'spans')):
        os.makedirs(os.path.join('results/', 'spans'))
        # run inference on dev set and save results
    articles = sorted([filename for filename in os.listdir('mantis+emnlp') if filename.endswith('.txt')])
    print("run inference on dev set and save results")

    # Initialize an empty list to store DataFrame rows
    inference_results = []
    for article in (articles):
            full_article_path = os.path.join(dev_data_path, article)
            if os.path.exists(os.path.join('results/', 'spans', article)): # check if prediction already exists
               continue
            with open(full_article_path, 'r', encoding='utf-8') as f:
                input_text = f.read()
                
            model_output = respond(input_text)
            if model_output == '':
                print("WARNING: model output is empty")
                #model_output = 'No propaganda found'
            if 'no propaganda' in model_output:
                #print("WARNING: model output is empty")
                model_output = ''
            with open(os.path.join('results/','spans', article), 'w', encoding="utf-8") as f:
                f.write(model_output)
            # processed = process_phrases(model_output)
            # parsed = parse_response(processed)
            # Append results to the DataFrame list
            inference_results.append({'Content': article, 'predicted_phrases': model_output})
        # Create a DataFrame from results
    df_results = pd.DataFrame(inference_results)
    print(f"Inference completed for {len(df_results)} articles.")

    return df_results


df_results = run_inference()
df_results.to_csv("results/spans/results_spans_inference.csv")

# df_results = pd.read_csv("results_inference.csv")
# df = pd.DataFrame()
# df = pd.concat([prop_dev['manipulation_phrases'], df_results['predicted_phrases']], axis=1)


