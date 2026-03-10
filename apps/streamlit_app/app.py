import io
import os
import uuid
from typing import Any, Dict, List

import requests
import streamlit as st

try:
    from pypdf import PdfReader
except Exception:
    PdfReader = None

try:
    from docx import Document as DocxDocument
except Exception:
    DocxDocument = None


def get_api_base_url() -> str:
    try:
        if "API_BASE_URL" in st.secrets:
            return st.secrets["API_BASE_URL"]
    except Exception:
        pass
    return os.getenv("API_BASE_URL", "http://localhost:8001")


API_BASE_URL = get_api_base_url().rstrip("/")

if "conversation_id" not in st.session_state:
    st.session_state["conversation_id"] = str(uuid.uuid4())


def extract_text_from_txt(file_bytes: bytes) -> str:
    return file_bytes.decode("utf-8", errors="ignore").strip()


def extract_text_from_pdf(file_bytes: bytes) -> str:
    if PdfReader is None:
        raise RuntimeError("pypdf is not installed. Run: pip install pypdf")
    reader = PdfReader(io.BytesIO(file_bytes))
    pages: List[str] = []
    for page in reader.pages:
        pages.append(page.extract_text() or "")
    return "\n".join(pages).strip()


def extract_text_from_docx(file_bytes: bytes) -> str:
    if DocxDocument is None:
        raise RuntimeError("python-docx is not installed. Run: pip install python-docx")
    doc = DocxDocument(io.BytesIO(file_bytes))
    return "\n".join(p.text for p in doc.paragraphs).strip()


def extract_uploaded_text(uploaded_file) -> str:
    if uploaded_file is None:
        return ""

    filename = uploaded_file.name.lower()
    file_bytes = uploaded_file.read()

    if filename.endswith(".txt") or filename.endswith(".md"):
        return extract_text_from_txt(file_bytes)

    if filename.endswith(".pdf"):
        return extract_text_from_pdf(file_bytes)

    if filename.endswith(".docx"):
        return extract_text_from_docx(file_bytes)

    raise RuntimeError("Unsupported file type. Use .txt, .md, .pdf, or .docx")


def store_document(title: str, content: str) -> Dict[str, Any]:
    payload = {
        "title": title,
        "content": content,
        "chunk_size": 1200,
        "chunk_overlap": 200,
        "metadata": {},
    }
    response = requests.post(
        f"{API_BASE_URL}/v1/documents/upload",
        json=payload,
        timeout=120,
    )

    if not response.ok:
        raise RuntimeError(f"Document upload failed: {response.status_code} | {response.text}")

    return response.json()


def run_query(question: str, llm_provider: str, conversation_id: str) -> Dict[str, Any]:
    payload = {
        "query": question,
        "provider": llm_provider,
        "mode": "text",
        "conversation_id": conversation_id,
    }
    response = requests.post(
        f"{API_BASE_URL}/v1/chat/query",
        json=payload,
        timeout=120,
    )

    if not response.ok:
        raise RuntimeError(f"Chat query failed: {response.status_code} | {response.text}")

    return response.json()


def transcribe_audio_file(audio_bytes: bytes) -> Dict[str, Any]:
    files = {"file": ("question.wav", audio_bytes, "audio/wav")}
    response = requests.post(
        f"{API_BASE_URL}/v1/speech/transcribe",
        files=files,
        timeout=180,
    )

    if not response.ok:
        raise RuntimeError(f"Transcription failed: {response.status_code} | {response.text}")

    return response.json()


def speak_text(text: str) -> bytes:
    response = requests.post(
        f"{API_BASE_URL}/v1/speech/speak",
        json={"text": text},
        timeout=180,
    )

    if not response.ok:
        raise RuntimeError(f"Speech synthesis failed: {response.status_code} | {response.text}")

    return response.content


st.set_page_config(page_title="Agentic Foundry", layout="wide")
st.title("Agentic Foundry")
st.caption("Grounded voice-enabled agentic AI boilerplate demo")

