import os
from hyperon.ext import register_atoms
from hyperon.atoms import OperationAtom,S,ExpressionAtom,E


def extract_synonyms(expression):
    """Extracts synonym strings from a synonym expression atom."""
    return [str(child) for child in expression.get_children()]

def extract_synonyms_for_list(syns):
    cleaned = str(syns).strip('()')
    return cleaned.split()

def extract_summary(atom):
    if isinstance(atom, ExpressionAtom):
        return " ".join(str(child) for child in atom.get_children())
    return str(atom)

def format_gene_info(gene_expr):
    """Formats gene data into a readable string."""
    output_lines = []
    parts = gene_expr.get_children()

    if len(parts) != 8:
        return  f"\n⚠️  Skipping : Expected 8 fields, got {len(parts)}.\n" \
                       f"    Raw expression: {gene_expr}\n" + "-" * 70

    gene_id, gene_type, chromosome, start, end, gene_name, synonyms_expr,summary_expr = parts
    synonyms = extract_synonyms_for_list(synonyms_expr)
    summary=extract_summary(summary_expr)

    block = [
        "\n" + "=" * 70,
        f"🧬  Gene Symbol : {gene_name}",
        f"🆔  Gene ID     : {gene_id}",
        "=" * 70,
        f"📌  Type        : {gene_type}",
        f"🧬  Chromosome  : {chromosome}",
        f"📏  Location    : {start} - {end}",
        f"🧾  Summary     : {summary}",
        "🔁  Synonyms    :"
    ]

    if synonyms:
        block.extend([f"\t\t\t     • {syn}" for syn in synonyms])
    else:
        block.append("\t\t\t     (none)")

    block.append("-" * 70)
    output_lines.append("\n".join(block))

    return "\n".join(output_lines)

def generate_header(title="GENE DATA SUMMARY"):
    return "\n" + "#" * 80 + "\n" + \
        "#{:^78}#\n".format(title) + \
        "#" * 80 + "\n"


def save_gene_info_to_file(formatted_text, output_file="gene_summary_result.txt"):
    """Appends gene info and summary to a text file, writing header if the file is empty or does not exist."""
    try:

        output_file=str(output_file)

        output_dir = "output"
        os.makedirs(output_dir, exist_ok=True)  # create folder if missing
        
        output_path = os.path.join(output_dir, output_file)

        # Check if file exists and is empty
        write_header = not os.path.exists(output_path) or os.path.getsize(output_path) == 0

        with open(output_path, "a", encoding="utf-8") as f:
            if write_header:
                header = generate_header()
                f.write(header)
            f.write(formatted_text)

        print(f"\n✅ Output saved to: {output_file}")
    except Exception as e:
        print(f"\n❌ Failed to write output to file: {e}")

def display_gene_info(formatted_text):
    """Displays gene info to the console."""
    header = generate_header()
    print(header + formatted_text)


def write_to_file(gene_data,output_file="gene_summary_result.txt"):
    formatted = format_gene_info(gene_data)
    display_gene_info(formatted)
    save_gene_info_to_file(formatted, output_file)

    return [S("Gene summary result saved")]


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



def format_gene_summary_atoms(gene_summary):

    gene_summary_parts = gene_summary.get_children()
    gene_exp, summary_exp = gene_summary_parts
    text_summary = extract_summary(summary_exp)
    gene_tuple = gene_exp.get_children()

    g, gene_type, chr_, start, end, name, syns = gene_tuple
    gene = E(S("gene"), S(str(g)))
    return [
        gene,
        E(S("gene_type"), gene, S(str(gene_type))),
        E(S("gene_type"), gene, S(str(gene_type))),
        E(S("chr"), gene, S(str(chr_))),
        E(S("start"), gene, S(str(start))),
        E(S("end"), gene, S(str(end))),
        E(S("gene_name"), gene, S(str(name))),
        E(S("synonyms"), gene, syns),
        E(S("summary"), gene, S(str(text_summary)))
    ]



@register_atoms(pass_metta=True)
def io_utils(metta):
    """
    Register I/O operations.

    save_human_readable_output(data, name) -> Atom
        Save gene data to file.
        data: Expression; filename: Expression.

    write_summary(summary, file_name) -> Atom
        Append gene summary to file.
        summary: Expression; file_name: Expression.
    """
    writeToFile= OperationAtom(
        "save_human_readable_output",
        lambda data, file_name: write_to_file(data, file_name),
        ["Expression","Expression", "Atom"],
        unwrap=False
        )
    
    writeSummery= OperationAtom(
        "write_summary",
        lambda summary,file_name: write_summary_to_file(summary,file_name),
        ["Expression","Expression","Atom"],
        unwrap=False
        )
    formatGeneSummery= OperationAtom(
        "write_summary",
        lambda summary: format_gene_summary_atoms(summary),
        ["Expression","Atom"],
        unwrap=False
        )
    return {
        
        "write_summary": writeSummery,
        "save_human_readable_output": writeToFile,
        "format_new_gene_data": formatGeneSummery,
    }
