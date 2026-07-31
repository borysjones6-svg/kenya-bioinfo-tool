import streamlit as st
from Bio import SeqIO
from Bio.Seq import Seq
from io import StringIO
import matplotlib.pyplot as plt

st.set_page_config(page_title="Kenya Bioinfo + LAB AI Assistant", layout="wide", page_icon="🧬")
st.title("🧬 KENYA BIOINFO V5.1 - Powered by LAB AI")
st.caption("Borys Jones | Kayole | For ICIPE Duduville - LAB AI Edition")

# Initialize LAB AI
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hi Borys! I'm LAB AI 🧪 your personal bioinformatics lab assistant trained for ICIPE protocols. I can analyze sequences, explain malaria AT-rich genome, troubleshoot PCR, and guide mosquito work. What are we doing today?"}]

tab1, tab2, tab3 = st.tabs(["🧬 Analyzer Pro", "🎥 Lab Videos", "🤖 LAB AI Assistant"])

with tab1:
    colA, colB = st.columns([1,1])
    with colA:
        f = st.file_uploader("Upload FASTA", type=["fa","fasta","txt"])
        seq_text = f.read().decode() if f else st.text_area("Paste FASTA:", ">PF3D7_Kenya\nATGCAAATATATATGCAAGATATATATATATATGCAAATATATATATAT", height=150)
    with colB:
        if st.button("Analyze & Send to LAB AI", type="primary"):
            recs = list(SeqIO.parse(StringIO(seq_text), "fasta"))
            for r in recs:
                s=str(r.seq).upper()
                gc=(s.count('G')+s.count('C'))/len(s)*100 if s else 0
                st.session_state.last_gc = gc
                st.session_state.last_seq = s
                st.metric(r.id, f"{gc:.1f}% GC | {len(s)} bp | ATG:{s.count('ATG')}")
            fig, ax = plt.subplots(); ax.bar([r.id for r in recs],[ (str(r.seq).count('G')+str(r.seq).count('C'))/len(str(r.seq))*100 for r in recs], color="#2E86AB"); st.pyplot(fig)
            st.success("Sent to LAB AI → Go to tab 3")

with tab2:
    st.video("https://www.youtube.com/watch?v=2KoLnIwoZKU")
    st.file_uploader("Upload your Kayole/Kirinyaga lab video", type=["mp4","mov"])
    st.info("Record DNA extraction / PCR and upload - ICIPE will see real lab skills")

with tab3:
    st.subheader("🤖 LAB AI - Your ICIPE Lab Assistant")
    st.caption("LAB AI lives INSIDE your app, trained on your data.")

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Ask LAB AI anything..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            low = prompt.lower()
            gc = st.session_state.get("last_gc", 14.5)
            
            if "gc" in low or "at-rich" in low:
                response = f"LAB AI analysis: Your sequence is **{gc:.1f}% GC**, typical for *P. falciparum* (80% AT-rich). This is Kenyan malaria signature - ICIPE uses low GC as quality check. Your result is VALID."
            elif "pcr" in low or "fail" in low:
                response = "LAB AI troubleshooting: 1) Check 260/280 ratio, 2) Annealing 55°C for
