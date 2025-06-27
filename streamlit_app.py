import streamlit as st
import requests
from pdfminer.high_level import extract_text
import pandas as pd

API_URL = "http://localhost:8080"
st.set_page_config(page_title="Resume Matcher", page_icon="📄")
st.title("Resume + JD Matcher 🚀")

mode = st.radio("Choose User Type", ["🎓 Student", "🧑‍💼 Recruiter"])

if mode == "🎓 Student":
    st.subheader("Upload your Resume (PDF) and Paste the Job Description")
    uploaded_file = st.file_uploader("Upload Resume", type="pdf")
    jd_text = st.text_area("Paste Job Description", height=200)

    if st.button("Match Resume to JD"):
        if uploaded_file and jd_text:
            with st.spinner("Extracting text and matching..."):
                try:
                    resume_text = extract_text(uploaded_file)
                    payload = {
                        "resume_text": resume_text,
                        "jd_text": jd_text
                    }

                    response = requests.post(f"{API_URL}/multiagent_match/", json=payload)
                    if response.status_code == 200:
                        result = response.json()

                        # ✅ Display Results
                        st.success("🎯 Match Successful!")
                        st.markdown(f"### 🔢 Matching Score: **{round(result['matching_score'] * 100, 2)}%**")
                        st.markdown(f"### ⏳ Total Experience: **{result['total_experience_years']} years**")

                        # 📂 Experience Breakdown
                        st.markdown("### 📌 Experience Breakdown:")
                        for i, exp in enumerate(result["experience"]):
                            st.markdown(f"""
                                **{i+1}. {exp['job_title']}** at **{exp['organization']}**
                                - Duration: {exp.get('start_date', 'N/A')} to {exp.get('end_date', 'N/A')}
                                - Description: {exp.get('description', '—')}
                            """)

                        # 🛠️ Skill Gap
                        if result['skill_gap']:
                            st.markdown("### ⚠️ Skill Gap Detected:")
                            st.markdown(", ".join(result['skill_gap']))
                        else:
                            st.markdown("### ✅ No Skill Gaps!")

                    else:
                        st.error("❌ Backend error: Could not get results.")

                except Exception as e:
                    st.error(f"❌ Request failed: {e}")
        else:
            st.warning("Please upload your resume and paste the job description.")

elif mode == "🧑‍💼 Recruiter":
    resume_files = st.file_uploader("Upload Multiple Resumes (PDF)", type=["pdf"], accept_multiple_files=True)
    jd_text = st.text_area("Paste Job Description")
    instructions = st.text_area("Optional Recruiter Instructions")

    if st.button("Match Candidates to JD") and resume_files and jd_text:
        resume_data = []
        for file in resume_files:
            resume_text = extract_text(file)
            resume_data.append({
                "filename": file.name,
                "text": resume_text
            })

        payload = {
            "jd_text": jd_text,
            "resumes": resume_data,
            "instructions": instructions
        }

        response = requests.post(f"{API_URL}/recruiter_match/", json=payload)
        if response.ok:
            results = response.json()["matches"]
            st.success("✅ Matching complete!")
            df = pd.DataFrame(results)
            st.dataframe(df)
            st.download_button("Download Report", df.to_csv(index=False), file_name="match_report.csv")
        else:
            st.error("❌ Error from backend!")
