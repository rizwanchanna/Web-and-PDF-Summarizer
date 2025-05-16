# 🧠 Groq Smart Summarizer

**Groq Smart Summarizer** is a powerful and intuitive web app built with [Streamlit](https://streamlit.io/) that lets you summarize YouTube videos, web articles, PDF documents, and plain text files using the blazing-fast **LLaMA3 (70B)** model served through the **Groq API**.

Whether you're a student, researcher, or content creator, this tool saves you time by delivering clear, concise summaries — with the option to translate them into multiple languages.

---

## ✨ Key Features

- 🔗 **Link Summarization**: Paste any YouTube or article URL and get a high-quality summary.
- 📄 **File Summarization**: Upload PDF or TXT files and generate summaries instantly.
- 🌍 **Multilingual Translation**: Translate summaries into major world languages like Spanish, French, Arabic, and Chinese.
- 📥 **Export Summaries**: Download any summary as a `.txt` file in your preferred language.
- ⚡ **Powered by Groq + LLaMA3**: Enjoy ultra-fast inference with the LLaMA3 70B model via Groq's high-performance backend.

---

## 🚀 Getting Started

### 1. Clone the Repository

git clone https://github.com/rizwanchanna/Web-and-PDF-Summarizer/tree/main

cd Web-and-PDF-Summarizer 

### 2. Install Dependencies

pip install -r requirements.txt

### 3. Launch the App

streamlit run app.py

### 4. Get Your Groq API Key

- Sign in at Groq Console

- Copy your API key and paste it into the app sidebar when prompted.

---

## 🧠 How It Works

The summarizer uses LangChain to create a summarization chain powered by LLaMA3, accessed through the Groq API. It processes content from URLs, transcripts, or files, and summarizes it within ~300 words. Optional translation is done by prompting LLaMA3 with your selected target language.

---

## 🌍 Supported Translation Languages

English (default)

Spanish

French

German

Arabic

Chinese

Urdu

---


## 🛠 Tech Stack

- Frontend: Streamlit

- LLM Backend: LLaMA3-70B via Groq API

- Document Handling: LangChain, UnstructuredURLLoader, PyPDF2

- YouTube Transcripts: youtube-transcript-api


---

## 📌 Tips & Notes

- Ensure YouTube videos have captions for transcript-based summarization.

- Web articles should be readable and not behind paywalls.

- File upload supports .pdf and .txt formats only.

- Translation quality depends on the language and content complexity.
