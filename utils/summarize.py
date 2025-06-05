
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
            contents = f"Summarize the following gene data in a single, concise paragraph:\n{text}"
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

def write_summary_to_file(gene_summary, file_name="gene_with_summary.metta"):
    try:
        gene_summary_parts = gene_summary.get_children()
        gene_exp, summary_exp = gene_summary_parts
        text_summary = summary_exp.get_children()[0]
        gene_tuple = gene_exp.get_children()

        file_name = str(file_name)
        file_path = os.path.join("data", file_name)
        formatted_gene = format_gene_with_summary(gene_tuple, text_summary)

        with open(file_path, "a", encoding="utf-8") as f:
            f.write(formatted_gene)

        return [S(f"\n✅ Gene knowledge with summary  appended to: {file_path}")]

    except Exception as e:
        return [S(f"\n❌ Failed to write output to file: {e}")]


def format_gene_with_summary(gene_tuple, summary_text):
    g, gene_type, chr_, start, end, name, syns = gene_tuple
    
    lines = [
        f"(gene {g})",
        f"(gene_type (gene {g}) {gene_type})",
        f"(chr (gene {g}) {chr_})",
        f"(start (gene {g}) {start})",
        f"(end (gene {g}) {end})",
        f"(gene_name (gene {g}) {name})",
        f"(synonyms (gene {g}) {syns})",
        f"(summary (gene {g}) ({summary_text}))\n"
    ]
    
    return "\n".join(lines)



@register_atoms(pass_metta=True)
def utils(metta):
    summarizeGeneData= OperationAtom(
        "summarize",
        lambda data: summarize(data),
        ["Expression", "Atom"],
        unwrap=False
        )
    writeSummery= OperationAtom(
        "write_summary",
        lambda summary,file_name: write_summary_to_file(summary,file_name),
        ["Expression","Expression","Atom"],
        unwrap=False
        )

    return {
        "write_summary": writeSummery,
        "summarize_gene_data": summarizeGeneData
    }