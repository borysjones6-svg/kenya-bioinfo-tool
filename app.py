import streamlit as st
from Bio import SeqIO
from Bio.Seq import Seq
from Bio import Restriction
from io import StringIO
import matplotlib.pyplot as plt
import re

st.set_page_config(page_title="LAB AI V6.3", layout="wide")
st.title("KENYA BIOINFO V6.3 - LAB AI MEGA FIXED")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "LAB AI V6.3 online - all syntax fixed"}]
if "last_gc" not in st.session_state:
    st.session_state.last_gc = 14.5
if "last_seq" not in st.session_state:
    st.session_state.last_seq = "ATGCAAATATATATGCAA"

tab1, tab2, tab3, tab4, tab5 = st.tabs(["Analyzer", "Primer", "Plots", "Videos", "LAB AI"])

with tab1:
    f = st.file_uploader("Upload FASTA", type=["fa","fasta","txt"])
    default = """>PF3D7_Kenya
ATGCAAATATATATGCAAGATATATATATATATGCAAATATATATATATGTTTTTT
>Anopheles_Kayole
ATGCGTTATATATATGCAAGATATATATATATATGCAAATATATATATATGAAAAA"""
    seq_input = f.read().decode() if f else st.text_area("Paste:", default, height=150)
    motif = st.text_input("Motif", "ATG")
    window = st.slider("Window", 5, 100, 20)

    if st.button("RUN ALL", type="primary"):
        records = list(SeqIO.parse(StringIO(seq_input), "fasta"))
        table=[]
        for rec in records:
            s = str(rec.seq).upper()
            g_count = s.count('G')
            c_count =
