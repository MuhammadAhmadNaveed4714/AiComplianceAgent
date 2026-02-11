from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.embeddings import HuggingFaceEmbeddings
import traceback

app = FastAPI(title="AI Compliance Agent")
load_dotenv()

print("Loading AI Brain...")
db = None
llm = None

try:
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    db = FAISS.load_local("faiss_index_local", embeddings, allow_dangerous_deserialization=True)
    # Using Lite model
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-lite", temperature=0)
    print("Brain Loaded Successfully!")
except Exception as e:
    print(f"CRITICAL ERROR loading brain: {e}")

class Request(BaseModel):
    text: str

@app.post("/check")
async def check_compliance(request: Request):
    if not db:
        return {"status": "Error", "reason": "Database failed to load."}
    
    try:
        # 1. Search for Rule
        results = db.similarity_search(request.text, k=1)
        if not results:
            return {"status": "Unknown", "reason": "No rule found."}
        
        matched_rule = results[0].page_content
        
        # 2. Ask Gemini
        prompt = f"""
        You are a Compliance Officer.
        Contract Clause: "{request.text}"
        Company Policy: "{matched_rule}"
        Task: Does the clause violate the policy? Answer COMPLIANT or VIOLATION.
        If VIOLATION, explain why nicely.
        """
        
        try:
            response = llm.invoke(prompt)
            ai_analysis = response.content
            source = "Google Gemini AI"
        except Exception as ai_error:
            # --- SMART SIMULATION LOGIC ---
            print(f"Google AI Failed: {ai_error}")
            source = "Simulation (Google Quota Exceeded)"
            
            clause_lower = request.text.lower()
            
            # Default to COMPLIANT so we don't accidentally flag things
            ai_analysis = "COMPLIANT" 

            # TOPIC 1: PAYMENTS
            # Only apply payment rules if the user mentions "payment", "net", or "terms"
            if "payment" in clause_lower or "net " in clause_lower:
                if "net 45" in clause_lower or "net 30" in clause_lower or "net 15" in clause_lower:
                     ai_analysis = "COMPLIANT"
                else:
                     ai_analysis = "VIOLATION. Payment terms must be explicitly Net 45 or less."
            
            # TOPIC 2: ENCRYPTION
            # Only apply encryption rules if the user mentions "data", "encryption", "security", or "aes"
            elif "encryption" in clause_lower or "aes" in clause_lower or "security" in clause_lower:
                if "aes-256" in clause_lower:
                     ai_analysis = "COMPLIANT"
                else:
                     ai_analysis = "VIOLATION. Policy explicitly requires 'AES-256' encryption."

            # TOPIC 3: LIABILITY
            # Only apply liability rules if the user mentions "liability" or "cap"
            elif "liability" in clause_lower or "cap" in clause_lower:
                if "2x" in clause_lower:
                     ai_analysis = "COMPLIANT"
                else:
                     ai_analysis = "VIOLATION. Policy caps liability at 2x."

        return {
            "status": "Checked",
            "source": source,
            "clause": request.text,
            "matched_policy": matched_rule,
            "ai_analysis": ai_analysis
        }

    except Exception as e:
        return {
            "status": "Crash",
            "error_message": str(e),
            "traceback": traceback.format_exc()
        }