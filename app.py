import streamlit as st
from Bio import SeqIO
from Bio.Seq import Seq
from io import StringIO
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="LAB AI + My Portfolio Videos", layout="wide")
st.title("🧬 Borys Jones - My School Projects Portfolio")
st.caption("Year 1 Kirinyaga | Kayole | Video Evidence for ICIPE")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hi! I'm LAB AI. I can now show your school projects in video portfolio for ICIPE!"}]
if "last_gc" not in st.session_state:
    st.session_state.last_gc = 0

# For storing your videos
if "portfolio" not in st.session_state:
    st.session_state.portfolio = []

tab1, tab2, tab3 = st.tabs(["1. DNA Analyzer", "2. 🎥 My School Projects [VIDEO PORTFOLIO]", "3. LAB AI"])

with tab1:
    st.subheader("DNA Analyzer")
    default = """>My_Sample_Kayole
ATGCAAATATATATGCAAGATATATATATATATGCAAATATAT"""
    seq_input = st.text_area("Paste FASTA:", default, height=100)
    if st.button("Analyze"):
        records = list(SeqIO.parse(StringIO(seq_input), "fasta"))
        for rec in records:
            s = str(rec.seq).upper()
            gc = (s.count("G")+s.count("C"))/len(s)*100 if len(s)>0 else 0
            st.session_state.last_gc = gc
            st.metric("GC%", f"{gc:.1f}%")
            fig, ax = plt.subplots()
            ax.bar(["GC%","AT%"], [gc, 100-gc])
            st.pyplot(fig)

with tab2:
    st.subheader("🎥 My Accomplished School Projects - Video Evidence")
    st.info("ICIPE will watch these! Upload videos of you doing lab work, presenting, field work.")

    # GUIDE HOW TO CAPTURE
    with st.expander("📱 How to Capture Your Projects in Video - Click to Learn"):
        st.markdown("""
        **How to capture for Year 1 portfolio:**
        
        1. **Use your phone** - Hold horizontal (landscape)
        2. **Show yourself** - Say: "I'm Borys Jones, Year 1, this is my project on..."
        3. **Show process** - Don't just show result, show you pipetting, measuring, plating
        4. **Keep 1-2 minutes** - Short is professional
        5. **Good light** - Near window or lab light
        6. **What to capture:**
           - You extracting DNA in school lab
           - You running PCR / Gel
           - You presenting poster
           - Field work in Kayole / Kirinyaga
           - You explaining your bioinfo tool
        
        **Example intro:** "Hi, I'm Borys from Kirinyaga University Year 1, in Kayole lab, today I'm showing my DNA extraction from..."
        """)

    # ADD NEW PROJECT VIDEO
    st.markdown("### ➕ Add New Project Video")
    col1, col2 = st.columns(2)
    with col1:
        project_title = st.text_input("Project Title", "DNA Extraction - Year 1 Practical")
        project_course = st.selectbox("Course", ["Biochemistry Lab", "Molecular Biology", "Microbiology", "Bioinformatics", "Field Work", "My Bioinfo Tool"])
        project_date = st.date_input("Date Done", datetime.now())
    with col2:
        project_desc = st.text_area("What did you accomplish?", "I extracted DNA from... I learned pipetting, sterile technique. Result was...", height=100)
        video_file = st.file_uploader("Upload Video (MP4, MOV)", type=["mp4","mov","avi"], key="portfolio_vid")

    if st.button("💾 Save to My Portfolio"):
        if video_file and project_title:
            st.session_state.portfolio.append({
                "title": project_title,
                "course": project_course,
                "date": str(project_date),
                "desc": project_desc,
                "video": video_file
            })
            st.success(f"Added {project_title} to portfolio! ICIPE can now see it.")
        else:
            st.error("Add title and video")

    # DISPLAY PORTFOLIO
    st.markdown("---")
    st.subheader(f"📚 My Portfolio - {len(st.session_state.portfolio)} Projects Captured")

    if len(st.session_state.portfolio) == 0:
        st.warning("No videos yet! Upload your first project above. Example: Upload a video of you using your bioinfo tool.")
        # Demo placeholder
        st.video("https://www.youtube.com/watch?v=2KoLnIwoZKU")
        st.caption("Example: This is how your project video should look - you explaining")
    else:
        for i, proj in enumerate(st.session_state.portfolio):
            with st.container(border=True):
                c1, c2 = st.columns([2,1])
                with c1:
                    st.markdown(f"**{i+1}. {proj['title']}**")
                    st.caption(f"{proj['course']} | {proj['date']}")
                    st.write(proj['desc'])
                    st.video(proj['video'])
                with c2:
                    st.metric("Project", proj['course'])
                    st.write("✅ Evidence for ICIPE")
                    # Download project info
                    info = f"Title: {proj['title']}\nCourse: {proj['course']}\nDate: {proj['date']}\nDesc: {proj['desc']}"
                    st.download_button(f"Download Info {i+1}", info, file_name=f"{proj['title']}.txt", key=f"dl{i}")

        # Download full portfolio list
        if st.session_state.portfolio:
            portfolio_csv = pd.DataFrame([{"Title": p["title"], "Course": p["course"], "Date": p["date"]} for p in st.session_state.portfolio]).to_csv(index=False)
            st.download_button("📥 Download Full Portfolio List (CSV)", portfolio_csv, file_name="Borys_Jones_Portfolio.csv")

with tab3:
    st.subheader("LAB AI - Portfolio Helper")
    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])
    
    prompt = st.chat_input("Ask LAB AI how to capture videos")
    if prompt:
        st.session_state.messages.append({"role":"user","content":prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            low = prompt.lower()
            if "video" in low or "captur" in low:
                resp = "To capture: 1) Phone horizontal, 2) Start with your name/year, 3) Show hands doing work, 4) Explain what you learned, 5) Show result. Keep 60-90 sec. Upload in Tab 2. ICIPE loves seeing YOU doing work, not just slides!"
            elif "icipe" in low:
                resp = f"You have {len(st.session_state.portfolio)} videos. Tell ICIPE: 'I documented {len(st.session_state.portfolio)} school projects on video - DNA extraction, bioinfo tool, etc. All in my portfolio tab.' This is stronger than other Year 1s who have only CV."
            else:
                resp = f"LAB AI: You have {len(st.session_state.portfolio)} projects captured. Add more in Tab 2. Year 1 portfolio with video = instant attachment!"
            st.markdown(resp)
            st.session_state.messages.append({"role":"assistant","content":resp})

st.sidebar.success(f"Portfolio: {len(st.session_state.portfolio)} Videos")
st.sidebar.info("ICIPE checks Tab 2 first!")
st.sidebar.markdown("**Tip:** Capture 3 videos today:\n1. You using this bioinfo tool\n2. You in lab coat\n3. You explaining malaria AT-rich")
