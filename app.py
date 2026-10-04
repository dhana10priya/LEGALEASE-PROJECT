"""Streamlit frontend for LegalEase. Run from project root:
    streamlit run frontend/app.py
"""
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import requests
import streamlit as st

from ai_core.generator import (
    format_docx, format_html_preview, format_pdf, sanitize_text,
)
from config import BACKEND_URL, WEB_LOGO_PATH

st.set_page_config(page_title="LegalEase", layout="centered")

_, c2, _ = st.columns([1, 2, 1])
with c2:
    if WEB_LOGO_PATH.exists():
        st.image(str(WEB_LOGO_PATH), use_container_width=True)
st.markdown("<h2 style='text-align:center;'>AI Legal Document Generator</h2>",
            unsafe_allow_html=True)

document_type = st.text_input("Document Type (Ex: Agreement, Contract, NDA)")
parties = st.text_area("Parties Involved")
terms = st.text_area("Terms & Conditions (Use semicolons for bullet points)")
dates = st.text_input("Effective Date")

if st.button("Generate Document"):
    if not document_type.strip() or not parties.strip():
        st.warning("Please enter at least a document type and the parties.")
    else:
        with st.spinner("Drafting your document..."):
            try:
                r = requests.post(
                    f"{BACKEND_URL}/generate",
                    json={"document_type": document_type, "parties": parties,
                          "terms": terms, "dates": dates},
                    timeout=120,
                )
                r.raise_for_status()
                st.session_state.generated_text = sanitize_text(r.json()["document"])
                st.session_state.doc_type = document_type
                st.session_state.terms = terms
                st.session_state.show_edit = False
                st.success("Document Generated Successfully!")
            except requests.HTTPError:
                st.error(f"Backend error: {r.json().get('detail', r.text)}")
            except requests.RequestException as e:
                st.error(f"Could not reach backend at {BACKEND_URL}: {e}")
else:
    if "generated_text" not in st.session_state:
        st.info("Click 'Generate Document' to start")

if "generated_text" in st.session_state:
    doc_type = st.session_state.doc_type
    slug = doc_type.strip().replace(" ", "_").lower() or "document"

    if st.button("\u270f\ufe0f Click to Edit Document"):
        st.session_state.show_edit = not st.session_state.get("show_edit", False)

    if st.session_state.get("show_edit"):
        st.session_state.generated_text = st.text_area(
            "Edit Document Below:", st.session_state.generated_text, height=300
        )

    text = st.session_state.generated_text
    st.markdown(
        "<div style='background:#0f172a;color:#e5e7eb;padding:18px;border-radius:10px;"
        "max-height:380px;overflow-y:auto;font-family:Georgia,serif'>"
        f"{format_html_preview(text)}</div>",
        unsafe_allow_html=True,
    )

    terms_in = st.session_state.get("terms", "")
    st.download_button("\U0001f4c4 Download as .TXT", data=text,
                       file_name=f"{slug}.txt", mime="text/plain")
    st.download_button(
        "\U0001f4dd Download as .DOCX", data=format_docx(text, doc_type, terms_in),
        file_name=f"{slug}.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
    try:
        st.download_button("\U0001f4d5 Download as .PDF",
                           data=format_pdf(text, doc_type, terms_in),
                           file_name=f"{slug}.pdf", mime="application/pdf")
    except ImportError:
        st.error("PDF export needs `pip install fpdf2`.")
