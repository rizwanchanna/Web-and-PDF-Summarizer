import streamlit as st
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import UnstructuredURLLoader
from langchain.schema import Document
from youtube_transcript_api import YouTubeTranscriptApi
import validators
import re
import PyPDF2
import unicodedata

# Page config
st.set_page_config(page_title="Groq Smart Summarizer", page_icon="🧠", layout="centered")

# Sidebar
st.sidebar.title("🔧 App Settings")

# API Key Input
groq_api_key = st.sidebar.text_input("🔑 Enter your Groq API Key", type="password")

# Navigation
section = st.sidebar.radio(
    "📂 Select Mode",
    options=["🔗 Link Summary", "📄 PDF/Text Summary"],
    index=0
)

# Reset summary when switching between modes
if "previous_section" not in st.session_state:
    st.session_state["previous_section"] = section
elif st.session_state["previous_section"] != section:
    st.session_state["summary"] = None
    st.session_state["translated_summary"] = None
    st.session_state["last_translation_lang"] = None
    st.session_state["previous_section"] = section

st.sidebar.markdown("---")
st.markdown("👋 Welcome to the **Groq Summarizer**. Paste any article or YouTube URL and PDF or PDF File, and get a summary powered by **LLaMA3 (70B)**.")
st.sidebar.markdown("📌 [Get your Groq API key](https://console.groq.com/keys)")
st.sidebar.markdown("🔗 Use readable articles or captioned videos.")
st.sidebar.markdown("🧠 Powered by LLaMA3 & Groq")


# Main Heading
st.markdown("<h1 style='text-align: center;'>🧠 Groq Smart Summarizer</h1>", unsafe_allow_html=True)

# Prompt Template
prompt_template = """
You are an expert AI assistant designed to generate professional, concise summaries of long-form content.
Your task is to carefully read the following content and provide a detailed yet concise summary in no more than 300 words. The summary should preserve the original meaning, include the key points and important insights, and be written in fluent, natural English. Do not copy verbatim sentences from the input.

If the content is a YouTube transcript, structure your summary to reflect the main topics discussed throughout the video. If the content is a written article or document, identify and summarize the thesis, main arguments, and conclusions.

Content: {text}

Output Format:
- Write in paragraph form
- Avoid repetition or filler phrases
- Maintain logical flow and clarity
- Use neutral and objective tone
"""
prompt = PromptTemplate(template=prompt_template, input_variables=["text"])

# YouTube transcript extractor
def get_youtube_transcript_text(url):
    match = re.search(r"(?:v=|youtu\.be/)([a-zA-Z0-9_-]{11})", url)
    if not match:
        raise ValueError("Invalid YouTube URL format.")
    video_id = match.group(1)
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    return " ".join([t["text"] for t in transcript])

# File text extractor
def extract_text_from_file(uploaded_file):
    if uploaded_file.type == "application/pdf":
        reader = PyPDF2.PdfReader(uploaded_file)
        text = "".join(page.extract_text() or "" for page in reader.pages)
        return text.strip()
    elif uploaded_file.type == "text/plain":
        return uploaded_file.read().decode("utf-8", errors="ignore").strip()
    else:
        raise ValueError("Unsupported file type.")

# Download summary button for text file
def download_summary_as_text(summary_text, lang=None):
    filename = f"summary.txt" if not lang else f"summary_{lang.lower()}.txt"
    st.download_button(
        label="📄 Download Text Summary",
        data=summary_text.encode('utf-8'),
        file_name=filename,
        mime="text/plain"
    )

def summary_translation(summary_text, groq_api_key):
    # 🌍 Translation Feature
    if "summary" in st.session_state:
        st.markdown("### 🌍 Translate Summary")
        languages = ["English", "Spanish", "French", "German", "Arabic", "Chinese", "Urdu"]
        target_lang = st.selectbox("Choose a language", languages)

        # Track language change to reset old translation
        if "last_translation_lang" not in st.session_state:
            st.session_state["last_translation_lang"] = target_lang

        if st.session_state["last_translation_lang"] != target_lang:
            st.session_state["translated_summary"] = None
            st.session_state["last_translation_lang"] = target_lang

        if target_lang != "English":
            if st.button("🌐 Translate Summary"):
                with st.spinner("🔄 Translating..."):
                    try:
                        llm = ChatGroq(model="llama3-70b-8192", groq_api_key=groq_api_key)
                        translation_prompt = f"Translate the following summary into {target_lang}:\n\n{st.session_state['summary']}"
                        translated_raw = llm.invoke(translation_prompt).content
                        translated_clean = unicodedata.normalize("NFKC", str(translated_raw))

                        st.session_state["translated_summary"] = translated_clean  # ✅ Store in session state

                        st.success(f"✅ Translated to {target_lang}")

                    except Exception as e:
                        st.error(f"❗ Translation failed: {str(e)}")

        # Always show translated summary if available
        if "translated_summary" in st.session_state and st.session_state["translated_summary"]:
            st.markdown("### ✍️ Translated Summary")
            st.markdown(st.session_state["translated_summary"], unsafe_allow_html=True)

            st.markdown("### 📥 Download Options")
            download_summary_as_text(st.session_state["translated_summary"], target_lang)

