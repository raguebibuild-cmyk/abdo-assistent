"""
code_review_pdf.py
Branded PDF generator for Code Review Agent reports.
Usage: python code_review_pdf.py <input.md> <output.pdf>
Tries reportlab first; falls back to fpdf2.
Severity sections are colour-coded: CRITICAL=red, WARNING=amber, INFO=indigo.
"""
import sys, os, re, subprocess
from pathlib import Path as _Path

_equipdir = str(_Path(__file__).parent)
if _equipdir not in sys.path:
    sys.path.insert(0, _equipdir)
from brand import page_callback as _brand_cb

if len(sys.argv) != 3:
    print("Usage: python code_review_pdf.py <input.md> <output.pdf>")
    sys.exit(1)

MD_PATH, PDF_PATH = sys.argv[1], sys.argv[2]

if not os.path.isfile(MD_PATH):
    print(f"ERROR: Input file not found: {MD_PATH}")
    sys.exit(1)

with open(MD_PATH, "r", encoding="utf-8") as f:
    content = f.read()

os.makedirs(os.path.dirname(os.path.abspath(PDF_PATH)), exist_ok=True)


def ensure_lib(lib_name, pip_name=None):
    pip_name = pip_name or lib_name
    try:
        __import__(lib_name)
        return True
    except ImportError:
        print(f"Installing {pip_name}...")
        r = subprocess.run(
            [sys.executable, "-m", "pip", "install", pip_name, "--quiet"],
            capture_output=True, text=True
        )
        return r.returncode == 0


