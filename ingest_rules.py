print("1. Script Starting...")

import os

from dotenv import load_dotenv

from langchain_community.document_loaders import TextLoader

from langchain_text_splitters import CharacterTextSplitter

from langchain_community.vectorstores import FAISS

# NEW: Import the Local/Free embedding tool

from langchain_community.embeddings import HuggingFaceEmbeddings



load_dotenv()



# 1. Load Policies

print("2. Loading Policy File...")

try:

    loader = TextLoader("company_policies.txt")

    documents = loader.load()

    print(f"   - Loaded {len(documents)} document(s).")

except Exception as e:

    print(f"   - ERROR loading file: {e}")

    exit()



# 2. Split Text

print("3. Splitting Text into Rules...")

text_splitter = CharacterTextSplitter(chunk_size=200, chunk_overlap=0, separator="\n")

docs = text_splitter.split_documents(documents)

print(f"   - Created {len(docs)} individual rules.")



# 3. Create Database (LOCALLY)

print("4. Creating Brain locally (This is free & unlimited)…")

try:

    # We use a small, fast model that runs on your laptop

    # NOTE: On the very first run, this will take 10-30 seconds to download the model.

    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    

    db = FAISS.from_documents(docs, embeddings)

    

    # Save

    print("5. Saving Database to Disk...")

    db.save_local("faiss_index_local")

    print("\nSUCCESS! The Brain is ready in folder 'faiss_index_local'.")



except Exception as e:

    print(f"\nERROR: {e}")