with st.sidebar:
    st.subheader("Demo Controls")

    provider_options = ["mock", "openai", "anthropic", "gemini"]

    default_provider = os.getenv("DEFAULT_LLM_PROVIDER", "openai").lower()
    if default_provider not in provider_options:
        default_provider = "openai"

    provider = st.selectbox(
        "LLM Provider",
        provider_options,
        index=provider_options.index(default_provider),
    )

    read_aloud = st.checkbox("Read answer aloud", value=True)

    st.write("This UI is intentionally thin. The architecture lives in the backend.")
    st.caption(f"API: {API_BASE_URL}")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Upload knowledge")

    document_title = st.text_input("Document title", value="Getting Started")

    input_mode = st.radio(
        "Knowledge input mode",
        ["Manual entry", "File upload"],
        horizontal=True,
    )

    final_document_text = ""

    if input_mode == "Manual entry":
        manual_content = st.text_area(
            "Document content",
            value="Agentic Foundry is a grounded AI boilerplate with Streamlit, FastAPI, MongoDB, Redis, MCP, and orchestration.",
            height=220,
        )
        final_document_text = manual_content.strip()
    else:
        uploaded_file = st.file_uploader(
            "Upload a document",
            type=["txt", "md", "pdf", "docx"],
            help="Supported formats: .txt, .md, .pdf, .docx",
        )

        if uploaded_file is not None:
            try:
                extracted_text = extract_uploaded_text(uploaded_file)
                final_document_text = extracted_text.strip()

                st.success(f"Loaded file: {uploaded_file.name}")
                st.text_area(
                    "Extracted document content",
                    value=final_document_text,
                    height=220,
                )
            except Exception as ex:
                st.error(f"Could not read uploaded file: {ex}")

    if st.button("Store document", use_container_width=True):
        if not document_title.strip():
            st.error("Please enter a document title.")
        elif not final_document_text.strip():
            st.error("Please provide document content manually or upload a valid document.")
        else:
            try:
                result = store_document(document_title.strip(), final_document_text.strip())
                st.success(
                    f"Document stored successfully. ID: {result.get('document_id', 'n/a')} | "
                    f"Chunks: {result.get('chunk_count', 'n/a')}"
                )
            except Exception as ex:
                st.error(f"Failed to store document: {ex}")

    st.subheader("Voice input")
    st.write("Record your question")
    audio_value = st.audio_input("Record audio")

    if audio_value is not None:
        st.audio(audio_value)

        if st.button("Transcribe recorded audio", use_container_width=True):
            try:
                transcript_result = transcribe_audio_file(audio_value.read())
                transcript = transcript_result.get("transcript", "").strip()

                if transcript:
                    st.session_state["transcribed_question"] = transcript
                    st.success("Audio transcribed successfully.")
                else:
                    st.warning("Transcription endpoint returned no transcript.")
            except Exception as ex:
                st.error(f"Transcription failed: {ex}")

with col2:
    st.subheader("Ask the copilot")

    default_question = st.session_state.get(
        "transcribed_question",
        "What is this document about?",
    )

    question = st.text_area("Question", value=default_question, height=160)

    if st.button("Run query", use_container_width=True):
        if not question.strip():
            st.error("Please enter a question.")
        else:
            try:
                query_result = run_query(
                    question.strip(),
                    provider,
                    st.session_state["conversation_id"],
                )

                answer = query_result.get("answer", "")
                citations = query_result.get("citations", [])
                trace_id = query_result.get("trace_id", "")

                st.session_state["last_answer"] = answer
                st.session_state["last_citations"] = citations
                st.session_state["last_trace_id"] = trace_id

                if read_aloud and answer.strip():
                    try:
                        audio_bytes = speak_text(answer)
                        st.session_state["last_audio"] = audio_bytes
                    except Exception as speech_ex:
                        st.warning(f"Answer generated, but speech synthesis failed: {speech_ex}")
                        st.session_state["last_audio"] = None
                else:
                    st.session_state["last_audio"] = None

            except Exception as ex:
                st.error(f"Query failed: {ex}")

    st.subheader("Answer")

    answer = st.session_state.get("last_answer", "")
    citations = st.session_state.get("last_citations", [])
    trace_id = st.session_state.get("last_trace_id", "")

    if answer:
        st.write(answer)

        if citations:
            st.markdown("**Citations**")
            for idx, citation in enumerate(citations, start=1):
                st.write(f"{idx}. {citation}")

        if trace_id:
            st.caption(f"Trace ID: {trace_id}")

    spoken_audio = st.session_state.get("last_audio")
    if spoken_audio:
        st.subheader("Spoken answer")
        st.audio(spoken_audio, format="audio/wav")