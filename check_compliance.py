from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

# Load local embeddings
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Load FAISS VectorDB
db = FAISS.load_local(
    "faiss_index_local",
    embeddings,
    allow_dangerous_deserialization=True
)

# Load document to check
with open("sample_contract.txt", "r") as file:
    document_text = file.read()

print("\n📄 Checking document for compliance...\n")

# Retrieve most relevant policies
matched_policies = db.similarity_search(document_text, k=3)

violations = []

for policy_doc in matched_policies:
    policy = policy_doc.page_content.lower()
    text = document_text.lower()

    if "net 45" in policy and "45" not in text:
        violations.append("❌ Payment terms do not comply with Net 45 policy.")

    if "aes-256" in policy and "aes-256" not in text:
        violations.append("❌ Cloud data is not encrypted using AES-256.")

    if "2x" in policy and "2x" not in text:
        violations.append("❌ Liability exceeds the allowed 2x contract value.")

# Output result
if violations:
    print("🚨 COMPLIANCE VIOLATIONS FOUND:\n")
    for v in violations:
        print(v)
else:
    print("✅ Document is fully compliant.")
