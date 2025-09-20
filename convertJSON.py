import pandas as pd
import json
import os

# Path to your Excel key
excel_file = "Key (Set A and B).xlsx"

# Output folder (must exist)
output_folder = "answer_keys"
os.makedirs(output_folder, exist_ok=True)

# Subject mapping (20 questions each)
subjects = ["Python", "Data Analysis", "MySQL", "Power BI", "Adv Stats"]

def extract_answers(df):
    correct_answers = {}
    for col in df.columns:
        for cell in df[col].dropna():
            parts = str(cell).replace(".", "-").split("-")
            if len(parts) >= 2:
                q_no = parts[0].strip()
                ans = parts[1].strip().upper()
                correct_answers[q_no] = ans
    return dict(sorted(correct_answers.items(), key=lambda x: int(x[0])))

def build_json(version, answers):
    data = {
        "version": version,
        "subjects": subjects,
        "questions_per_subject": 20,
        "total_questions": 100,
        "bubble_positions": [],
        "correct_answers": answers
    }
    return data

# Load sheets
set_a_df = pd.read_excel(excel_file, sheet_name="Set - A")
set_b_df = pd.read_excel(excel_file, sheet_name="Set - B")

# Extract answers
set_a_answers = extract_answers(set_a_df)
set_b_answers = extract_answers(set_b_df)

# Build JSONs
set_a_json = build_json("setA", set_a_answers)
set_b_json = build_json("setB", set_b_answers)

# Save JSONs
with open(os.path.join(output_folder, "setA.json"), "w") as f:
    json.dump(set_a_json, f, indent=2)

with open(os.path.join(output_folder, "setB.json"), "w") as f:
    json.dump(set_b_json, f, indent=2)

print("JSON keys generated: setA.json and setB.json")
