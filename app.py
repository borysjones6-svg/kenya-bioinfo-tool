import streamlit as st
from Bio import SeqIO
from Bio.Seq import Seq
from Bio import Restriction
from io import StringIO
import matplotlib.pyplot as plt
import re

st.set_page_config(page_title="LAB AI Bioinfo V6 ULTIMATE", layout="wide", page_icon="🧬")
st.title("🧬 KENYA BIOINFO V6 ULTIMATE - LAB AI MEGA SUITE")
st.caption("Borys Jones | Kayole | Built for ICIPE, ILRI, KEMRI - All-in-One")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "LAB AI V6 online 🧬🔬. I now have 12 tools: Analyzer, Primer Design, Restriction Map, ORF, Phylogeny, GC Skew, Codon Usage, BLAST, Videos. Paste your FASTA and tell me what to run!"}]
if "last_gc" not in st.session_state: st.session_state.last_gc = 14.5
if "last_seq" not in st.session_state: st.session_state.last_seq = "ATGCAAATATATATGCAA"

tab1, tab2, tab3, tab4, tab5 = st.tabs(["🧬 MEGA Analyzer", "🧪 Primer & Enzymes", "📈 Advanced Plots", "🎥 Lab Videos", "🤖 LAB AI V6"])

with tab1:
    f = st.file_uploader("Upload FASTA/FASTQ", type=["fa","fasta","fastq","txt"], key="f6")
    default = """>PF3D7_Kenya_Chr1\nATGCAAATATATATGCAAGATATATATATATATGCAAATATATATATATGTTTTTTAAATAG\n>Anopheles_gambiae_COI_Kayole\nATGCGTTATATATATGCAAGATATATATATATATGCAAATATATATATATGAAAAATAG\n>ILRI_Trypanosoma_Kenya\nATGCAAATATATGCAAGATATATATATATATGCAAATATATATATGTTTTTGTAA"""
    seq_input = f.read().decode() if f else st.text_area("Paste multi-FASTA (3 sequences for demo):", default, height=180)

    c1,c2,c3,c4 = st.columns(4)
    motif_search = c1.text_input("Motif", "ATG")
    min_orf = c2.number_input("Min ORF length", 10, 500, 30)
    window = c3.slider("GC Window", 5, 100, 20)
    c4.metric("LAB AI", "READY")

    if st.button("🚀 RUN ALL 12 TOOLS", type="primary"):
        try:
            records = list(SeqIO.parse(StringIO(seq_input), "fasta"))
            table=[]
            for rec in records:
                s=str(rec.seq).upper()
                gc=(s.count('G')+s.count('C'))/len(s)*100 if s else 0
                table.append([rec.id, len(s), f"{gc:.1f}%", s.count(motif_search), s.count('N'), f"{s[:10]}...{s[-10:]}"])
                st.session_state.last_gc=gc; st.session_state.last_seq=s

            st.subheader("📊 1. Summary Table")
            st.dataframe(table, use_container_width=True)

            st.subheader("📊 2. GC% Comparison")
            fig, ax = plt.subplots(); ax.bar([t[0][:15] for t in table], [float(t[2][:-1]) for t in table], color=["#2E86AB","#A23B72","#F18F01"]); st.pyplot(fig)

            st.subheader("🧬 3. Translation (All 3 Frames)")
            for rec in records[:1]:
                seq_obj = Seq(str(rec.seq))
                for i in range(3):
                    st.code(f"Frame {i+1}: {seq_obj[i:].translate()[:100]}")

        except Exception as e:
            st.error(f"Error: {e}")

with tab2:
    st.subheader("🧪 Primer Designer + Restriction Enzymes")
    dna = st.text_input("DNA for primer design:", st.session_state.last_seq[:200], key="primer")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Primer Stats**")
        if len(dna)>0:
            gc_p = (dna.upper().count('G')+dna.upper().count('C'))/
