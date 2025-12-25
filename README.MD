# 📄 PDF AI Chatbot

An interactive AI chatbot that allows users to upload PDF documents and ask questions based on their content.  
Built with **Streamlit** and **OpenAI**, featuring **role-based system prompting** and secure API key management.

---

## ✨ Features

- 📄 Upload PDF files and extract text
- 🤖 Ask questions based on PDF content
- 🎭 Role-based assistant modes:
  - General Assistant
  - Python Instructor
  - .NET Expert
  - German Tutor (TELC B2 level)
- 🧠 Chat history management with `session_state`
- 🧹 Clear chat functionality
- 🔒 Secure API key handling via `.env`
- ✂️ Automatic message trimming to control context size
- 🧩 PDF text length control (~12,000 characters)

---

## 🧰 Tech Stack

- Python
- Streamlit
- OpenAI (Responses API)
- python-dotenv
- PyPDF

---

## 📝 Notes

- If the PDF content is too long, only the first ~12,000 characters are used to avoid token overflow.
- If an answer is not found in the PDF, the assistant will explicitly state this.
- Chat history is automatically trimmed after a certain number of messages.

---

## 🛣️ Roadmap (Planned Improvements)

- True RAG architecture with embeddings and vector databases (FAISS / Chroma)
- Page-level chunking and smarter context selection
- Source citations (page numbers)
- Improved handling of tables and structured content

---

## 🔐 Security

- Never hardcode API keys.
- Always use environment variables for sensitive credentials.

---


