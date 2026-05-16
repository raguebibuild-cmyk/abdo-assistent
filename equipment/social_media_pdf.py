"""
social_media_pdf.py
CLI PDF generator for Social Media Content markdown files.
Usage: python social_media_pdf.py <input.md> <output.pdf>
Tries reportlab first; falls back to fpdf2.
Platform section headers (## LinkedIn Post, ## Facebook Post, ## Instagram Post)
render in each platform's brand color.
"""
import sys, os, re, subprocess

if len(sys.argv) != 3:
    print("Usage: python social_media_pdf.py <input.md> <output.pdf>")
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
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable

    MARGIN = 22 * mm
    DARK   = colors.HexColor("#1a1a2e")
    MID    = colors.HexColor("#16213e")
    BLUE   = colors.HexColor("#0f3460")
    ACCENT = colors.HexColor("#e94560")
    LGREY  = colors.HexColor("#888888")
    LI_COL = colors.HexColor("#0077B5")
    FB_COL = colors.HexColor("#1877F2")
    IG_COL = colors.HexColor("#E1306C")

    doc = SimpleDocTemplate(
        pdf_path, pagesize=A4,
        rightMargin=MARGIN, leftMargin=MARGIN,
        topMargin=MARGIN, bottomMargin=MARGIN + 8*mm,
        title="Social Media Content Pack — degiabdo",
        author="Social Media Repurposing Agent — degiabdo",
    )

    H1     = ParagraphStyle("H1",     fontName="Helvetica-Bold",    fontSize=20, leading=26,   textColor=DARK,   spaceAfter=3*mm)
    H2_LI  = ParagraphStyle("H2_LI",  fontName="Helvetica-Bold",    fontSize=14, leading=18,   textColor=LI_COL, spaceBefore=6*mm, spaceAfter=2*mm)
    H2_FB  = ParagraphStyle("H2_FB",  fontName="Helvetica-Bold",    fontSize=14, leading=18,   textColor=FB_COL, spaceBefore=6*mm, spaceAfter=2*mm)
    H2_IG  = ParagraphStyle("H2_IG",  fontName="Helvetica-Bold",    fontSize=14, leading=18,   textColor=IG_COL, spaceBefore=6*mm, spaceAfter=2*mm)
    H2_DEF = ParagraphStyle("H2_DEF", fontName="Helvetica-Bold",    fontSize=14, leading=18,   textColor=MID,    spaceBefore=6*mm, spaceAfter=2*mm)
    H3     = ParagraphStyle("H3",     fontName="Helvetica-Bold",    fontSize=11, leading=15,   textColor=BLUE,   spaceBefore=4*mm, spaceAfter=1.5*mm)
    BODY   = ParagraphStyle("BODY",   fontName="Helvetica",         fontSize=10, leading=15,   textColor=colors.HexColor("#222222"), spaceAfter=2*mm)
    BULLET = ParagraphStyle("BULLET", fontName="Helvetica",         fontSize=10, leading=14,   textColor=colors.HexColor("#222222"), spaceAfter=1.5*mm, leftIndent=8*mm, firstLineIndent=-4*mm)
    LABEL  = ParagraphStyle("LABEL",  fontName="Helvetica-Bold",    fontSize=9,  leading=13,   textColor=BLUE,   spaceAfter=1*mm)
    TH     = ParagraphStyle("TH",     fontName="Helvetica-Bold",    fontSize=8.5, leading=11,  textColor=MID)
    TR     = ParagraphStyle("TR",     fontName="Helvetica",         fontSize=8,   leading=11,  textColor=colors.HexColor("#333333"))
    FOOT   = ParagraphStyle("FOOT",   fontName="Helvetica-Oblique", fontSize=8,  leading=10,   textColor=LGREY,  spaceBefore=4*mm)

    def h2_style(title):
        t = title.lower()
        if 'linkedin' in t:  return H2_LI
        if 'facebook' in t:  return H2_FB
        if 'instagram' in t: return H2_IG
        return H2_DEF

    def clean(t):
        return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    def inline(t):
        t = re.sub(r'\*\*\*(.+?)\*\*\*', r'<b><i>\1</i></b>', t)
        t = re.sub(r'\*\*(.+?)\*\*',     r'<b>\1</b>', t)
        t = re.sub(r'\*(.+?)\*',         r'<i>\1</i>', t)
        t = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'<font color="#0f3460">\1</font>', t)
        t = re.sub(r'`([^`]+)`', r'<font name="Courier" size="9">\1</font>', t)
        return t

    def para(text, style):
        try:
            return Paragraph(inline(clean(text)), style)
        except Exception:
            return Paragraph(clean(text), style)

    story = []
    lines = content.split('\n')
    i = 0
    table_rows = []

    while i < len(lines):
        line = lines[i].rstrip()

        if line.startswith('# ') and not line.startswith('## '):
            story.append(para(line[2:], H1))
            story.append(HRFlowable(width="100%", thickness=1.5, color=ACCENT, spaceAfter=3*mm))
        elif line.startswith('## '):
            title = line[3:]
            story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#cccccc"), spaceBefore=3*mm, spaceAfter=1*mm))
            story.append(para(title, h2_style(title)))
        elif line.startswith('### '):
            story.append(para(line[4:], H3))
        elif re.match(r'^-{3,}$', line.strip()):
            story.append(HRFlowable(width="100%", thickness=0.4, color=colors.HexColor("#dddddd"), spaceBefore=2*mm, spaceAfter=2*mm))
        elif line.startswith('|'):
            cells = [c.strip() for c in line.split('|')[1:-1]]
            if not all(re.match(r'^[-: ]+$', c) for c in cells):
                table_rows.append(cells)
            if not (i + 1 < len(lines) and lines[i+1].startswith('|')):
                for idx, row in enumerate(table_rows):
                    story.append(para("  |  ".join(row), TH if idx == 0 else TR))
                table_rows = []
        elif line.startswith('- ') or line.startswith('* '):
            story.append(para(u'• ' + line[2:], BULLET))
        elif re.match(r'^\d+\. ', line):
            story.append(para(line, BULLET))
        elif line.startswith('**') and ':**' in line:
            story.append(para(line, LABEL))
        elif re.match(r'^\*[^*].+[^*]\*$', line):
            story.append(para(line.strip('*'), FOOT))
        elif not line.strip():
            story.append(Spacer(1, 1.5*mm))
        else:
            story.append(para(line, BODY))

        i += 1

    doc.build(story)
    print(f"SUCCESS (reportlab): {pdf_path}")
    return True

