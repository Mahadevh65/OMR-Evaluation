# 📄 OMR Sheet Evaluation System

This project is a **Streamlit-based web application** for evaluating Optical Mark Recognition (OMR) answer sheets.  
It allows users to upload an OMR response sheet, compare it with the answer key, and automatically generate student results.  
All results are stored in an **SQLite database** for easy access.

---

## 🚀 Features

- ✅ Upload scanned OMR sheets (image format)  
- ✅ Extract marked answers using pre-defined JSON coordinates  
- ✅ Compare answers with the correct answer key  
- ✅ Auto-generate results (marks & percentage)  
- ✅ Store results in **SQLite database**  
- ✅ View student results directly in the app  
- ✅ Admin can clear/reset data  

---

## 🛠️ Tech Stack

- **Frontend**: HTML, CSS 
- **Backend**: Python (Flask)  
- **Database**: SQLite  
- **Libraries**:  
  - `sqlite3` → store and fetch student results  
  - `opencv-python` → image processing for OMR  
  - `numpy` → calculations  
  - `pandas` → handling results  
  - `streamlit` → user interface  

---

## 📂 Project Structure
# 📄 OMR Sheet Evaluation System

This project is a **web application** for evaluating Optical Mark Recognition (OMR) answer sheets.  
It allows users to upload an OMR response sheet, compare it with the answer key, and automatically generate student results.  
All results are stored in an **SQLite database** for easy access.

---

## 🚀 Features

- ✅ Upload scanned OMR sheets (image format)  
- ✅ Extract marked answers using pre-defined JSON coordinates  
- ✅ Compare answers with the correct answer key  
- ✅ Auto-generate results (marks & percentage)  
- ✅ Store results in **SQLite database**  
- ✅ View student results directly in the app  
- ✅ Admin can clear/reset data  

---

## 🛠️ Tech Stack

- **Frontend**: [Streamlit](https://streamlit.io/)  
- **Backend**: Python (Flask/Streamlit logic)  
- **Database**: SQLite  
- **Libraries**:  
  - `sqlite3` → store and fetch student results  
  - `opencv-python` → image processing for OMR  
  - `numpy` → calculations  
  - `pandas` → handling results  
  - `streamlit` → user interface  

---

## 📂 Project Structure
OMR-Evaluation/
│-- app.py # Main Streamlit application
│-- database.db # SQLite database (auto-created)
│-- omr_utils.py # Helper functions for OMR processing
│-- requirements.txt # Dependencies
│-- README.md # Project documentation
│-- data/ # Sample OMR sheets & keys
│-- results/ # Output results (optional)


## ⚙️ Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/omr-evaluation.git
   cd omr-evaluation
2. Install dependencies By entering command
  ---pip install -r requirements.txt

3. Run app.py file locally
   ---python app.py
