import os
import fitz  # PyMuPDF
from crewai import Agent, Task, Crew, Process
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import letter
from reportlab.lib.enums import TA_LEFT

os.environ["GROQ_API_KEY"] = "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"
llm = ChatGroq(model="llama3-8b-8192")

# ========== Utility ==========
def load_pdf_text(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text.strip()

# ========== Summary ==========
def generate_summary(resume_text, role, style):
    llm = ChatGroq(model="llama3-8b-8192")

    prompt_template = PromptTemplate.from_template(
        "You are a recruiter writing a {style}-style summary for a resume.\n"
        "Role: {role}\n\n"
        "Resume:\n{resume_text}\n\n"
        "Write a role-specific summary."
    )

    chain = prompt_template | llm
    return chain.invoke({"resume_text": resume_text, "role": role, "style": style})

# ========== JD Comparison ==========
def run_crew_comparison(resume_text, jd_text):
    llm = ChatGroq(model="groq/llama3-8b-8192")
    HR = Agent(
        role="Skill Comparator",
        goal="Accurately compare resume with JD and list matching, missing, and extra skills",
        backstory="You're a recruitment expert skilled at parsing resumes and job descriptions.",
        verbose=True,
        llm=llm
    )

    HR_task = Task(
        description="You are given a job description and a candidate's resume.\n\n"
                    "--- JOB DESCRIPTION ---\n"
                    f"{jd_text}\n\n"
                    "--- RESUME ---\n"
                    f"{resume_text}\n\n"
                    "Compare both and return:\n"
                    "1. Matching Skills\n"
                    "2. Missing Skills\n"
                    "3. Extra Skills\n"
                    "Format clearly and professionally.",
        expected_output="A professional comparison including:\n"
                        "1. Matching Skills\n"
                        "2. Missing Skills\n"
                        "3. Extra Skills",
        agent=HR
    )

    Reviewer_task = Task(
        description="Review the Compared Skills",
        expected_output="A detailed skill comparison between JD and Resume",
        agent=HR
    )

    crew = Crew(
        agents=[HR],
        tasks=[HR_task, Reviewer_task],
        process=Process.sequential
    )

    return crew.kickoff()

# ========== PDF Export ==========
def export_combined_pdf(summary, comparison, filename="final_output.pdf"):
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
    from reportlab.lib.units import inch

    doc = SimpleDocTemplate(filename, pagesize=letter,
                            rightMargin=50, leftMargin=50,
                            topMargin=50, bottomMargin=50)

    styles = getSampleStyleSheet()
    body_style = ParagraphStyle(
        name='BodyStyle',
        parent=styles['Normal'],
        fontSize=11,
        leading=14,
        alignment=TA_LEFT
    )

    elements = []

    # Role-Specific Summary Section
    elements.append(Paragraph("<b>ROLE-SPECIFIC SUMMARY:</b>", styles['Heading2']))
    for line in summary.strip().split("\n"):
        elements.append(Paragraph(line.strip(), body_style))
        elements.append(Spacer(1, 0.1 * inch))

    # JD vs Resume Comparison Section
    elements.append(Spacer(1, 0.2 * inch))
    elements.append(Paragraph("<b>JD vs RESUME COMPARISON:</b>", styles['Heading2']))
    for line in str(comparison).strip().split("\n"):
        elements.append(Paragraph(line.strip(), body_style))
        elements.append(Spacer(1, 0.1 * inch))

    doc.build(elements)
    print(f" PDF exported successfully to '{filename}' with proper text wrapping.")

# ========== Main Test ==========
def run_crew_summary(resume_path, jd_path, role, style):
    resume_text = load_pdf_text(resume_path)
    jd_text = load_pdf_text(jd_path)
    summary_result = generate_summary(resume_text, role, style)
    comparison_result = run_crew_comparison(resume_text, jd_text)
    export_combined_pdf(summary_result.content, str(comparison_result))
    return summary_result.content, str(comparison_result)

# === Test Runner ===
if __name__ == "__main__":
    summary, comparison = run_crew_summary(
        resume_path="Sample_Resume.pdf",
        jd_path="Sample_Job_Description.pdf",
        role="Data Analyst",
        style="Recruiter"
    )
    print("\n--- ROLE-SPECIFIC SUMMARY ---\n", summary)
    print("\n=== FINAL COMPARISON ===\n", comparison)