import streamlit as st
from Bio import SeqIO
from io import StringIO
import matplotlib.pyplot as plt

st.set_page_config(page_title="LAB AI Bioinfo", layout="wide")
st.title("🧬 Kenya Bioinfo + LAB AI V5.1")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hi! I'm LAB AI - your lab assistant for ICIPE. Ask me about GC%, PCR, or malaria."}]

tab1, tab2 = st.tabs(["Analyzer", "LAB AI"])

with tab1:
    seq_text = st.text_area("Paste FASTA", ">PF3D7_Kenya\nATGCAAATATATATGCAAATATATATATAT", height=120)
    if st.button("Analyze"):
        try:
            recs = list(SeqIO.parse(StringIO(seq_text), "fasta"))
            for r in recs:
                s=str(r.seq).upper()
                gc=(s.count('G')+s.count('C'))/len(s)*100 if len(s)>0 else 0
                st.session_state.last_gc=gc
                st.write(f"{r.id} | Length {len(s)} | GC {gc:.1f}%")
                fig, ax = plt.subplots()
                ax.bar(["GC%","AT%"],[gc,100-gc])
                st.pyplot(fig)
            st.success("Done - go to LAB AI tab")
        except Exception as e:
            st.error(f"Error: {e} - check FASTA format starts with >")

with tab2:
    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])
    
    if prompt := st.chat_input("Ask LAB AI"):
        st.session_state.messages.append({"role":"user","content":prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            gc = st.session_state.get("last_gc",14.5)
            if "gc" in prompt.lower():
                resp = f"LAB AI: Your GC is {gc:.1f}% - Perfect for P. falciparum, it's AT-rich. ICIPE will love this result."
            else:
                resp = f"LAB AI: Got it '{prompt}'. Based on your GC {gc:.1f}%, this matches Kenyan malaria. Need ICIPE report help?"
            st.markdown(resp)
            st.session_state.messages.append({"role":"assistant","content":resp})
