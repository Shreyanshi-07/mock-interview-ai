import streamlit as st
import fitz


st.set_page_config(page_title="Mock Interview AI")


st.title("Mock Interview AI")

uploaded_file = st.file_uploader(
    "Upload your resume (PDF only)",
    type=["pdf"]
)


def extract_text_from_pdf(pdf_file):
    text = ""

    pdf_document = fitz.open(stream=pdf_file.read(), filetype="pdf")

    for page in pdf_document:
        text += page.get_text()

    return text


if uploaded_file is not None:

    extracted_text = extract_text_from_pdf(uploaded_file)

    st.subheader("Extracted Resume Text")

    st.text_area(
        "Resume Content",
        extracted_text,
        height=300
    )