# 🎙️ AI Podcast Summarizer

An end-to-end AI application that transcribes podcast audio files and generates structured summaries, key takeaways, and action items. This project leverages **OpenAI's Whisper** for high-accuracy local transcription and **Google Gemini 2.0 Flash** for intelligent content analysis.

## ✨ Features
- **Local Transcription:** Uses Whisper (running on your machine) to convert audio to text for free.
- **AI Summarization:** Utilizes Gemini 2.0 Flash to distill long podcasts into concise summaries.
- **Structured Key Points:** Automatically extracts bulleted takeaways and actionable advice.
- **User-Friendly UI:** Built with Streamlit for a clean, interactive experience.
- **Privacy Focused:** Audio files are processed locally and deleted immediately after analysis.

## 🛠️ Tech Stack
- **Frontend:** [Streamlit](https://streamlit.io/)
- **Speech-to-Text:** [OpenAI Whisper](https://github.com/openai/whisper)
- **LLM Orchestration:** [LangChain](https://www.langchain.com/)
- **AI Model:** Google Gemini 2.0 Flash (via Google AI Studio)

---

## 🚀 Getting Started

### 1. Prerequisites
Ensure you have **FFmpeg** installed on your system, as it is required by Whisper to process audio files.
- **macOS:** `brew install ffmpeg`
- **Windows:** `choco install ffmpeg`
- **Linux:** `sudo apt install ffmpeg`

### 2. Installation
Clone the repository and install the dependencies:
```bash
# Clone the repo
git clone [https://github.com/yourusername/podcast-summarizer.git](https://github.com/yourusername/podcast-summarizer.git)
cd podcast-summarizer

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install required packages
pip install -r ./requirements.txt