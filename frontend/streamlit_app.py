import streamlit as st
import requests

st.set_page_config(page_title="PDF Chatbot", layout="centered")

API_URL = "http://localhost:8000"  # FastAPI backend

st.title("📄 Chat with your PDF")

# Upload PDF
with st.expander("📤 Upload your PDF"):
    uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])
    if uploaded_file and st.button("Upload and Index"):
        with st.spinner("Uploading and indexing..."):
            files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}
            res = requests.post(f"{API_URL}/upload", files=files)
            if res.status_code == 200:
                st.success(res.json()["message"])
            else:
                st.error("Failed to upload file.")

# Ask questions
st.subheader("💬 Ask a question")
question = st.text_input("Your question")

if st.button("Ask"):
    if question:
        with st.spinner("Thinking..."):
            res = requests.post(f"{API_URL}/ask", data={"question": question})
            if res.status_code == 200:
                st.markdown("### 🧠 Answer:")
                st.write(res.json()["answer"])
            else:
                st.error("Something went wrong with the backend.")
    else:
        st.warning("Please enter a question.")
