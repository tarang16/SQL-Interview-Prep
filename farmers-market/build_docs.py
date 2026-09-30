"""Builds PDF (headless Chrome) and DOCX versions of the 200-question bank."""
import re, subprocess
from pathlib import Path
import markdown
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt, RGBColor, Cm

ROOT = Path(__file__).resolve().parent
BUILD = ROOT / "build"; BUILD.mkdir(exist_ok=True)
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
MD = ROOT / "Farmers_Market_200_SQL_Questions_with_Answers.md"

# ── 2. HTML → PDF via Chrome ─────────────────────────────────────────────────
CSS = """
@page { size: A4; margin: 18mm 16mm 18mm 16mm; }
body { font-family: 'Segoe UI', Calibri, Arial, sans-serif; font-size: 10.5pt; line-height: 1.5; color: #1d2330; }
h1 { font-size: 21pt; color: #14532d; border-bottom: 3px solid #16a34a; padding-bottom: 6px; margin-top: 0; }
h2 { font-size: 14pt; color: #fff; background: #166534; padding: 6px 10px; border-radius: 4px; margin-top: 22px; page-break-after: avoid; }
p { margin: 6px 0; }
p:has(> strong:first-child) { margin-top: 12px; }
code { font-family: Consolas, 'Courier New', monospace; font-size: 9.2pt; background: #f1f5f2; padding: 1px 4px; border-radius: 3px; color: #7c2d12; }
pre { background: #f6f8fa; border: 1px solid #d8dee4; border-left: 4px solid #16a34a; padding: 8px 10px; border-radius: 4px; page-break-inside: avoid; white-space: pre-wrap; }
pre code { background: none; color: #1d2330; padding: 0; font-size: 9pt; }
table { border-collapse: collapse; margin: 8px 0; font-size: 9.5pt; page-break-inside: avoid; }
th, td { border: 1px solid #cbd5d0; padding: 4px 8px; text-align: left; vertical-align: top; }
th { background: #dcfce7; }
h1 + p, h1 { page-break-after: avoid; }
h1:not(:first-of-type) { page-break-before: always; }
blockquote { border-left: 4px solid #f59e0b; background: #fffbeb; margin: 8px 0; padding: 4px 10px; }
hr { border: none; border-top: 1px solid #d1d5db; margin: 14px 0; }
.answer-label { color: #166534; page-break-after: avoid; break-after: avoid; }
"""

def fix_lists(md_text):
    out, in_code = [], False
    for ln in md_text.splitlines():
        if ln.startswith("```"): in_code = not in_code
        is_item = re.match(r"^(\s*[-*] |\d+\. )", ln)
        if not in_code and is_item and out and out[-1].strip() and not re.match(r"^(\s*[-*] |\d+\. )", out[-1]):
            out.append("")
        out.append(ln)
    return "\n".join(out)

def md_to_html(md_text, title):
    html = markdown.markdown(fix_lists(md_text), extensions=["tables", "fenced_code"])
    html = html.replace("<p><strong>Answer</strong></p>",
                        '<p class="answer-label"><strong>Answer</strong></p>')
    return f"<!DOCTYPE html><html><head><meta charset='utf-8'><title>{title}</title><style>{CSS}</style></head><body>{html}</body></html>"

def to_pdf(md_path, title):
    html_path = BUILD / (md_path.stem + ".html")
    pdf_path = ROOT / (md_path.stem + ".pdf")
    html_path.write_text(md_to_html(md_path.read_text(encoding="utf-8"), title), encoding="utf-8")
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                    f"--print-to-pdf={pdf_path}", html_path.as_uri()],
                   check=True, capture_output=True, timeout=180)
    print("pdf:", pdf_path.name, pdf_path.stat().st_size)

# ── 3. Markdown → DOCX ───────────────────────────────────────────────────────
GREEN = RGBColor(0x16, 0x65, 0x34)
INLINE = re.compile(r"(\*\*[^*]+\*\*|`[^`]+`|\*[^*]+\*)")

