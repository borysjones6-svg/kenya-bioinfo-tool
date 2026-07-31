import streamlit as st
from Bio import SeqIO
from io import StringIO
import matplotlib.pyplot as plt

st.set_page_config(page_title="Kenya Bioinfo Suite", page_icon="🧬", layout="wide")

st.title("🧬 Kenya Bioinfo Suite V2")
st.caption("Built by Borys Jones | Kirinyaga University | Kayole, Nairobi - For ICIPE")

# Sidebar
st.sidebar.header("Settings")
motif = st.sidebar.text_input("Motif to find", "ATG")
uploaded = st.sidebar.file_uploader("Or upload FASTA file", type=["fasta","fa","txt"])

# Main input
default_fasta = """>PF3D7_1 Malaria Kenya
ATGCAAATATATATGCAAGATATATATATATATGCAAATATATATATATGTTTTTT
>Anopheles_gambiae_Kayole
ATGCGTTATATATATGCAAGATATATATATATATGCAAATATATATATATGAAAAA"""

fasta_input = uploaded.read().decode() if uploaded else st.text_area("Paste FASTA:", default_fasta, height=200)

if st.button("🔬 Analyze Now", type="primary"):
    records = list(SeqIO.parse(StringIO(fasta_input), "fasta"))

    if not records:
        st.error("No valid FASTA found")
    else:
        # Stats table
        data = []
        for rec in records:
            seq = str(rec.seq).upper()
            gc = (seq.count('G')+seq.count('C'))/len(seq)*100 if len(seq)>0 else 0
            data.append({"ID": rec.id, "Length": len(seq), "GC%": round(gc,1), motif: seq.count(motif)})

        st.subheader("📊 Results")
        st.dataframe(data, use_container_width=True)

        # Plots
        col1, col2 = st.columns(2)
        with col1:
            fig, ax = plt.subplots()
            ax.bar([d["ID"] for d in data], [d["GC%"] for d in data], color="#2E86AB")
            ax.set_ylabel("GC%"); ax.set_title("GC Content Comparison"); plt.xticks(rotation=10)
            st.pyplot(fig)
        with col2:
            fig2, ax2 = plt.subplots()
            ax2.bar([d["ID"] for d in data], [d[motif] for d in data], color="#A23B72")
            ax2.set_ylabel(f"{motif} count"); ax2.set_title(f"{motif} Motif Count"); plt.xticks(rotation=10)
            st.pyplot(fig2)

        st.success(f"Analyzed {len(records)} sequences | AT-rich = P. falciparum signature")

st.markdown("---")
st.markdown("**For ICIPE Duduville:** This tool predicts ATG start codons and AT-rich malaria genome features. [GitHub](https://github.com/borysjones6-svg/kenya-bioinfo-tool)")
