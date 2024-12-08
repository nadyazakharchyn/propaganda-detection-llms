from openai import OpenAI
import numpy as np
import os
from dotenv import load_dotenv
from sklearn.metrics import accuracy_score, hamming_loss, precision_score, recall_score, f1_score
from sklearn.preprocessing import MultiLabelBinarizer
import tqdm
import pandas as pd
from difflib import SequenceMatcher

api_key = os.environ.get("OPENAI_API_KEY")
os.environ['OPENAI_API_KEY'] = api_key
client = OpenAI()

#model_name = 'ft:gpt-4o-mini-2024-07-18:personal::AVIkMPT1'


def calculate_similarity(phrase1, phrase2):
    """Compute similarity between two phrases using SequenceMatcher."""
    return SequenceMatcher(None, phrase1, phrase2).ratio()

def extract_phrase(text):
    """Extract the part of the phrase after ':'."""
    return text.split(':', 1)[1].strip() if ':' in text else text.strip()


def evaluate_propaganda_2(df, similarity_threshold=0.3):
    all_true_positives = 0
    all_false_positives = 0
    all_false_negatives = 0

    for _, row in df.iterrows():
        predicted = row["predicted_phrases"]
        actual = row["manipulation_phrases"]
        
        # Convert non-string or NaN values to empty lists
        list_predicted = str(predicted).split('\n') if isinstance(predicted, str) else []
        list_actual = str(actual).split('\n') if isinstance(actual, str) else []

        # Extract the parts after ':' and remove duplicates/empty strings
        list_predicted = list(set(filter(None, [extract_phrase(p) for p in list_predicted])))
        list_actual = list(set(filter(None, [extract_phrase(a) for a in list_actual])))

        list_predicted = list(set(list_predicted))
        # Handle special case: both lists empty → count as true positive
        if not list_predicted and not list_actual:
            # print("yes it happens")
            all_true_positives += 1
            continue
        
        # Initialize sets for matching
        actual_matched = set()
        true_positives = 0
        
        # Match predicted to actual
        for pred in list_predicted:
            best_match = None
            best_similarity = 0
            
            for act in list_actual:
                if act not in actual_matched:
                    # Explicitly handle empty strings
                    if not pred and not act:
                        best_similarity = 1  # Empty strings match perfectly
                        best_match = act
                    else:
                        similarity = SequenceMatcher(None, pred, act).ratio()
                        
                        if similarity > best_similarity:
                            best_similarity = similarity
                            best_match = act
            
            if best_similarity >= similarity_threshold and best_match:
                #print('Predicted phrase: ', pred, ' | Actual phrase: ', best_match)
                true_positives += 1
                actual_matched.add(best_match)
        
        # Calculate false positives and false negatives
        false_positives = len(list_predicted) - true_positives
        false_negatives = len(list_actual) - len(actual_matched)
        
        all_true_positives += true_positives
        all_false_positives += false_positives
        all_false_negatives += false_negatives

    # Aggregate metrics
    precision = all_true_positives / (all_true_positives + all_false_positives) if (all_true_positives + all_false_positives) > 0 else 0
    recall = all_true_positives / (all_true_positives + all_false_negatives) if (all_true_positives + all_false_negatives) > 0 else 0
    f_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    
    return precision, recall, f_score

def calculate_metrics(pred_label_path, metric_file_path):
        
        """pred_label_path files must have each line starting with a technique and :. Need to hardcode filenames in pred label path"""
        true_labels = []
        pred_labels = []

        # pred_label_path = os.path.join('kaggle_results/results')

        filenames = sorted([filename for filename in os.listdir(dev_data_path) if filename.endswith('.tsv')])
        count = 0
        for filename in filenames:
            true_label_file = []
            file_path = os.path.join(dev_data_path, filename)
            if os.stat(file_path).st_size == 0:
                true_labels.append(true_label_file) 
            else:
                with open(file_path, 'r', encoding="utf-8") as file:
                    for line in file:
                        line = line.strip()
                        line = line.split('\t')[1]
                        true_label_file.append(line)
                true_labels.append(true_label_file)

            pred_label_file = set()
            allowed_labels = ['Appeal_to_Authority', 'Appeal_to_fear-prejudice', 'Bandwagon','Reductio_ad_hitlerum', 'Black-and-White_Fallacy', 'Causal_Oversimplification', 'Doubt', 'Exaggeration,Minimisation', 'Flag-Waving', 'Loaded_Language', 'Name_Calling,Labeling', 'Repetition', 'Slogans', 'Thought-terminating_Cliches', 'Whataboutism','Straw_Men','Red_Herring']
            file_name = str(filename.split('.labels.tsv')[0])+'.txt'
            # file_name = str(count)+'.txt'
            with open(os.path.join(pred_label_path, file_name), 'r', encoding="utf-8") as file:
                input_text = file.read()
                #response = input_text.split('Response:')[1] # for Gemma
                if (input_text == '') | (input_text == 'No propaganda found') | (input_text == 'no propaganda detected'):
                    pred_labels.append(list(pred_label_file))
                else:

                    for line in input_text.splitlines():

                        label = line.split(': ')[0].strip()
                        if label in allowed_labels:
                            pred_label_file.add(label)

                    pred_labels.append(list(pred_label_file))
            count += 1


        # Convert labels to binary representation using MultiLabelBinarizer
        mlb = MultiLabelBinarizer()
        true_labels_binary = mlb.fit_transform(true_labels)
        predicted_labels_binary = mlb.transform(pred_labels)

        # Define the output file path
        # metric_file_path = os.path.join('results/', 'metrics_gemma_9.txt')

        # Open the file in write mode
        with open(metric_file_path, "w") as file:
            # Accuracy
            accuracy = accuracy_score(true_labels_binary, predicted_labels_binary)
            file.write(f"Accuracy: {accuracy}\n")

            # Hamming Loss
            hamming_loss_value = hamming_loss(true_labels_binary, predicted_labels_binary)
            file.write(f"Hamming Loss: {hamming_loss_value}\n")

            # Precision, Recall, and F1-Score (Micro-Averaged)
            precision = precision_score(true_labels_binary, predicted_labels_binary, average='micro')
            recall = recall_score(true_labels_binary, predicted_labels_binary, average='micro')
            f1 = f1_score(true_labels_binary, predicted_labels_binary, average='micro')
            file.write(f"Micro-Averaged Precision: {precision}\n")
            file.write(f"Micro-Averaged Recall: {recall}\n")
            file.write(f"Micro-Averaged F1-Score: {f1}\n")

            # Subset Accuracy
            subset_accuracy = accuracy_score(true_labels_binary, predicted_labels_binary, normalize=True)
            file.write(f"Subset Accuracy: {subset_accuracy}\n")

            # Macro-Averaged Precision, Recall, and F1-Score
            macro_precision = precision_score(true_labels_binary, predicted_labels_binary, average='macro')
            macro_recall = recall_score(true_labels_binary, predicted_labels_binary, average='macro')
            macro_f1 = f1_score(true_labels_binary, predicted_labels_binary, average='macro')
            file.write(f"Macro-Averaged Precision: {macro_precision}\n")
            file.write(f"Macro-Averaged Recall: {macro_recall}\n")
            file.write(f"Macro-Averaged F1-Score: {macro_f1}\n")

            # F1-Score per class
            class_f1_scores = f1_score(true_labels_binary, predicted_labels_binary, average=None)
            file.write("F1-Score per Class:\n")
            for label, f1_score_class in zip(mlb.classes_, class_f1_scores):
                file.write(f"{label}: {f1_score_class}\n")
        print("Evaluation metrics written to the file:", metric_file_path)

