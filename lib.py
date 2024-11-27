import os
from langchain_community.document_loaders import PDFMinerLoader
from langchain.text_splitter import CharacterTextSplitter

def load_chunk_pdf(pdf_file):
    print("Loading " + pdf_file)
    # Load the PDF file
    loader = PDFMinerLoader(pdf_file)
    documents = loader.load()

    # Split the documents into chunks
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    chunked_documents = text_splitter.split_documents(documents)

    return chunked_documents
