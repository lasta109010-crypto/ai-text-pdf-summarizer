import streamlit as st
from openai import OpenAI
from pypdf import PdfReader

client = OpenAI()

st.set_page_config(
    page_title="AI Text & PDF Summarizer",
    layout="centered"
)
# TITL AND TEXT AREA 
st.title("AI Text & PDF Summarizer")

text = st.text_area(
    "Paste text here",
    height=250
)



uploaded_file = st.file_uploader(
    "Upload a PDF",
    type=["pdf"]
)

# Add pdf reader

pdf_text = ""


if uploaded_file is not None:
    reader = PdfReader(uploaded_file)

    for page in reader .pages:
        pdf_text += page.extract_text()

#Add how many pullet point customer wants 

number = st.number_input(
    "How many bullet points do you want?",
    min_value=1,
    max_value=10,
    value=3
)

if st.button("Summarize"):
    final_text = pdf_text if pdf_text.strip() != "" else text

    if final_text.strip() == "":
        st.warning("Please paste some text or upload a PDF.")

    else:
        instructions = f"Summarize the text into exactly {number} bullet points."

        response = client.responses.create(
            model="gpt-4.1-mini",
            instructions=instructions,
            input=final_text
        )

        assistant_reply = response.output_text

        st.subheader("Summary")
        st.write(assistant_reply)

        # QUALITY CONTROL
        quality_response = client.responses.create(
            model="gpt-4.1-mini",
            input=f"""
Evaluate this summary.

Original Text:
{final_text}

Summary:
{assistant_reply}

Return:

Quality Score (0-100)

Strengths

Missing Information
"""
        )

                # QUALITY REPORT

        quality_report = quality_response.output_text

        st.subheader("⭐ AI Quality Analysis")

        st.divider()

        st.write(quality_report)

        original_words = len(final_text.split())

        summary_words = len(assistant_reply.split())

        compression = round(
            (1 - summary_words / original_words) * 100,
            1
        )

        st.subheader("📊 Dashboard")

        st.metric("Original Words", original_words)

        st.metric("Summary Words", summary_words)

        st.metric("Compression", f"{compression}%")






        