# Main Content LINK SUMMERIZER
if section == "🔗 Link Summary":
    st.markdown("### 🔗 Enter a YouTube or Web Article URL")
    generic_url = st.text_input("Paste the URL here")

    # Reset state when switching between sections
    if "previous_section" not in st.session_state:
        st.session_state["previous_section"] = section
    elif st.session_state["previous_section"] != section:
        st.session_state["summary"] = None
        st.session_state["translated_summary"] = None
        st.session_state["last_translation_lang"] = None
        st.session_state["previous_section"] = section

    if st.button("🚀 Summarize Link"):
        if not groq_api_key:
            st.sidebar.error("❗ Enter your Groq API Key first.")
        elif not validators.url(generic_url):
            st.error("❗ Invalid URL.")
        else:
            try:
                with st.spinner("⏳ Summarizing..."):
                    llm = ChatGroq(model="llama3-70b-8192", groq_api_key=groq_api_key)

                    if "youtube.com/watch" in generic_url or "youtu.be/" in generic_url:
                        transcript = get_youtube_transcript_text(generic_url)
                        docs = [Document(page_content=transcript)]
                    else:
                        loader = UnstructuredURLLoader(
                            urls=[generic_url],
                            ssl_verify=False,
                            headers={"User-Agent": "Mozilla/5.0  Chrome/116.0.0.0"}
                        )
                        docs = loader.load()

                    chain = load_summarize_chain(llm, chain_type="stuff", prompt=prompt)
                    summary = chain.run(docs)

                    st.session_state["summary"] = summary

            except Exception as e:
                st.error(f"⚠️ Error: {str(e)}")

    # Always show summary and download if it exists
    if "summary" in st.session_state and st.session_state["summary"]:
        st.success("✅ Summary Ready!")
        st.markdown("### ✍️ Summary")
        st.write(st.session_state["summary"])

        st.markdown("### 📥 Download Options")
        download_summary_as_text(st.session_state["summary"])
    
    if "summary" in st.session_state:
        summary_translation(st.session_state["summary"], groq_api_key)

# FILE BASE SUMMERIZER
elif section == "📄 PDF/Text Summary":
    st.markdown("### 📄 Upload a PDF or Text File")
    uploaded_file = st.file_uploader("Choose a file", type=["pdf", "txt"])

    # 🧹 Clear summary if a new file is uploaded
    if uploaded_file and (
        "last_file_name" not in st.session_state or st.session_state["last_file_name"] != uploaded_file.name
    ):
        st.session_state["summary"] = None
        st.session_state["translated_summary"] = None
        st.session_state["last_translation_lang"] = None
        st.session_state["last_file_name"] = uploaded_file.name

    if st.button("🚀 Summarize File"):
        if not groq_api_key:
            st.sidebar.error("❗ Enter your Groq API Key first.")
        elif not uploaded_file:
            st.error("❗ Upload a file to summarize.")
        else:
            try:
                with st.spinner("⏳ Reading and summarizing..."):
                    llm = ChatGroq(model="llama3-70b-8192", groq_api_key=groq_api_key)
                    text = extract_text_from_file(uploaded_file)
                    docs = [Document(page_content=text)]
                    chain = load_summarize_chain(llm, chain_type="stuff", prompt=prompt)
                    summary = chain.run(docs)

                    st.session_state["summary"] = summary

            except Exception as e:
                st.error(f"⚠️ Error: {str(e)}")

    # Always show summary and download if it exists
    if "summary" in st.session_state and st.session_state["summary"]:
        st.success("✅ Summary Ready!")
        st.markdown("### ✍️ Summary")
        st.write(st.session_state["summary"])

        st.markdown("### 📥 Download Options")
        download_summary_as_text(st.session_state["summary"])

    if "summary" in st.session_state:
        summary_translation(st.session_state["summary"], groq_api_key)

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; font-size: 14px;'>Made with ❤️ using LLaMA3 and Groq API | © 2025</p>", unsafe_allow_html=True)
