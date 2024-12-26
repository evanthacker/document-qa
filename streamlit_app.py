import streamlit as st
from openai import OpenAI
import pandas as pd

# Show title and description.
st.title("📄 Document question answering")
st.write(
    "Upload a document below and ask a question about it – GPT will answer! "
)

# Access the OpenAI API key from Streamlit secrets
openai_api_key = st.secrets["OPENAI_API_KEY"] 

# Create an OpenAI client.
client = OpenAI(api_key=openai_api_key)

# Let the user upload a file via `st.file_uploader`.
uploaded_file = st.file_uploader(
    "Upload a document (.txt, .md or .csv)", type=("txt", "md", "csv")
)

# Ask the user for a question via `st.text_area`.
question = st.text_area(
    "Now ask a question about the document!",
    placeholder="1.	Which items have expired warranties?",
    disabled=not uploaded_file,
)

if uploaded_file and question:

    # Process the uploaded file and question.
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
        document = df.to_csv(index=False)
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