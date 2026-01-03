import os
import tempfile
import whisper
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import List, Union
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
import yt_dlp

load_dotenv()

# 1. Define the structure for the AI's output
class PodcastAnalysis(BaseModel):
    summary: str = Field(description="A 2-sentence overview of the podcast.")
    key_points: List[str] = Field(description="List of 5-8 most important takeaways.")
    action_items: List[str] = Field(description="Specific recommendations or resources mentioned.")

def download_youtube_audio(youtube_url):
    """
    Download audio from YouTube video and save to temporary file.
    Returns the path to the downloaded audio file.
    """
    temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    temp_path = temp_audio.name
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': temp_path.replace('.mp3', ''),
        # Add proper headers to prevent HTTP 403 Forbidden errors
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0',
        },
        # Additional options to handle YouTube restrictions
        'nocheckcertificate': True,
        'no_warnings': True,
        'quiet': True,
        'no_color': True,
        'geo_bypass': True,  # Bypass geographic restrictions
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])
    
    return temp_path

def transcribe_and_summarize(uploaded_file_or_url):
    """
    Transcribe and summarize audio from either uploaded file or YouTube URL.
    """
    # Check if input is a YouTube URL
    youtube_domains = ['youtube.com', 'youtu.be', 'www.youtube.com']
    is_youtube = any(domain in str(uploaded_file_or_url) for domain in youtube_domains)
    
    if is_youtube:
        # Download from YouTube
        temp_path = download_youtube_audio(uploaded_file_or_url)
    else:
        # Handle uploaded file (existing logic)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
            temp_audio.write(uploaded_file_or_url.getvalue())
            temp_path = temp_audio.name

    try:
        # Step B: Local Transcription with Whisper (Free)
        # Using 'base' model for a good balance of speed and accuracy
        model = whisper.load_model("base")
        result = model.transcribe(temp_path)
        transcript_text = result["text"]

        # Step C: Summarization with Gemini (Free Tier)
        llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0, api_key=os.getenv("GEMINI_API_KEY"))
        structured_llm = llm.with_structured_output(PodcastAnalysis)

        prompt = ChatPromptTemplate.from_template("""
        You are an expert podcast analyst. Extract the main insights from the following transcript.
        
        Transcript:
        {transcript}
        """)

        chain = prompt | structured_llm
        analysis = chain.invoke({"transcript": transcript_text})

        return {
            "transcript": transcript_text,
            "analysis": analysis
        }

    finally:
        # Step D: Cleanup the temporary file from your disk
        if os.path.exists(temp_path):
            os.remove(temp_path)