def extract_phrases(row):
    manipulations = row["predicted_phrases"]
    text = row["Content"]
    
    # Check if manipulations or text are NaN
    if pd.isna(manipulations) or pd.isna(text):
        return []  # Return an empty list if either is NaN
    
    extracted = []
    manipulations = manipulations.split('\n')
    for manipulation in manipulations:
        # Parse the technique and indices
        parts = manipulation.split("\t")
        if len(parts) == 3:  # Ensure valid structure
            try:
                technique = parts[0]
                start = int(parts[1])
                end = int(parts[2].strip())
                phrase = text[start:end]
                extracted.append(f"{technique}: {phrase}")
            except ValueError:
                # Handle cases where conversion to int fails
                continue  # Skip invalid entries
    
    return extracted



# for classification evaluation
dev_data_path = 'mantis+emnlp_en'

# 
# metric_file_path = os.path.join('results/', 'metrics_gemma2_9_techniques.txt')
# pred_label_path = os.path.join('kaggle_results/results')
# pred_label_path = os.path.join('results/phrased_temp_5')
# metric_file_path = os.path.join('results/', 'metrics_phrased_temp5_1.txt')

pred_label_path = os.path.join('results/phrased_temp_5_en')
metric_file_path = os.path.join('results/', 'metrics_phrased_temp_5_en.txt')
# calculate_metrics(pred_label_path, metric_file_path)



# for spans evaluation
# prop_dev = pd.read_csv("csv/prop_dev_final.csv")
prop_dev = pd.read_csv("csv/phrases/phrased_dev_string.csv")

# file_1 = "results/spans/results_spans_inference.csv"
# file_1 = "kaggle_results/results/inference_results_phrased.csv"
file_1 = "results_inference_temp_5.csv"
# file_1 = "results/phrased_gpt/results_inference_gpt.csv"
# file_1 = "results/phrased/inference.csv"

#metrics_spans_file = "full_task_phrased.txt"
# metrics_spans_file = "only_span_phrased_temp_5.txt"
metrics_spans_file = "only_span_phrased_temp_5_1_en.txt"
# metrics_spans_file = "only_span_spans.txt"
df_results = pd.read_csv(file_1)
df_results = df_results.loc[126:185]
#df_results = df_results.loc[0:126]

# Apply function to create the new column
# phrased_df = df_results.copy()
# phrased_df = pd.concat([phrased_df["predicted_phrases"], prop_dev['Content']], axis=1)
# phrased_df['predicted_phrases'] = phrased_df['predicted_phrases'].replace(to_replace=r'.* detected', value=np.nan, regex=True)

# phrased_df["predicted_phrases"] = phrased_df.apply(extract_phrases, axis=1)
# phrased_df['predicted_phrases'] = [",\n".join(map(str, l)) for l in phrased_df['predicted_phrases']]

df_results.rename(columns={"manipulation_phrases": "predicted_phrases"}, inplace=True)
df = pd.DataFrame()
#prop_dev.loc[0:126]
prop_dev.loc[126:185]
# prop_dev.drop(df.tail(1).index,inplace=True) # only for gemma phrased
df = pd.concat([prop_dev['Content'],prop_dev['manipulation_phrases'], df_results["predicted_phrases"]], axis=1)

precision, recall, f_score = evaluate_propaganda_2(df, similarity_threshold=0.5)
print(f"Precision: {precision:.2f}, Recall: {recall:.2f}, F-score: {f_score:.2f}")
with open(metrics_spans_file, 'w') as file:
    file.write(file_1)
    file.write(f"\nPrecision: {precision:.2f}, Recall: {recall:.2f}, F-score: {f_score:.2f}")



