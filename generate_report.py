
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_google_genai import GoogleChat  # Correct import for Google Gemini

# 1️⃣ Load embeddings and FAISS DB
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
db = FAISS.load_local("faiss_index_local", embeddings, allow_dangerous_deserialization=True)

# 2️⃣ Load document to check
with open("sample_contract.txt", "r") as file:
    document_text = file.read()

# 3️⃣ Retrieve relevant policies
matched_policies = db.similarity_search(document_text, k=3)

violations = []
for policy_doc in matched_policies:
    policy = policy_doc.page_content.lower()
    text = document_text.lower()
    if "net 45" in policy and "45" not in text:
        violations.append("Payment terms do not comply with Net 45 policy.")
    if "aes-256" in policy and "aes-256" not in text:
        violations.append("Cloud data is not encrypted using AES-256.")
    if "2x" in policy and "2x" not in text:
        violations.append("Liability exceeds the allowed 2x contract value.")

# 4️⃣ Generate AI Explanation using Google Gemini
if violations:
    prompt_text = f"""
You are an AI compliance assistant. Analyze the following document and explain in simple terms why it violates company policies.

Document:
{document_text}

Violations:
{violations}

Write a professional report summarizing the issues and recommendations to fix them.
"""
    # ✅ Initialize Google Gemini Chat model
    llm = GoogleChat(model="models/chat-bison-001", temperature=0)

    # ✅ Mini-Test to verify LLM
    test_prompt = "Hello! Are you working?"
    test_response = llm.predict(test_prompt)
    print("Test LLM Response:", test_response)

    # Generate actual compliance report
    report = llm.predict(prompt_text)
    print("\n📄 COMPLIANCE REPORT:\n")
    print(report)
else:
    print("✅ Document is fully compliant. No issues found.")
