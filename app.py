import streamlit as st
from Bio import SeqIO
from Bio.Seq import Seq
from Bio import Restriction
from io import StringIO
import matplotlib.pyplot as plt
import re

st.set_page_config(page_title="LAB AI V6.4", layout="wide")
st.title("KENYA BIOINFO V6.4 - LAB AI MEGA")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "LAB AI V6.4 online - fixed"}]
if "last_gc" not in st.session_state:
    st.session_state.last_gc = 14.5
if "last_seq" not in st.session_state:
    st.session_state.last_seq = "ATGCAAATATATATGCAA"

tab1, tab2, tab3, tab4, tab5 = st.tabs(["Analyzer", "Primer", "Plots", "Videos", "LAB AI"])

with tab1:
    f = st.file_uploader("Upload FASTA", type=["fa","fasta","txt"])
    default_seq = """>PF3D7
ATGCAAATATATATGCAAATATATATATATATGCAA
>Anopheles
ATGCGTTATATATATGCAAGATATATATATATATGAAAAA"""
    seq_input = default_seq
    if f is not None:
        seq_input = f.read().decode()
    else:
        seq_input = st.text_area("Paste:", default_seq, height=150)

    motif = st.text_input("Motif", "ATG")
    window = st.slider("Window", 5, 100, 20)

    if st.button("RUN ALL", type="primary"):
        records = list(SeqIO.parse(StringIO(seq_input), "fasta"))
        table = []
        for rec in records:
            s = str(rec.seq).upper()
            g_count = s.count("G")
            c_count = s.count("C")
            gc = 0
            if len(s) > 0:
                gc = (g_count + c_count) / len(s) * 100
            short = s[0:10] + "..." + s[-10:]
            count_motif = s.count(motif)
            table.append([rec.id, len(s), round(gc,1), count_motif, short])
            st.session_state.last_gc = gc
            st.session_state.last_seq = s
        st.dataframe(table)
        fig, ax = plt.subplots()
        ids = [t[0][:15] for t in table]
        gcs = [t[2] for t in table]
        ax.bar(ids, gcs)
        st.pyplot(fig)

with tab2:
    st.subheader("Primer Designer")
    dna_input = st.session_state.last_seq[:200]
    dna = st.text_input("DNA:", dna_input)
    if len(dna) > 0:
        upper = dna.upper()
        g = upper.count("G")
        c = upper.count("C")
        a = upper.count("A")
        t_count = upper.count("T")
        gc_p = 0
        if len(dna) > 0:
            gc_p = (g + c) / len(dna) * 100
        tm = 4 * (g + c) + 2 * (a + t_count)
        st.metric("Length", len(dna))
        st.metric("GC%", f"{gc_p:.1f}%")
        st.metric("Tm", f"{tm}C")
        fwd = dna[:20]
        st.write(f"Fwd: {fwd}")
        rev_part = dna[-20:]
        rev_seq = Seq(rev_part)
        rev_comp = rev_seq.reverse_complement()
        st.write(f"Rev: {rev_comp}")

    st.markdown("Restriction Map")
    if len(dna) > 10:
        batch = Restriction.RestrictionBatch(["EcoRI","BamHI","HindIII"])
        seq_obj = Seq(dna)
        result = batch.search(seq_obj)
        for enz in result:
            sites = result[enz]
            if len(sites) == 0:
                st.write(f"{enz}: No cut")
            else:
                st.write(f"{enz}: {sites}")

    pattern = st.text_input("Regex", "ATGC.*TAA")
    if st.button("Find"):
        matches = re.findall(pattern, st.session_state.last_seq)
        st.write(matches[:5])

with tab3:
    s = st.session_state.last_seq
    if len(s) > 20:
        gc_skew = []
        i = 0
        while i < len(s) - window:
            win = s[i:i+window]
            g = win.count("G")
            c = win.count("C")
            total = g + c
            skew = 0
            if total > 0:
                skew = (g - c) / total
            gc_skew.append(skew)
            i = i + window
        fig2, ax2 = plt.subplots()
        ax2.plot(gc_skew)
        st.pyplot(fig2)

with tab4:
    lib = {"DNA Extraction": "https://www.youtube.com/watch?v=5G0P3ZQ1W7E", "PCR": "https://www.youtube.com/watch?v=2KoLnIwoZKU"}
    sel = st.selectbox("Protocols:", list(lib.keys()))
    st.video(lib[sel])
    v = st.file_uploader("Upload video", type=["mp4","mov","avi"])
    if v:
        st.video(v)

with tab5:
    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])
    prompt = st.chat_input("Ask LAB AI...")
    if prompt:
        st.session_state.messages.append({"role":"user","content":prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            gc = st.session_state.last_gc
            resp = f"LAB AI: GC {gc:.1f}% - AT-rich Kenya malaria signature."
            st.markdown(resp)
            st.session_state.messages.append({"role":"assistant","content":resp})

st.sidebar.success("V6.4 - Fixed")
