import streamlit as st
from Bio import SeqIO
from io import StringIO
import matplotlib.pyplot as plt

st.set_page_config(page_title="Kenya Bioinfo Tool", page_icon="🧬")
st.title("🧬 Kenya Bioinfo Tool - ICIPE Ready")
st.write("Built by Borys Jones from Kayole | Kirinyaga University")

fasta_text = st.text_area("Paste your FASTA sequence here:", height=150, 
value=">PF3D7_test1\nATGCAAATATATATGCAAGATATATATATATATGCAAATATATATAT")

if st.button("Analyze Sequence"):
    for record in SeqIO.parse(StringIO(fasta_text), "fasta"):
        seq = str(record.seq).upper()
        gc = (seq.count('G') + seq.count('C')) / len(seq) * 100 if len(seq)>0 else 0
        atg = seq.count('ATG')
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Sequence", record.id)
        col2.metric("Length", len(seq))
        col3.metric("GC %", f"{gc:.1f}%")
        
        st.write(f"**ATG start codons:** {atg} found")
        
        # Plot
        fig, ax = plt.subplots()
        ax.bar(["GC%", "AT%"], [gc, 100-gc], color=["#2E86AB", "#F18F01"])
        ax.set_ylabel("%")
        ax.set_title(f"GC Content - {record.id}")
        st.pyplot(fig)

st.markdown("---")
st.markdown("GitHub: [borysjones6-svg/kenya-bioinfo-tool](https://github.com/borysjones6-svg/kenya-bioinfo-tool)")
