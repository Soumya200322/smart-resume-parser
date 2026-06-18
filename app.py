import streamlit as st
import fitz
import pandas as pd
import re
import os

st.set_page_config(page_title="Smart Resume Parser")

st.title("📄 Smart Resume Parser")

uploaded_file = st.file_uploader(
    "Upload Resume (PDF)",
    type=["pdf"]
)

if uploaded_file:

    pdf = fitz.open(
        stream=uploaded_file.read(),
        filetype="pdf"
    )

    text = ""

    for page in pdf:
        text += page.get_text()

    st.subheader("Resume Text")

    st.text_area(
        "Extracted Content",
        text,
        height=300
    )

    # Email Extraction
    email = re.findall(
    r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}',
    text
)
    

    # Phone Number Extraction
    phone = re.findall(
        r'\+?\d[\d\s\-]{8,}\d',
        text
    )

    # Skills Database
    skills_db = [
        "python",
        "java",
        "sql",
        "mysql",
        "flask",
        "html",
        "css",
        "javascript",
        "git",
        "github",
        "pandas",
        "numpy",
        "streamlit",
        "c",
        "c++",
        "machine learning",
        "data analysis",
        "linux"
    ]

    found_skills = []

    resume_text = text.lower()

    for skill in skills_db:
        if skill in resume_text:
            found_skills.append(skill)

    st.subheader("📧 Email")

    if email:
        for e in email:
            st.success(e)

    else:
        st.error("Email Not Found")

    st.subheader("📱 Phone Number")

    if phone:
        st.success(phone[0])
    else:
        st.error("Phone Number Not Found")

    st.subheader("🛠 Skills Found")

    if found_skills:
        for skill in found_skills:
            st.write("✅", skill.title())
    else:
        st.write("No Skills Found")

    required_skills = [
        "python",
        "sql",
        "flask",
        "git",
        "html"
    ]

    matched = 0

    for skill in required_skills:
        if skill in found_skills:
            matched += 1

    score = (matched / len(required_skills)) * 100

    st.subheader("📊 Resume Score")

    st.progress(int(score))

    st.success(
        f"Resume Score: {score:.0f}%"
    )

    if not os.path.exists("output"):
        os.makedirs("output")

    data = {
        "Email": [email[0] if email else ""],
        "Phone": [phone[0] if phone else ""],
        "Skills": [", ".join(found_skills)],
        "Score": [score]
    }

    df = pd.DataFrame(data)

    df.to_csv(
        "output/resume_output.csv",
        index=False
    )

    st.success(
        "CSV Report Generated Successfully"
    )

    st.download_button(
        label="📥 Download CSV Report",
        data=df.to_csv(index=False),
        file_name="resume_output.csv",
        mime="text/csv"
    )