def try_fpdf2(content, pdf_path):
    from fpdf import FPDF

    class PDF(FPDF):
        def header(self):
            self.set_font("Helvetica", "B", 10)
            self.set_text_color(26, 26, 46)
            self.cell(0, 8, "Social Media Content Pack — degiabdo", align="C")
            self.ln(4)
        def footer(self):
            self.set_y(-12)
            self.set_font("Helvetica", "I", 7)
            self.set_text_color(150, 150, 150)
            self.cell(0, 5, f"Social Media Repurposing Agent — degiabdo  |  Page {self.page_no()}", align="C")

    pdf = PDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=18)
    pdf.set_margins(20, 20, 20)

    def plain(t):
        t = re.sub(r'\*\*\*(.+?)\*\*\*', r'\1', t)
        t = re.sub(r'\*\*(.+?)\*\*', r'\1', t)
        t = re.sub(r'\*(.+?)\*', r'\1', t)
        t = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', t)
        t = re.sub(r'`([^`]+)`', r'\1', t)
        return t

    for line in content.split('\n'):
        line = line.rstrip()
        if not line:
            pdf.ln(2)
        elif line.startswith('# ') and not line.startswith('## '):
            pdf.set_font("Helvetica", "B", 16); pdf.set_text_color(26, 26, 46)
            pdf.multi_cell(0, 9, plain(line[2:]))
        elif line.startswith('## '):
            pdf.set_font("Helvetica", "B", 13)
            t = line[3:].lower()
            if 'linkedin' in t:    pdf.set_text_color(0, 119, 181)
            elif 'facebook' in t:  pdf.set_text_color(24, 119, 242)
            elif 'instagram' in t: pdf.set_text_color(225, 48, 108)
            else:                  pdf.set_text_color(22, 33, 62)
            pdf.multi_cell(0, 7, plain(line[3:]))
        elif line.startswith('### '):
            pdf.set_font("Helvetica", "B", 10); pdf.set_text_color(15, 52, 96)
            pdf.multi_cell(0, 6, plain(line[4:]))
        elif line.startswith('|'):
            cells = [c.strip() for c in line.split('|')[1:-1]]
            if not all(re.match(r'^[-: ]+$', c) for c in cells):
                pdf.set_font("Helvetica", "", 7.5); pdf.set_text_color(60, 60, 60)
                pdf.multi_cell(0, 5, "  |  ".join(cells))
        elif line.startswith('- ') or line.startswith('* '):
            pdf.set_font("Helvetica", "", 9); pdf.set_text_color(34, 34, 34)
            pdf.multi_cell(0, 5.5, u'• ' + plain(line[2:]))
        elif re.match(r'^-{3,}$', line.strip()):
            pdf.ln(1)
        else:
            pdf.set_font("Helvetica", "", 9); pdf.set_text_color(34, 34, 34)
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