def add_inline(par, text, bold=False):
    for part in INLINE.split(text):
        if not part:
            continue
        if part.startswith("**") and part.endswith("**"):
            add_inline(par, part[2:-2], bold=True)
        elif part.startswith("`") and part.endswith("`"):
            r = par.add_run(part[1:-1]); r.font.name = "Consolas"; r.font.size = Pt(9.5)
            r.font.color.rgb = RGBColor(0x7c, 0x2d, 0x12); r.bold = bold
        elif part.startswith("*") and part.endswith("*") and len(part) > 2:
            r = par.add_run(part[1:-1]); r.italic = True; r.bold = bold
        else:
            r = par.add_run(part); r.bold = bold

def shade(cell_or_par_pr, hex_fill):
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear"); shd.set(qn("w:color"), "auto"); shd.set(qn("w:fill"), hex_fill)
    cell_or_par_pr.append(shd)

def to_docx(md_path):
    doc = Document()
    sec = doc.sections[0]
    sec.left_margin = sec.right_margin = Cm(2); sec.top_margin = sec.bottom_margin = Cm(1.8)
    st = doc.styles["Normal"]; st.font.name = "Calibri"; st.font.size = Pt(10.5)
    lines = md_path.read_text(encoding="utf-8").splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("```"):
            code = []
            i += 1
            while i < len(lines) and not lines[i].startswith("```"):
                code.append(lines[i]); i += 1
            p = doc.add_paragraph()
            shade(p._p.get_or_add_pPr(), "F3F5F7")
            p.paragraph_format.left_indent = Cm(0.3)
            r = p.add_run("\n".join(code)); r.font.name = "Consolas"; r.font.size = Pt(9)
        elif line.startswith("# "):
            if doc.paragraphs: doc.add_page_break()
            h = doc.add_heading(level=0); add_inline(h, line[2:])
        elif line.startswith("> "):
            p = doc.add_paragraph(); shade(p._p.get_or_add_pPr(), "FFFBEB")
            add_inline(p, line[2:])
        elif line.startswith("## "):
            h = doc.add_heading(level=1); add_inline(h, line[3:])
            for r in h.runs: r.font.color.rgb = GREEN
        elif line.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                if not all(re.fullmatch(r":?-+:?", c) for c in cells):
                    rows.append(cells)
                i += 1
            t = doc.add_table(rows=len(rows), cols=len(rows[0])); t.style = "Table Grid"
            for ri, row in enumerate(rows):
                for ci, val in enumerate(row):
                    cell = t.cell(ri, ci); cell.text = ""
                    add_inline(cell.paragraphs[0], val, bold=(ri == 0))
                    if ri == 0: shade(cell._tc.get_or_add_tcPr(), "DCFCE7")
            doc.add_paragraph()
            continue
        elif re.match(r"^-{3,}\s*$", line):
            pass
        elif re.match(r"^\s*[-*] ", line):
            p = doc.add_paragraph(style="List Bullet"); add_inline(p, re.sub(r"^\s*[-*] ", "", line))
        elif re.match(r"^\d+\. ", line):
            p = doc.add_paragraph(style="List Number"); add_inline(p, re.sub(r"^\d+\. ", "", line))
        elif line.strip() == "**Answer**":
            p = doc.add_paragraph(); r = p.add_run("Answer"); r.bold = True; r.font.color.rgb = GREEN
        elif line.strip():
            p = doc.add_paragraph()
            if re.match(r"^\*\*[QA]\d+\.\*\*", line):
                p.paragraph_format.space_before = Pt(10)
            add_inline(p, line)
        i += 1
    out = ROOT / (md_path.stem + ".docx")
    doc.save(out)
    print("docx:", out.name, out.stat().st_size)


to_pdf(MD, "Farmers Market: 200 SQL Questions")
to_docx(MD)

# Questions-only PDF: everything before the ANSWERS heading
QMD = ROOT / "Farmers_Market_200_SQL_Questions_Only.md"
q = MD.read_text(encoding="utf-8").split("\n# ANSWERS", 1)[0].rstrip().rstrip("-").rstrip()
q = q.replace("- The answers are at the end of the file.\n",
              "- The answers are in the separate file *Farmers_Market_200_SQL_Questions_with_Answers*.\n")
QMD.write_text(q + "\n", encoding="utf-8")
to_pdf(QMD, "Farmers Market: 200 SQL Questions")
