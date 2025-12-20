import streamlit as st
from backend import transcribe_and_summarize

# Page Config
st.set_page_config(page_title="AI Podcast Summarizer", page_icon="🎙️")
st.title("🎙️ AI Podcast Summarizer")
st.markdown("Upload your podcast audio and get a structured summary using **Whisper** and **Gemini**.")

# 1. File Uploader
audio_file = st.file_uploader("Upload Podcast Audio", type=["mp3", "wav", "m4a"])

if audio_file:
    # 2. Trigger processing on button click
    if st.button("Start Analysis"):
        with st.spinner("Transcribing audio and generating key points..."):
            try:
                # Call the backend
                result = transcribe_and_summarize(audio_file)
                analysis = result["analysis"]

                # 3. Display the Results
                st.success("Analysis Complete!")
                
                # Summary Section
                st.header("📌 Executive Summary")
                st.write(analysis.summary)

                # Key Points Section
                st.header("💡 Key Takeaways")
                for point in analysis.key_points:
                    st.write(f"• {point}")

                # Action Items Section
                if analysis.action_items:
                    st.header("🚀 Action Items")
                    for item in analysis.action_items:
                        st.write(f"✅ {item}")

                # Expandable Transcript
                with st.expander("📄 View Full Transcript"):
                    st.write(result["transcript"])

            except Exception as e:
                st.error(f"An error occurred: {e}")