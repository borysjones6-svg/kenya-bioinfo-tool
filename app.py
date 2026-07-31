import streamlit as st
from Bio import SeqIO
from Bio.Seq import Seq
from Bio import Restriction
from io import StringIO
import matplotlib.pyplot as plt
import re

st.set_page_config(page_title="LAB AI V6.1 ULTIMATE", layout="wide", page_icon="🧬")
st.title("🧬 KENYA BIOINFO V6.1 ULTIMATE - LAB AI MEGA")
st.caption("Borys Jones | Kayole | ICIPE - Fixed")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "LAB AI V6.1 online - 12 tools fixed. No more line 63 error. Ready!"}]
if "last_gc" not in st.session_state:
    st.session_state.last_gc = 14.5
if "last_seq" not in st.session_state:
    st.session_state.last_seq = "ATGCAAATATATATGCAA"

tab1, tab2, tab3, tab4, tab5 = st.tabs(["🧬 MEGA Analyzer", "🧪 Primer & Enzymes", "📈 Advanced Plots", "🎥 Lab Videos", "🤖 LAB AI V6"])

with tab1:
    f = st.file_uploader("Upload FASTA/FASTQ", type=["fa","fasta","fastq","txt"], key="f6")
    default = """>PF3D7_Kenya_Chr1
ATGCAAATATATATGCAAGATATATATATATATGCAAATATATATATATGTTTTTTAAATAG
>Anopheles_gambiae_COI_Kayole
ATGCGTTATATATATGCAAGATATATATATATATGCAAATATATATATATGAAAAATAG
>ILRI_Trypanosoma_Kenya
ATGCAAATATATGCAAGATATATATATATATGCAAATATATATATGTTTTTGTAA"""
    seq_input = f.read().decode() if f else st.text_area("Paste multi-FASTA:", default, height=180)

    c1,c2,c3 = st.columns(3)
    motif_search = c1.text_input("Motif", "ATG")
    min_orf = c2.number_input("Min ORF", 10, 500, 30)
    window = c3.slider("GC Window", 5, 100, 20)

    if st.button("🚀 RUN ALL 12 TOOLS", type="primary"):
        try:
            records = list(SeqIO.parse(StringIO(seq_input), "fasta"))
            table=[]
            for rec in records:
                s = str(rec.seq).upper()
                gc = (s.count('G')+s.count('C'))/len(s)*100 if len(s)>0 else 0
                # FIXED LINE 63 - no nested f-string issue
                short_seq = s[0:10] + "..." + s[-10:]
                table.append([rec.id, len(s), round(gc,1), s.count(motif_search), s.count('N'), short_seq])
                st.session_state.last_gc = gc
                st.session_state.last_seq = s

            st.subheader("1. Summary Table")
            st.dataframe(table, use_container_width=True)

            st.subheader("2. GC% Comparison")
            fig, ax = plt.subplots()
            ids = [t[0][:15] for t in table]
            gcs = [t[2] for t in table]
            ax.bar(ids, gcs, color=["#2E86AB","#A23B72","#F18F01"])
            plt.xticks(rotation=15)
            st.pyplot(fig)

            st.subheader("3. Translation 3 Frames")
            for rec in records[:1]:
                seq_obj = Seq(str(rec.seq))
                for i in range(3):
                    st.code(f"Frame {i+1}: {str(seq_obj[i:].translate())[:100]}")

        except Exception as e:
            st.error(f"Error: {e}")

with tab2:
    st.subheader("Primer Designer + Restriction")
    dna = st.text_input("DNA for primer:", st.session_state.last_seq[:200], key="primer")
    col1, col2 = st.columns(2)
    with col1:
        if len(dna)>0:
            gc_p = (dna.upper().count('G')+dna.upper().count('C'))/len(dna)*100
            tm = 4*(dna.upper().count('G')+dna.upper().count('C')) + 2*(dna.upper().count('A')+dna.upper().count('T'))
            st.metric("Length", len(dna))
            st.metric("GC%", f"{gc_p:.1f}%")
            st.metric("Tm", f"{tm}C")
            st.write(f"Fwd: {dna[:20]}")
            st.write(f"Rev: {str(Seq(dna[-20:]).reverse_com
