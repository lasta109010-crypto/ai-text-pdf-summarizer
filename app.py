import streamlit as st
from openai import OpenAI
from pypdf import PdfReader

client = OpenAI()

st.set_page_config(
    page_title="AI Text Summarizer",
    layout="centered"
)
# TITL AND TEXT AREA 
st.title("AI Text Summarizer")

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
        st.warning("Please paste some or upload PDF.")

    else:
        instructions = f"Summarize the text into exactly {number} bullet points."

        response = client.responses.create(
            model="gpt-4.1-mini",
            instructions=instructions,
            input= final_text
        )

        st.subheader("Summary")
        st.write(response.output_text)