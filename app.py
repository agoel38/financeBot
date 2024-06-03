import streamlit as st
from main import extract_text_from_pdf, analyze_financial_document, create_chain

def main():
    st.title("Financial Document Analyzer")

    api_key = st.text_input("Enter your OpenAI API Key", type="password")
    uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

    if api_key and uploaded_file:
        with st.spinner("Extracting text from PDF..."):
            text = extract_text_from_pdf(uploaded_file)

        chain = create_chain(api_key)
        
        with st.spinner("Analyzing the document..."):
            summary = analyze_financial_document(text, chain)

        st.subheader("Summary of the financial document:")
        st.write(summary)

if __name__ == "__main__":
    main()