def try_reportlab(content, pdf_path):
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.units import mm
    from reportlab.lib import colors
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Preformatted

    MARGIN  = 22 * mm
    NAVY    = colors.HexColor("#012240")
    INDIGO  = colors.HexColor("#4f4cee")
    AMBER   = colors.HexColor("#e89820")
    RED     = colors.HexColor("#c0392b")
    ORANGE  = colors.HexColor("#e67e22")
    BODY_C  = colors.HexColor("#1e293b")
    MUTED   = colors.HexColor("#64748b")
    BORDER  = colors.HexColor("#e2e8f0")
    CODEBG  = colors.HexColor("#f1f5f9")
    REDBG   = colors.HexColor("#fff5f5")
    ORANGBG = colors.HexColor("#fffbeb")
    INDIGBG = colors.HexColor("#f0f0ff")

    doc = SimpleDocTemplate(
        pdf_path, pagesize=A4,
        rightMargin=MARGIN, leftMargin=MARGIN,
        topMargin=MARGIN + 4 * mm, bottomMargin=MARGIN + 8 * mm,
        title="Code Review — degiabdo",
        author="Code Review Agent — degiabdo",
    )

    H1     = ParagraphStyle("H1",     fontName="Helvetica-Bold",    fontSize=18, leading=24,   textColor=NAVY,   spaceAfter=3*mm)
    H2     = ParagraphStyle("H2",     fontName="Helvetica-Bold",    fontSize=13, leading=17,   textColor=NAVY,   spaceBefore=5*mm, spaceAfter=2*mm)
    H2CRIT = ParagraphStyle("H2CRIT", fontName="Helvetica-Bold",    fontSize=13, leading=17,   textColor=RED,    spaceBefore=5*mm, spaceAfter=2*mm)
    H2WARN = ParagraphStyle("H2WARN", fontName="Helvetica-Bold",    fontSize=13, leading=17,   textColor=ORANGE, spaceBefore=5*mm, spaceAfter=2*mm)
    H2INFO = ParagraphStyle("H2INFO", fontName="Helvetica-Bold",    fontSize=13, leading=17,   textColor=INDIGO, spaceBefore=5*mm, spaceAfter=2*mm)
    H3     = ParagraphStyle("H3",     fontName="Helvetica-Bold",    fontSize=11, leading=15,   textColor=BODY_C, spaceBefore=4*mm, spaceAfter=1.5*mm)
    BODY   = ParagraphStyle("BODY",   fontName="Helvetica",         fontSize=9.5, leading=14.5, textColor=BODY_C, spaceAfter=2*mm)
    META   = ParagraphStyle("META",   fontName="Helvetica-Oblique", fontSize=8.5, leading=12,   textColor=MUTED,  spaceAfter=1*mm)
    LABEL  = ParagraphStyle("LABEL",  fontName="Helvetica-Bold",    fontSize=9,  leading=13,   textColor=INDIGO, spaceAfter=1*mm)
    BULLET = ParagraphStyle("BULLET", fontName="Helvetica",         fontSize=9.5, leading=14,  textColor=BODY_C, spaceAfter=1.5*mm, leftIndent=8*mm, firstLineIndent=-4*mm)
    CODE   = ParagraphStyle("CODE",   fontName="Courier",           fontSize=8,  leading=11,   textColor=BODY_C, spaceAfter=2*mm, leftIndent=4*mm,
                             backColor=CODEBG, borderPad=3)
    TH     = ParagraphStyle("TH",     fontName="Helvetica-Bold",    fontSize=8.5, leading=11,  textColor=NAVY)
    TR     = ParagraphStyle("TR",     fontName="Helvetica",         fontSize=8,   leading=11,  textColor=colors.HexColor("#333333"))
    FOOT   = ParagraphStyle("FOOT",   fontName="Helvetica-Oblique", fontSize=8,  leading=10,   textColor=MUTED,  spaceBefore=4*mm)
    SUMS   = ParagraphStyle("SUMS",   fontName="Helvetica-Bold",    fontSize=10, leading=14,   textColor=NAVY,   spaceAfter=1*mm)

    def clean(t):
        return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    def inline(t):
        t = re.sub(r'\*\*\*(.+?)\*\*\*', r'<b><i>\1</i></b>', t)
        t = re.sub(r'\*\*(.+?)\*\*',     r'<b>\1</b>', t)
        t = re.sub(r'\*(.+?)\*',         r'<i>\1</i>', t)
        t = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'<font color="#4f4cee">\1</font>', t)
        t = re.sub(r'`([^`]+)`', r'<font name="Courier" size="8.5" color="#c0392b">\1</font>', t)
        return t

    def para(text, style):
        try:
            return Paragraph(inline(clean(text)), style)
        except Exception:
            return Paragraph(clean(text), style)

    # Determine which H2 style to use based on section heading
    def h2_style(text):
        upper = text.upper()
        if "CRITICAL" in upper:
            return H2CRIT
        if "WARNING" in upper:
            return H2WARN
        if "INFO" in upper or "BEST PRACTICE" in upper:
            return H2INFO
        return H2

    story = []
    lines = content.split('\n')
    i = 0
    in_code_block = False
    code_lines = []
    table_rows = []

    while i < len(lines):
        line = lines[i].rstrip()

        # Code block handling
        if line.startswith('```'):
            if in_code_block:
                in_code_block = False
                block_text = '\n'.join(code_lines)
                for cl in code_lines:
                    story.append(Paragraph(clean(cl) if cl else ' ', CODE))
                story.append(Spacer(1, 1 * mm))
                code_lines = []
            else:
                in_code_block = True
                code_lines = []
            i += 1
            continue

        if in_code_block:
            code_lines.append(line)
            i += 1
            continue

        if line.startswith('# ') and not line.startswith('## '):
            story.append(para(line[2:], H1))
            story.append(HRFlowable(width="100%", thickness=1.5, color=AMBER, spaceAfter=3*mm))
        elif line.startswith('## '):
            heading = line[3:]
            story.append(HRFlowable(width="100%", thickness=0.5, color=BORDER, spaceBefore=3*mm, spaceAfter=1*mm))
            story.append(para(heading, h2_style(heading)))
        elif line.startswith('### '):
            story.append(para(line[4:], H3))
        elif re.match(r'^-{3,}$', line.strip()):
            story.append(HRFlowable(width="100%", thickness=0.4, color=BORDER, spaceBefore=2*mm, spaceAfter=2*mm))
        elif line.startswith('|'):
            cells = [c.strip() for c in line.split('|')[1:-1]]
            if not all(re.match(r'^[-: ]+$', c) for c in cells):
                table_rows.append(cells)
            if not (i + 1 < len(lines) and lines[i + 1].startswith('|')):
                for idx, row in enumerate(table_rows):
                    story.append(para("  |  ".join(row), TH if idx == 0 else TR))
                table_rows = []
        elif line.startswith('- ') or line.startswith('* '):
            story.append(para(u'• ' + line[2:], BULLET))
        elif re.match(r'^\d+\. ', line):
            story.append(para(line, BULLET))
        elif line.startswith('**') and ':**' in line:
            story.append(para(line, LABEL))
        elif re.match(r'^\*[^*].+[^*]\*$', line.strip()):
            story.append(para(line.strip('*'), FOOT))
        elif line.startswith('**Issues found:**'):
            story.append(para(line, SUMS))
        elif not line.strip():
            story.append(Spacer(1, 1.5 * mm))
        else:
            story.append(para(line, BODY))

        i += 1

    doc.build(story, onFirstPage=_brand_cb, onLaterPages=_brand_cb)
    print(f"SUCCESS (reportlab): {pdf_path}")
    return True


