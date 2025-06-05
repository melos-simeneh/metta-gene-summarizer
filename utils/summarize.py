
import os
from dotenv import load_dotenv
from hyperon.ext import register_atoms
from hyperon.atoms import OperationAtom,S,E
from google import genai

load_dotenv()

GENAI_API_KEY = os.getenv("GENAI_API_KEY")
client=genai.Client(api_key= GENAI_API_KEY) if GENAI_API_KEY else None

def gemini_summarize(text):
    if not client:
        return "❌ Gemini client not initialized. Make sure the GENAI_API_KEY environment variable is set"
    try:
        response = client.models.generate_content(
            model='gemini-2.0-flash-001',
            contents=f"Summarize the following gene data and make the summarry short and efficent:\n{text}"
        )
        return response.text.strip()
    except Exception as e:
        return f"❌ Gemini API error: {str(e)}"

def summarize(data):
    try:
        parts = data.get_children()

        def flatten_to_str(elem):
            if isinstance(elem, (list, tuple)):
                return " ".join(flatten_to_str(e) for e in elem)
            else:
                return str(elem)

        parts_wrapped = [S(flatten_to_str(p)) for p in parts]
        summary = gemini_summarize(" ".join(str(p) for p in parts))
        
        # Unpack parts_wrapped so each is passed as a separate argument
        return [E(E(*parts_wrapped), E(S(summary)))]

    except Exception as e:
        return [E(S("error"), S(f"❌ Summarization failed: {e}"))]


@register_atoms(pass_metta=True)
def utils(metta):
    summarizeGeneData= OperationAtom(
        "summarize",
        lambda data: summarize(data),
        ["Expression", "Atom"],
        unwrap=False
        )
    return {
        "summarize_gene_data": summarizeGeneData
    }