import streamlit as st
import requests
from pdfminer.high_level import extract_text
import os

st.title("Resume + JD Matcher 🚀")

# Upload Resume
uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

if uploaded_file is not None:
    with open("uploaded_resume.pdf", "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success("Resume uploaded successfully.")

    # Extract text
    extracted_text = extract_text("uploaded_resume.pdf")
    st.write("✅ Extracted Resume Text:")
    st.text_area("Resume Text (Editable)", extracted_text, key="resume_text", height=300)

# JD input
jd_text = st.text_area("Paste Job Description here")

# Submit button
if st.button("Run Matching"):
    if uploaded_file and jd_text:
        payload = {
            "resume_text": extracted_text,
            "jd_text": jd_text
        }
        try:
            response = requests.post("http://localhost:8080/multiagent_match/", json=payload)
            if response.status_code == 200:
                result = response.json()
                st.success("✅ Matching Completed Successfully")

                # Display overall matching score
                st.metric("Matching Score", f"{result['matching_score']*100:.0f} %")

                # Display total experience
                st.metric("Total Experience", f"{result['total_experience_years']} Years")

                # Display skill gaps clearly
                st.subheader("🛑 Skill Gaps (Missing Skills from Resume):")
                skill_gap = result.get("skill_gap", [])
                if skill_gap:
                    st.error(f"Missing Skills: {', '.join(skill_gap)}")
                else:
                    st.success("No skill gaps found! ✅")

                # Show normalized skills side-by-side
                st.subheader("🎯 Normalized Skills Comparison:")
                col1, col2 = st.columns(2)

                with col1:
                    st.write("Resume Skills:")
                    st.write(result['normalized_resume_skills'])

                with col2:
                    st.write("JD Skills:")
                    st.write(result['normalized_jd_skills'])

                # Display full experience section
                st.subheader("📄 Extracted Professional Experience:")
                experience_list = result.get("experience", [])
                if experience_list:
                    for job in experience_list:
                        st.markdown(f"""
                        **Job Title:** {job.get('job_title', '')}  
                        **Organization:** {job.get('organization', '')}  
                        **Start Date:** {job.get('start_date', '')}  
                        **End Date:** {job.get('end_date', '')}
                        """)
                else:
                    st.warning("No experience section extracted.")

            else:
                st.error("❌ Error from backend!")
        except Exception as e:
            st.error(f"❌ Request failed: {e}")
    else:
        st.warning("⚠ Please upload resume and enter JD first.")

