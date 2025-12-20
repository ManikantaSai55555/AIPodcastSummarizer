import os
import tempfile
import whisper
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import List
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

# 1. Define the structure for the AI's output
class PodcastAnalysis(BaseModel):
    summary: str = Field(description="A 2-sentence overview of the podcast.")
    key_points: List[str] = Field(description="List of 5-8 most important takeaways.")
    action_items: List[str] = Field(description="Specific recommendations or resources mentioned.")

def transcribe_and_summarize(uploaded_file):
    # Step A: Save the uploaded file to a temporary location
    # Whisper requires a real file path string to work properly.
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
        temp_audio.write(uploaded_file.getvalue())
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