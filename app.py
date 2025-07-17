import streamlit as st
from extract_text import extract_text_from_pdf, extract_text_from_docx
from parsing import extract_name, extract_email, extract_phone, extract_skills, extract_job_title

st.set_page_config(page_title="AI Resume Parser", page_icon="🧠")
st.title("🧠 AI Resume Parser")

st.markdown("Upload a resume and (optionally) a job description to extract and compare skills.")

# Upload Resume
uploaded_resume = st.file_uploader("📄 Upload Resume", type=["pdf", "docx"], key="resume")

# Upload Job Description (Optional)
uploaded_jd = st.file_uploader("📑 Upload Job Description (Optional)", type=["pdf", "docx"], key="jd")

if uploaded_resume is not None:
    file_type = uploaded_resume.name.split('.')[-1]

    if file_type == "pdf":
        resume_text = extract_text_from_pdf(uploaded_resume)
    elif file_type == "docx":
        resume_text = extract_text_from_docx(uploaded_resume)
    else:
        st.error("Unsupported resume file type.")
        st.stop()

    # Extract information from resume
    name = extract_name(resume_text) or "Not Found"
    email = extract_email(resume_text) or "Not Found"
    phone = extract_phone(resume_text) or "Not Found"
    resume_skills = extract_skills(resume_text)
    job_title = extract_job_title(resume_text)

    # Display extracted info
    st.subheader("📌 Extracted Resume Info")
    st.write(f"**Name:** {name}")
    st.write(f"**Email:** {email}")
    st.write(f"**Phone:** {phone}")
    st.write(f"**Job Role:** {job_title}")
    st.write(f"**Skills:** {', '.join(resume_skills) if resume_skills else 'None'}")

    # If job description is uploaded
    if uploaded_jd is not None:
        jd_type = uploaded_jd.name.split('.')[-1]

        if jd_type == "pdf":
            jd_text = extract_text_from_pdf(uploaded_jd)
        elif jd_type == "docx":
            jd_text = extract_text_from_docx(uploaded_jd)
        else:
            st.warning("Unsupported job description file type.")
            st.stop()

        jd_skills = extract_skills(jd_text)

        # Skill matching
        matched = set(resume_skills) & set(jd_skills)
        missing = set(jd_skills) - set(resume_skills)
        match_percent = round(len(matched) / len(jd_skills) * 100, 2) if jd_skills else 0

        st.subheader("🔍 Job Description Match")
        st.write(f"**Match:** {match_percent}%")
        st.write(f"✅ Matching Skills:** {', '.join(matched) if matched else 'None'}")
        st.write(f"❌ Missing Skills:** {', '.join(missing) if missing else 'None'}")
