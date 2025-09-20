import json

# Subjects in order
subjects = ["Python", "Data Analysis", "MySQL", "Power BI", "Adv Stats"]

# Config (tune these values based on your OMR sheet design)
start_x = 0.10       # leftmost bubble (A)
start_y = 0.10       # first subject top
x_step = 0.08        # horizontal distance between A, B, C, D
y_step = 0.04        # vertical distance between questions
bubble_w = 0.03      # width of one bubble
bubble_h = 0.03      # height of one bubble
subject_gap = 0.90   # vertical gap between subjects (20 questions block)

bubble_positions = []

q_no = 1
for subj_index, subj in enumerate(subjects):
    # top position for this subject block
    subj_y_start = start_y + subj_index * (20 * y_step + 0.05)

    for i in range(20):  # 20 questions per subject
        q_y = subj_y_start + i * y_step

        for opt_index, opt in enumerate(["A", "B", "C", "D"]):
            q_x = start_x + opt_index * x_step
            bubble_positions.append({
                "q_no": q_no,
                "subject": subj,
                "choices": [opt],
                "box": [round(q_x, 3), round(q_y, 3), bubble_w, bubble_h]
            })

        q_no += 1

# Save into setA_bubbles.json
with open("setA_bubbles.json", "w") as f:
    json.dump(bubble_positions, f, indent=2)

print("Bubble positions generated in setA_bubbles.json")
for item in data:
    print(item["box"])
