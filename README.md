# 🤖 AI Resume Summarizer & JD Skill Comparator

This project is an **AI-powered Resume Summarizer and Job Description (JD) Skill Comparator**. It analyzes a candidate's resume, generates a role-specific summary, compares it with a provided JD, and exports both into a well-formatted PDF report.

---

## 📌 Features

✅ Generate AI-based summary tailored to any job role  
✅ Compare resume vs job description to identify:
- Matching Skills  
- Missing Skills  
- Extra Skills  

✅ Export the results in a **single professional PDF**  
✅ Built with **LangChain, CrewAI, ChatGroq (LLaMA3)**  
✅ Includes a **Tkinter GUI** (optional) for user interaction  

---

## 🧠 Tech Stack

| Tool / Library       | Purpose                                 |
|----------------------|-----------------------------------------|
| `LangChain`          | Prompt and chain management             |
| `CrewAI`             | Multi-agent orchestration               |
| `ChatGroq + LLaMA3`  | LLM for summarization and comparison    |
| `PyMuPDF (fitz)`     | PDF text extraction                     |
| `ReportLab`          | PDF generation with proper formatting   |
| `Tkinter`            | GUI (optional, see `app.py`)            |

---

## 📂 Project Structure


---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/ai-resume-summarizer.git
cd ai-resume-summarizer
```

### 2. Install the requirements

```bash
pip install -r requirements.txt

```
### 3. Add your GroqAPI Key

Edit AI_HR.py and paste your key:
os.environ["GROQ_API_KEY"] = "your_actual_groq_api_key"

### 4. Running the project

Option 1: Run the backend (AI_HR.py)

```bash
python AI_HR.py

```
This will:
  Load the sample resume and JD
  Generate a summary and comparison
  Export results to final_output.pdf

Optionn 2: Run with GUI

```bash
streamlit run app.py

```
This will:
  Launch a streamlit window
  Allow you to browse and upload resume + JD
  Set job role and style
  Automatically generate and save the PDF report

### Example Output
PDF contains two sections:

Role-Specific Summary

JD vs Resume Skill Comparison
All formatted and wrapped correctly.
