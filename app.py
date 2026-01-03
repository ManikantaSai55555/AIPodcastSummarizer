import streamlit as st
from backend import transcribe_and_summarize
import re

# Page Config
st.set_page_config(page_title="AI Podcast Summarizer", page_icon="🎙️")
st.title("🎙️ AI Podcast Summarizer")
st.markdown("Enter a YouTube link to get a structured summary using **Whisper** and **Gemini**.")

# 1. YouTube URL Input
youtube_url = st.text_input("Enter YouTube Video URL", placeholder="https://www.youtube.com/watch?v=...")

# Validate YouTube URL
def is_valid_youtube_url(url):
    youtube_regex = r'^(https?\:\/\/)?(www\.)?(youtube\.com|youtu\.?be)\/.+$'
    return re.match(youtube_regex, url) is not None

if youtube_url:
    if not is_valid_youtube_url(youtube_url):
        st.error("Please enter a valid YouTube URL")
    else:
        # 2. Trigger processing on button click
        if st.button("Start Analysis"):
            with st.spinner("Downloading audio, transcribing, and generating key points..."):
                try:
                    # Call the backend
                    result = transcribe_and_summarize(youtube_url)
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
