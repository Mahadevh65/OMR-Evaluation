import cv2
import numpy as np
from PIL import Image
import json

def load_answer_key(path):
    with open(path, 'r') as f:
        data = json.load(f)
    return data

def preprocess_image(image_path, width=1000, height=1400):
    # load, resize, grayscale, blur
    img = cv2.imread(image_path)
    img = cv2.resize(img, (width, height))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    edged = cv2.Canny(blur, 50, 150)
    return img, gray, edged

def find_paper_contour(edged):
    # find contours, pick the biggest rectangular one
    contours, hierarchy = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # sort by area descending
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    for cnt in contours:
        peri = cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
        if len(approx) == 4:
            return approx
    return None

def warp_image(img, contour, width, height):
    # reorder points, then warp
    # use utils for reorder
    pts = contour.reshape(4,2)
    # reordering so that pts order is [top-left, top-right, bottom-right, bottom-left]
    rect = reorder_pts(pts)
    dst = np.array([[0,0], [width-1,0], [width-1, height-1], [0, height-1]], dtype="float32")
    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(img, M, (width, height))
    return warped

def reorder_pts(pts):
    # input: array of 4 points [ (x1,y1), ... ]
    rect = np.zeros((4,2), dtype="float32")
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]
    return rect

def threshold_image(warped):
    gray = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
    # maybe adaptive threshold or fixed
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    return thresh

def extract_responses(thresh_img, answer_key):
    """
    thresh_img: binary image (inverted so bubbles are white on black background)
    answer_key: loaded JSON dict
    """
    h, w = thresh_img.shape
    results = {}
    # for each bubble position
    for b in answer_key['bubble_positions']:
        q = b['q_no']
        subject = b['subject']
        choices = b['choices']
        bx, by, bw, bh = b['box']  # relative
        # convert to pixel coords
        x1 = int(bx * w)
        y1 = int(by * h)
        x2 = int((bx + bw) * w)
        y2 = int((by + bh) * h)
        # crop box
        box_img = thresh_img[y1:y2, x1:x2]
        # count white pixels (because we inverted, filled bubble -> white)
        total = cv2.countNonZero(box_img)
        area = box_img.shape[0] * box_img.shape[1]
        # threshold: say if > some fraction (e.g. 0.5) then filled
        # you may need to tune this/flexibility
        filled = total / float(area) > 0.5
        # store
        if q not in results:
            results[q] = {"selected": None, "scores": 0, "subject": subject}
        # among choices, we want the one with max fill
        # We will compare all choices, so better to accumulate
        if 'choice_counts' not in results[q]:
            results[q]['choice_counts'] = {}
        results[q]['choice_counts'][choices[0]] = results[q]['choice_counts'].get(choices[0],0)
        # but better to iterate over all choices – simpler: compute all, then pick max below
        # We'll build a list per question
        # Let's change: simpler approach: in answer_key bubble_positions we assume choices are in order, 
        # so we can do for each choice box, compare, pick the choice with maximum fill. 

    # Better rewrite extract_responses as below:
    responses = {}
    for q in range(1, answer_key['total_questions']+1):
        # find all box entries for this question
        boxes = [b for b in answer_key['bubble_positions'] if b['q_no']==q]
        best_choice = None
        best_fill = 0
        for b in boxes:
            bx, by, bw, bh = b['box']
            x1 = int(bx * w); y1 = int(by * h)
            x2 = int((bx + bw) * w); y2 = int((by + bh) * h)
            box_img = thresh_img[y1:y2, x1:x2]
            fill = cv2.countNonZero(box_img) / float(box_img.shape[0] * box_img.shape[1])
            if fill > best_fill:
                best_fill = fill
                best_choice = b['choices'][0] if len(b['choices'])==1 else b['choices'][ boxes.index(b) ] 
                # actually defining mapping from each box to a choice needs careful construction
        responses[q] = best_choice
    return responses

def score_responses(responses, answer_key):
    per_subject = {}
    for subj in answer_key['subjects']:
        per_subject[subj] = 0
    total = 0
    for q, sel in responses.items():
        correct = answer_key['correct_answers'].get(str(q))
        subj = None
        # find the subject for this question
        for b in answer_key['bubble_positions']:
            if b['q_no'] == q:
                subj = b['subject']
                break
        if sel == correct:
            per_subject[subj] += 1
            total += 1
    return per_subject, total

# def score_responses(responses, answer_key):
#     # Initialize score per subject
#     per_subject = {subj: 0 for subj in answer_key['subjects']}
#     total = 0

#     for q, sel in responses.items():
#         correct = answer_key['correct_answers'].get(str(q))

#         # If bubble_positions missing, infer subject by question number
#         if "bubble_positions" in answer_key and answer_key["bubble_positions"]:
#             subj = None
#             for b in answer_key['bubble_positions']:
#                 if b['q_no'] == q:
#                     subj = b['subject']
#                     break
#         else:
#             # Fallback: group every 20 questions by subject
#             subj_index = (int(q) - 1) // answer_key['questions_per_subject']
#             subj = answer_key['subjects'][subj_index]

#         # Score
#         if sel == correct:
#             per_subject[subj] += 1
#             total += 1

#     return per_subject, total


def process_image(image_path, key_path, template_width=1000, template_height=1400):
    answer_key = load_answer_key(key_path)
    original, gray, edged = preprocess_image(image_path, template_width, template_height)
    contour = find_paper_contour(edged)
    if contour is None:
        raise Exception("Could not find sheet boundary")
    warped = warp_image(original, contour, template_width, template_height)
    thresh = threshold_image(warped)
    responses = extract_responses(thresh, answer_key)
    per_subject, total_correct = score_responses(responses, answer_key)
    # since 20 questions per subject, subject score can be per_subject[subj], or scaled to 0‑20
    # total out of 100
    return {
        "per_subject": per_subject,
        "total_correct": total_correct,
        "responses": responses
    }
