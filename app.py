from openai import OpenAI
import streamlit as st
import os
from dotenv import load_dotenv
from pypdf import PdfReader


load_dotenv()
api_key = os.getenv("openaikey")
client = OpenAI(api_key=api_key)


st.set_page_config(
    page_title="PDF AI Chatbot",
    page_icon="🤖",
    layout="centered"
)

st.header("📄PDF Destekli AI Sohbet Botu")
st.divider()


SYSTEM_PROMPTS = {
    "Genel": (
        "Sen Türkçe konuşan, yardımsever ve açıklayıcı bir yapay zeka asistansın."
    ),
    "Python Eğitmeni": (
        "Sen Python konusunda uzman bir eğitmensin. "
        "Kodları sade ve örneklerle anlatırsın."
    ),
    ".NET Uzmanı": (
        "Sen ASP.NET Core, C# ve backend mimarileri konusunda uzman bir yazılımcısın. "
        "Clean Code ve best practice kullanırsın."
    ),
    "Almanca Öğretmeni": (
        "Sen TELC B2 seviyesinde Almanca öğreten bir asistansın. "
        "Basit ve anlaşılır anlatırsın."
    )
}


st.sidebar.title("⚙️ Ayarlar")

assistant_role = st.sidebar.selectbox(
    "Asistan Rolü",
    list(SYSTEM_PROMPTS.keys())
)

uploaded_pdf = st.sidebar.file_uploader(
    "📄 PDF Yükle",
    type="pdf"
)


if "current_role" not in st.session_state:
    st.session_state.current_role = assistant_role

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": SYSTEM_PROMPTS[assistant_role]}
    ]

if "pdf_text" not in st.session_state:
    st.session_state.pdf_text = ""


if st.session_state.current_role != assistant_role:
    st.session_state.messages = [
        {"role": "system", "content": SYSTEM_PROMPTS[assistant_role]}
    ]
    st.session_state.current_role = assistant_role
    st.session_state.pdf_text = ""


if st.sidebar.button("🧹 Sohbeti Temizle"):
    st.session_state.messages = [
        {"role": "system", "content": SYSTEM_PROMPTS[assistant_role]}
    ]
    st.session_state.pdf_text = ""
    st.rerun()


def extract_pdf_text(pdf_file) -> str:
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + "\n"
    return text[:12000]  # token kontrolü

if uploaded_pdf:
    st.session_state.pdf_text = extract_pdf_text(uploaded_pdf)
    st.sidebar.success("✅ PDF başarıyla yüklendi")


MAX_MESSAGES = 12

def trim_messages():
    if len(st.session_state.messages) > MAX_MESSAGES:
        st.session_state.messages = (
            [st.session_state.messages[0]] +
            st.session_state.messages[-MAX_MESSAGES:]
        )


def generate_response(prompt: str) -> str:
    try:
        if st.session_state.pdf_text:
            user_prompt = f"""
Aşağıdaki PDF içeriğine göre soruyu cevapla.
Eğer cevap PDF içinde yoksa bunu açıkça belirt.

PDF İÇERİĞİ:
{st.session_state.pdf_text}

SORU:
{prompt}
"""
        else:
            user_prompt = prompt

        st.session_state.messages.append(
            {"role": "user", "content": user_prompt}
        )

        trim_messages()

        response = client.responses.create(
            model="gpt-4.1-mini",
            input=st.session_state.messages
        )

        return response.output_text

    except Exception as e:
        return f"❌ Bir hata oluştu: {str(e)}"


for message in st.session_state.messages[1:]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


if prompt := st.chat_input("PDF hakkında bir soru sor veya mesaj yaz..."):
    st.chat_message("user").markdown(prompt)

    with st.spinner("Asistan düşünüyor... 🤖"):
        response = generate_response(prompt)

    with st.chat_message("assistant"):
        st.markdown(response)

    st.session_state.messages.append(
        {"role": "assistant", "content": response}
    )
