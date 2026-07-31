import streamlit as st
from Bio import SeqIO
from Bio.Seq import Seq
from io import StringIO
import matplotlib.pyplot as plt

# Page setup
st.set_page_config(page_title="LAB AI - Year 1 Bioinfo", layout="wide")
st.title("🧬 My Bioinfo Project - LAB AI Year 1")
st.caption("Borys Jones | Year 1 | Kirinyaga University | For ICIPE Attachment")

# LAB AI chat memory
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi! I'm LAB AI, built for Year 1 students. I can help you understand GC%, DNA, and ICIPE lab work. Ask me anything!"}
    ]
if "last_gc" not in st.session_state:
    st.session_state.last_gc = 0

# 3 Simple Tabs for Year 1
tab1, tab2, tab3 = st.tabs(["1. DNA Analyzer", "2. My Lab Video", "3. LAB AI Help"])

with tab1:
    st.subheader("Simple DNA Analyzer - Year 1 Level")
    st.write("This tool is for analyzing malaria DNA (AT-rich).")
    
    # Simple default - easy to explain
    default = """>My_Sample_Kayole
ATGCAAATATATATGCAAGATATATATATATATGCAAATATAT"""
    
    seq_input = st.text_area("Paste your FASTA here:", default, height=120)
    
    if st.button("Analyze", type="primary"):
        # Simple analysis - Year 1 can explain
        records = list(SeqIO.parse(StringIO(seq_input), "fasta"))
        for rec in records:
            s = str(rec.seq).upper()
            length = len(s)
            g = s.count("G")
            c = s.count("C")
            a = s.count("A")
            t = s.count("T")
            gc = (g + c) / length * 100
            
            st.session_state.last_gc = gc
            
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Length", length)
            col2.metric("GC%", f"{gc:.1f}%")
            col3.metric("AT%", f"{100-gc:.1f}%")
            col4.metric("A count", a)
            
            st.info(f"My result: GC is {gc:.1f}% - This is low because malaria is AT-rich. ICIPE taught us this.")
            
            # Simple bar chart
            fig, ax = plt.subplots()
            ax.bar(["A","T","G","C"], [a,t,g,c], color=["green","red","blue","orange"])
            ax.set_title("Base Count - Simple Year 1 Plot")
            st.pyplot(fig)
            
            # Reverse complement - Year 1 topic
            seq_obj = Seq(s)
            st.write(f"Original: {s[:30]}...")
            st.write(f"Reverse Complement: {seq_obj.reverse_complement()[:30]}...")

with tab2:
    st.subheader("My Lab Skills - Video")
    st.write("Upload your lab work to show ICIPE you have hands-on skills.")
    
    # Simple YouTube for learning
    st.video("https://www.youtube.com/watch?v=2KoLnIwoZKU")
    st.caption("Learning PCR - Year 1")
    
    # Your upload
    vid = st.file_uploader("Upload your own lab video (optional)", type=["mp4","mov"])
    if vid:
        st.video(vid)
        st.success("Your video added!")

with tab3:
    st.subheader("LAB AI - Ask for Help (Year 1 Friendly)")
    st.write("LAB AI will answer in simple Year 1 language.")
    
    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])
    
    prompt = st.chat_input("Ask LAB AI: What is GC%? Why AT-rich?")
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            low = prompt.lower()
            gc = st.session_state.last_gc
            
            if "gc" in low:
                resp = f"Good question! Your GC is {gc:.1f}%. GC% is how much G and C you have. Malaria has low GC (14%) because it is AT-rich. In Year 1 we learn this is for immune evasion. You can tell ICIPE this!"
            elif "pcr" in low:
                resp = "PCR in Year 1: 1. Denature at 95C, 2. Anneal at 55C, 3. Extend at 72C. For malaria, annealing 55C works. Keep primers cold!"
            elif "icipe" in low:
                resp = "For ICIPE interview (Year 1): Say 'I built a simple GC analyzer with LAB AI. It shows malaria is AT-rich. I am Year 1 but I learned this from Kayole to Duduville lab.' They will like your honesty."
            else:
                resp = f"LAB AI: I am here to help Year 1 students. You asked '{prompt}'. Your GC is {gc:.1f}%. Keep it simple for ICIPE - explain GC, length, and AT-rich."
            
            st.markdown(resp)
            st.session_state.messages.append({"role": "assistant", "content": resp})

st.sidebar.title("Year 1 Project")
st.sidebar.success("Simple & Explainable")
st.sidebar.markdown("""
**What I built:**
- FASTA reader
- GC% calculator
- Base counter
- Bar chart
- Reverse complement
- Video upload
- LAB AI helper

**Year 1 level - I can explain all**
""")
st.sidebar.info("Borys Jones - Kayole")