def try_fpdf2(content, pdf_path):
    from fpdf import FPDF

    class PDF(FPDF):
        def header(self):
            self.set_fill_color(255, 255, 255)
            self.rect(0, 0, self.w, 14, 'F')
            self.set_fill_color(232, 152, 32)
            self.rect(0, 14, self.w, 1.2, 'F')
            self.set_font("Helvetica", "B", 10)
            self.set_text_color(79, 76, 238)
            self.set_y(2)
            self.cell(0, 8, "DEGI", align="R")

        def footer(self):
            self.set_y(-12)
            self.set_font("Helvetica", "I", 7)
            self.set_text_color(100, 116, 139)
            self.cell(0, 5, f"degiabdo  |  Page {self.page_no()}", align="C")

    def plain(t):
        t = re.sub(r'\*\*\*(.+?)\*\*\*', r'\1', t)
        t = re.sub(r'\*\*(.+?)\*\*', r'\1', t)
        t = re.sub(r'\*(.+?)\*', r'\1', t)
        t = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', t)
        t = re.sub(r'`([^`]+)`', r'\1', t)
        return t

    pdf = PDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=18)
    pdf.set_margins(20, 22, 20)

    in_code = False
    for line in content.split('\n'):
        line = line.rstrip()
        if line.startswith('```'):
            in_code = not in_code
            continue
        if in_code:
            pdf.set_font("Courier", "", 7.5)
            pdf.set_text_color(30, 41, 59)
            pdf.multi_cell(0, 4.5, line or ' ')
            continue
        if not line:
            pdf.ln(2)
        elif line.startswith('# ') and not line.startswith('## '):
            pdf.set_font("Helvetica", "B", 16)
            pdf.set_text_color(1, 34, 64)
            pdf.multi_cell(0, 9, plain(line[2:]))
        elif line.startswith('## '):
            heading = plain(line[3:])
            upper = heading.upper()
            if "CRITICAL" in upper:
                pdf.set_text_color(192, 57, 43)
            elif "WARNING" in upper:
                pdf.set_text_color(230, 126, 34)
            elif "INFO" in upper or "BEST PRACTICE" in upper:
                pdf.set_text_color(79, 76, 238)
            else:
                pdf.set_text_color(1, 34, 64)
            pdf.set_font("Helvetica", "B", 12)
            pdf.multi_cell(0, 7, heading)
        elif line.startswith('### '):
            pdf.set_font("Helvetica", "B", 10)
            pdf.set_text_color(30, 41, 59)
            pdf.multi_cell(0, 6, plain(line[4:]))
        elif line.startswith('|'):
            cells = [c.strip() for c in line.split('|')[1:-1]]
            if not all(re.match(r'^[-: ]+$', c) for c in cells):
                pdf.set_font("Helvetica", "", 7.5)
                pdf.set_text_color(60, 60, 60)
                pdf.multi_cell(0, 5, "  |  ".join(cells))
        elif line.startswith('- ') or line.startswith('* '):
            pdf.set_font("Helvetica", "", 9)
            pdf.set_text_color(30, 41, 59)
            pdf.multi_cell(0, 5.5, u'• ' + plain(line[2:]))
        elif re.match(r'^-{3,}$', line.strip()):
            pdf.ln(1)
        else:
            pdf.set_font("Helvetica", "", 9)
            pdf.set_text_color(30, 41, 59)
            pdf.multi_cell(0, 5.5, plain(line))

    pdf.output(pdf_path)
    print(f"SUCCESS (fpdf2): {pdf_path}")


if ensure_lib("reportlab"):
    try:
        try_reportlab(content, PDF_PATH)
        sys.exit(0)
    except Exception as e:
        print(f"reportlab failed: {e}")

if ensure_lib("fpdf", "fpdf2"):
    try:
        try_fpdf2(content, PDF_PATH)
        sys.exit(0)
    except Exception as e:
        print(f"fpdf2 failed: {e}")
        sys.exit(2)

print("ERROR: No PDF library available.")
sys.exit(3)
