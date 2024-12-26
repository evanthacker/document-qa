import streamlit as st
from openai import OpenAI
import pandas as pd
import docx2txt  # For Word files
import PyPDF2  # For PDF files
from PIL import Image

# Load the image
image = Image.open('SCAMPI - Legacy Inventory Intelligence System.png')

# Display the image (using use_container_width)
st.image(image, use_container_width=True)  

# Show title and description.
st.title("SCAMPI: Legacy Inventory Intelligence System")
st.write(
    "Upload a document (.txt, .md, .csv, .xlsx, .docx, .pdf) below and ask a question about it. A custom artificial intelligence (A.I.) large language model (LLM) model will answer!"
)


# Access the OpenAI API key from Streamlit secrets
openai_api_key = st.secrets["OPENAI_API_KEY"]

# Create an OpenAI client.
client = OpenAI(api_key=openai_api_key)

# Let the user upload a file via `st.file_uploader`.
uploaded_file = st.file_uploader(
    "Upload a document (.txt, .md, .csv, .xlsx, .docx, .pdf)",
    type=("txt", "md", "csv", "xlsx", "docx", "pdf"),
)

# Ask the user for a question via `st.text_area`.
question = st.text_area(
    "Now ask a question about the document!",
    placeholder="1. Which items have expired warranties?",
    disabled=not uploaded_file,
)

if uploaded_file and question:
    # Process the uploaded file and question.
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
        document = df.to_csv(index=False)
    elif uploaded_file.name.endswith(".xlsx"):
        df = pd.read_excel(uploaded_file)
        document = df.to_csv(index=False)
    elif uploaded_file.name.endswith(".docx"):
        document = docx2txt.process(uploaded_file)
    elif uploaded_file.name.endswith(".pdf"):
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        document = ""
        for page in pdf_reader.pages:
            document += page.extract_text()
    else:
        document = uploaded_file.read().decode()

    messages = [
        {
            "role": "user",
            "content": f"Here's a document: {document} \n\n---\n\n {question}",
        }
    ]

    # Generate an answer using the OpenAI API.
    stream = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        stream=True,
    )

    # Stream the response to the app using `st.write_stream`.
    st.write_stream(stream)