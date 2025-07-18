import streamlit as st
from AI_HR import load_pdf_text, generate_summary, run_crew_comparison, export_combined_pdf
import os

st.set_page_config(page_title="AI Resume Summarizer", layout="wide")
st.title("🤖 AI Resume Summarizer & JD Comparator")

st.markdown("""
Upload your **Resume** and **Job Description (JD)** PDFs to generate:
- A role-specific professional summary
- Skill comparison (Matching, Missing, Extra skills)
- Downloadable PDF report
""")

# --- File Uploads ---
resume_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
jd_file = st.file_uploader("Upload Job Description (PDF)", type=["pdf"])

# --- Selectors ---
role = st.text_input("Target Role", value="Data Analyst")
style = st.selectbox("Summary Style", ["Recruiter", "HR", "Technical Lead"])

# --- Process Button ---
if st.button("Generate Summary and Compare Skills"):
    if resume_file is not None and jd_file is not None:
        # Save temp files
        with open("resume_temp.pdf", "wb") as f:
            f.write(resume_file.read())
        with open("jd_temp.pdf", "wb") as f:
            f.write(jd_file.read())

        try:
            with st.spinner("Processing..."):
                # Extract Text
                resume_text = load_pdf_text("resume_temp.pdf")
                jd_text = load_pdf_text("jd_temp.pdf")

                # Summary
                result_summary = generate_summary(resume_text, role, style)
                st.subheader("📄 Role-Specific Summary")
                st.markdown(result_summary.content)

                # Comparison
                result_comparison = run_crew_comparison(resume_text, jd_text)
                st.subheader("🧠 JD vs Resume Skill Comparison")
                st.markdown(result_comparison)

                # Export to PDF
                export_combined_pdf(result_summary.content, result_comparison, "final_output.pdf")
                with open("final_output.pdf", "rb") as f:
                    st.download_button("📥 Download Report", f, file_name="AI_Resume_Report.pdf")

        except Exception as e:
            st.error(f"⚠️ Something went wrong: {e}")
    else:
        st.warning("📌 Please upload both Resume and JD files.")
