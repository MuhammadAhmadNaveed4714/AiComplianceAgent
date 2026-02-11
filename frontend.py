import streamlit as st
import requests

st.title("🤖 AI Compliance & Policy Enforcement Agent")
st.write("Upload a contract clause or type it below to check for violations.")

clause_text = st.text_area("Enter Contract Clause:", height=150)

if st.button("Check Compliance"):
    if clause_text:
        with st.spinner("Consulting the AI Compliance Officer..."):
            try:
                response = requests.post("http://127.0.0.1:8000/check", json={"text": clause_text})
                
                if response.status_code == 200:
                    data = response.json()
                    analysis = data.get("ai_analysis", "")
                    
                    # LOGIC FIX: Check explicitly for Violation OR Compliant
                    if "VIOLATION" in analysis.upper():
                        st.error("🚨 VIOLATION DETECTED")
                    elif "COMPLIANT" in analysis.upper():
                        st.success("✅ COMPLIANT")
                    else:
                        # If it's neither (e.g., "Manual Review"), show yellow warning
                        st.warning("⚠️ UNCLEAR / MANUAL REVIEW NEEDED")
                        
                    st.subheader("Analysis:")
                    st.write(analysis)
                    
                    st.divider()
                    st.info(f"🔍 Matched Policy:\n{data.get('matched_policy')}")
                    
                    if "Simulation" in data.get("source", ""):
                        st.caption("⚠️ Note: Running in Simulation Mode (Google Quota Exceeded)")
                else:
                    st.error(f"Error: {response.status_code}")
            except Exception as e:
                st.error(f"Connection Error: Is the backend running? {e}")
    else:
        st.warning("Please enter some text first.")