from flask import Flask, request, render_template, redirect, url_for, send_file
import os
from werkzeug.utils import secure_filename
from omr_processor import process_image
import sqlite3
import uuid
import json

# conn = sqlite3.connect('data/results.db')
# c = conn.cursor()
# c.execute("SELECT * FROM results WHERE student_name=?",("Mahadev",))
# # conn.commit()
# # conn.close()
# user=c.fetchone()
# print(user)

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# initialize DB
def init_db():
    conn = sqlite3.connect('data/results.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS results (
            id TEXT PRIMARY KEY,
            student_name TEXT,
            sheet_version TEXT,
            per_subject TEXT,  -- JSON
            total_correct INTEGER,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

init_db()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET','POST'])
def upload_file():
    if request.method == 'POST':
        student_name = request.form.get('student_name')
        sheet_version = request.form.get('sheet_version')
        file = request.files.get('file')
            
        if not student_name or not sheet_version or not file:
            return "Missing data", 400
        if file and allowed_file(file.filename):
            fname = secure_filename(file.filename)
            unique_name = f"{uuid.uuid4().hex}_{fname}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_name)
            file.save(filepath)
            # process
            key_path = f"answer_keys/{sheet_version}.json"
            try:
                result = process_image(filepath, key_path)
            except Exception as e:
                return f"Error processing image: {str(e)}", 500
            # save to DB
            conn = sqlite3.connect('data/results.db')
            c = conn.cursor()
            c.execute('''
                INSERT INTO results (id, student_name, sheet_version, per_subject, total_correct)
                VALUES (?, ?, ?, ?, ?)
            ''', (uuid.uuid4().hex, student_name, sheet_version, json.dumps(result["per_subject"]), result["total_correct"]))
            conn.commit()
            conn.close()
            return render_template("result.html", student_name=student_name, per_subject=result["per_subject"], total=result["total_correct"])
        else:
            return "File not allowed", 400
    else:
        # list versions available
        versions = [f[:-5] for f in os.listdir('answer_keys') if f.endswith('.json')]
        return render_template("upload.html", versions=versions)

if __name__ == "__main__":
    app.run(debug=True, port="8051", use_reloader=False)
