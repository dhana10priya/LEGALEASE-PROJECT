"""Gemini integration: builds the prompt and calls the model."""
import google.generativeai as genai
from config import GEMINI_API_KEY, GEMINI_MODEL


class GeminiDocumentGenerator:
    def __init__(self, model_name: str = GEMINI_MODEL):
        if not GEMINI_API_KEY:
            raise RuntimeError("GEMINI_API_KEY is missing. Add it to your .env file.")
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel(model_name)

    def generate_document(self, document_type, parties, terms, dates) -> str:
        term_lines = "\n".join(
            f"- {t.strip()}" for t in terms.split(";") if t.strip()
        )
        prompt = (
            f"Generate a comprehensive legal document titled '{document_type}'.\n"
            f"Involved parties: {parties}\n"
            f"Effective Date: {dates}\n"
            f"Terms and conditions:\n{term_lines}\n\n"
            "Requirements:\n"
            "- Use formal legal structure with numbered sections (e.g. '1. Services:') "
            "and standard legal clauses (governing law, severability, entire agreement, "
            "termination, confidentiality where relevant).\n"
            "- Incorporate every listed term faithfully.\n"
            "- Use [square-bracket placeholders] for any missing details.\n"
            "- End with an IN WITNESS WHEREOF signature block.\n"
            "- Output plain text only: no markdown, no code fences, no commentary."
        )
        response = self.model.generate_content(prompt)
        return response.text
