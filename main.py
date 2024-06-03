from io import StringIO
from pdfminer.high_level import extract_text_to_fp
from pdfminer.layout import LAParams
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

def extract_text_from_pdf(pdf_file):
    output_string = StringIO()
    extract_text_to_fp(pdf_file, output_string, laparams=LAParams(), output_type='text', codec=None)
    return output_string.getvalue()

def chunk_text(text, max_tokens=3000):
    words = text.split()
    chunks = []
    chunk = []
    chunk_size = 0

    for word in words:
        word_size = len(word) + 1  # Adding 1 for the space
        if chunk_size + word_size > max_tokens:
            chunks.append(' '.join(chunk))
            chunk = []
            chunk_size = 0
        chunk.append(word)
        chunk_size += word_size

    if chunk:
        chunks.append(' '.join(chunk))
    
    return chunks

def analyze_financial_document(text, chain):
    chunks = chunk_text(text)
    summaries = []
    
    for chunk in chunks:
        summary = chain.run({"text": chunk})
        summaries.append(summary)
    
    return "\n".join(summaries)

def create_chain(api_key):
    llm = OpenAI(api_key=api_key)

    template = """
    You are an investment advisor. Analyze the following financial document and provide a summary focusing on key financial metrics such as revenue, profit, and any notable changes or trends.

    Document:
    {text}

    Summary:
    """
    prompt = PromptTemplate(template=template, input_variables=["text"])
    chain = LLMChain(llm=llm, prompt=prompt)
    return chain
