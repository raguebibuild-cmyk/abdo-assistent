"""
gen_pdf_final.py
Generates a styled PDF from the research brief markdown.
Tries reportlab first; falls back to fpdf2; falls back to plain-text PDF via fpdf2.
"""
import sys
import os
import re
import subprocess

MD_PATH = r"d:\AI ZARA\ABDO ASSISTENT\.tmp\research-brief-ai-agentic-2026-05-10.md"
PDF_PATH = r"d:\AI ZARA\ABDO ASSISTENT\.tmp\research-brief-ai-agentic-2026-05-10.pdf"

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
        if r.returncode != 0:
            print(f"Failed to install {pip_name}: {r.stderr}")
            return False
        return True

with open(MD_PATH, "r", encoding="utf-8") as f:
    content = f.read()

os.makedirs(os.path.dirname(PDF_PATH), exist_ok=True)

def try_reportlab(content, pdf_path):
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import mm
    from reportlab.lib import colors
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer, HRFlowable, KeepTogether
    )
    from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY

    PAGE_W, PAGE_H = A4
    MARGIN = 22 * mm

    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=A4,
        rightMargin=MARGIN,
        leftMargin=MARGIN,
        topMargin=MARGIN,
        bottomMargin=MARGIN + 8*mm,
        title="AI Agentic Trends Research Brief — 2026-05-10",
        author="Research Brief Agent — degiabdo",
    )

    DARK = colors.HexColor("#1a1a2e")
    MID  = colors.HexColor("#16213e")
    BLUE = colors.HexColor("#0f3460")
    ACCENT = colors.HexColor("#e94560")
    GREY = colors.HexColor("#555555")
    LGREY = colors.HexColor("#888888")

    styles = getSampleStyleSheet()

    H1 = ParagraphStyle("H1", fontName="Helvetica-Bold",
        fontSize=20, leading=26, textColor=DARK,
        spaceAfter=3*mm, spaceBefore=0)
    META = ParagraphStyle("META", fontName="Helvetica",
        fontSize=9, leading=13, textColor=GREY, spaceAfter=1.5*mm)
    H2 = ParagraphStyle("H2", fontName="Helvetica-Bold",
        fontSize=13, leading=17, textColor=MID,
        spaceBefore=5*mm, spaceAfter=2*mm)
    H3 = ParagraphStyle("H3", fontName="Helvetica-Bold",
        fontSize=11, leading=15, textColor=BLUE,
        spaceBefore=4*mm, spaceAfter=1.5*mm)
    BODY = ParagraphStyle("BODY", fontName="Helvetica",
        fontSize=9.5, leading=14.5, textColor=colors.HexColor("#222222"),
        spaceAfter=2*mm, alignment=TA_JUSTIFY)
    LABEL = ParagraphStyle("LABEL", fontName="Helvetica-Bold",
        fontSize=9, leading=13, textColor=BLUE, spaceAfter=1*mm)
    BULLET = ParagraphStyle("BULLET", fontName="Helvetica",
        fontSize=9.5, leading=14, textColor=colors.HexColor("#222222"),
        spaceAfter=1.5*mm, leftIndent=8*mm, firstLineIndent=-4*mm)
    TABLE_HDR = ParagraphStyle("TABLE_HDR", fontName="Helvetica-Bold",
        fontSize=8.5, leading=11, textColor=MID)
    TABLE_ROW = ParagraphStyle("TABLE_ROW", fontName="Helvetica",
        fontSize=8, leading=11, textColor=colors.HexColor("#333333"))
    FOOTER_S = ParagraphStyle("FOOTER_S", fontName="Helvetica-Oblique",
        fontSize=8, leading=10, textColor=LGREY, alignment=TA_CENTER,
        spaceBefore=4*mm)
    CONF_HIGH = ParagraphStyle("CONF_HIGH", fontName="Helvetica-Bold",
        fontSize=9, leading=12, textColor=colors.HexColor("#1a7a1a"), spaceAfter=1*mm)

    def clean(text):
        """Escape ampersands and angle-brackets for ReportLab XML."""
        text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        return text

    def render_inline(text):
        """Convert **bold** and *italic* markdown to ReportLab XML tags."""
        # Bold+italic
        text = re.sub(r'\*\*\*(.+?)\*\*\*', r'<b><i>\1</i></b>', text)
        # Bold
        text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
        # Italic
        text = re.sub(r'\*(.+?)\*', r'<i>\1</i>', text)
        # Links — render URL inline, styled as blue
        text = re.sub(
            r'\[([^\]]+)\]\(([^\)]+)\)',
            r'<font color="#0f3460">\1</font>',
            text
        )
        # Inline code
        text = re.sub(r'`([^`]+)`', r'<font name="Courier" size="9">\1</font>', text)
        return text

    def safe_para(text, style):
        try:
            text = clean(text)
            text = render_inline(text)
            return Paragraph(text, style)
        except Exception as e:
            return Paragraph(clean(text), style)

    story = []
    lines = content.split('\n')
    i = 0

    in_table = False
    table_rows = []

    while i < len(lines):
        raw = lines[i]
        line = raw.rstrip()

        # H1
        if line.startswith('# ') and not line.startswith('## '):
            story.append(safe_para(line[2:], H1))
            story.append(HRFlowable(
                width="100%", thickness=1.5,
                color=ACCENT, spaceAfter=3*mm
            ))
            i += 1; continue

        # H2
        if line.startswith('## '):
            story.append(HRFlowable(
                width="100%", thickness=0.5,
                color=colors.HexColor("#cccccc"), spaceBefore=3*mm, spaceAfter=1*mm
            ))
            story.append(safe_para(line[3:], H2))
            i += 1; continue

        # H3
        if line.startswith('### '):
            story.append(safe_para(line[4:], H3))
            i += 1; continue

        # HR
        if re.match(r'^-{3,}$', line.strip()):
            story.append(HRFlowable(
                width="100%", thickness=0.4,
                color=colors.HexColor("#dddddd"), spaceBefore=2*mm, spaceAfter=2*mm
            ))
            i += 1; continue

        # Table header / row
        if line.startswith('|'):
            cells = [c.strip() for c in line.split('|')[1:-1]]
            if all(re.match(r'^[-: ]+$', c) for c in cells):
                i += 1; continue  # separator row
            if not in_table:
                in_table = True
                table_rows = []
            table_rows.append(cells)
            # Check if next line is still a table
            if i + 1 < len(lines) and lines[i+1].startswith('|'):
                i += 1; continue
            else:
                # Render accumulated table rows as paragraphs
                for idx, row in enumerate(table_rows):
                    sty = TABLE_HDR if idx == 0 else TABLE_ROW
                    row_text = "  |  ".join(row)
                    story.append(safe_para(row_text, sty))
                in_table = False
                table_rows = []
                i += 1; continue

        # Bullet
        if line.startswith('- ') or line.startswith('* '):
            story.append(safe_para(u'• ' + line[2:], BULLET))
            i += 1; continue

        # Numbered list
        if re.match(r'^\d+\. ', line):
            story.append(safe_para(line, BULLET))
            i += 1; continue

        # Italic footer line
        if re.match(r'^\*[^*].+[^*]\*$', line):
            story.append(safe_para(line.strip('*'), FOOTER_S))
            i += 1; continue

        # Confidence label
        if line.strip().startswith('**Confidence:**'):
            val = line.replace('**Confidence:**', '').strip()
            col = colors.HexColor('#1a7a1a') if val == 'HIGH' else colors.HexColor('#996600') if val == 'MEDIUM' else colors.HexColor('#aa0000')
            conf_style = ParagraphStyle("CS", fontName="Helvetica-Bold",
                fontSize=9, leading=12, textColor=col, spaceAfter=1*mm)
            story.append(Paragraph(f"Confidence: {val}", conf_style))
            i += 1; continue

        # Bold meta lines (**Key:** Value)
        if line.startswith('**') and ':**' in line:
            story.append(safe_para(line, LABEL))
            i += 1; continue

        # Empty line
        if not line.strip():
            story.append(Spacer(1, 1.5*mm))
            i += 1; continue

        # Default body
        story.append(safe_para(line, BODY))
        i += 1

    doc.build(story)
    print(f"SUCCESS (reportlab): {pdf_path}")
    return True

# Attempt 1: reportlab
if ensure_lib("reportlab"):
    try:
        success = try_reportlab(content, PDF_PATH)
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"reportlab failed: {e}")

# Attempt 2: fpdf2
if ensure_lib("fpdf", "fpdf2"):
    try:
        from fpdf import FPDF

        class PDF(FPDF):
            def header(self):
                self.set_font("Helvetica", "B", 10)
                self.set_text_color(26, 26, 46)
                self.cell(0, 8, "AI Agentic Trends — Research Brief — degiabdo", align="C")
                self.ln(4)
            def footer(self):
                self.set_y(-12)
                self.set_font("Helvetica", "I", 7)
                self.set_text_color(150, 150, 150)
                self.cell(0, 5, f"Research Brief Agent — degiabdo — 2026-05-10  |  Page {self.page_no()}", align="C")

        pdf = PDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=18)
        pdf.set_margins(20, 20, 20)

        def plain(text):
            text = re.sub(r'\*\*\*(.+?)\*\*\*', r'\1', text)
            text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
            text = re.sub(r'\*(.+?)\*', r'\1', text)
            text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
            text = re.sub(r'`([^`]+)`', r'\1', text)
            return text

        for line in content.split('\n'):
            line = line.rstrip()
            if not line:
                pdf.ln(2)
            elif line.startswith('# ') and not line.startswith('## '):
                pdf.set_font("Helvetica", "B", 16)
                pdf.set_text_color(26, 26, 46)
                pdf.multi_cell(0, 9, plain(line[2:]))
                pdf.ln(2)
            elif line.startswith('## '):
                pdf.set_font("Helvetica", "B", 12)
                pdf.set_text_color(22, 33, 62)
                pdf.multi_cell(0, 7, plain(line[3:]))
                pdf.ln(1)
            elif line.startswith('### '):
                pdf.set_font("Helvetica", "B", 10)
                pdf.set_text_color(15, 52, 96)
                pdf.multi_cell(0, 6, plain(line[4:]))
            elif re.match(r'^-{3,}$', line.strip()):
                pdf.ln(1)
            elif line.startswith('|'):
                cells = [c.strip() for c in line.split('|')[1:-1]]
                if all(re.match(r'^[-: ]+$', c) for c in cells):
                    continue
                pdf.set_font("Helvetica", "", 7.5)
                pdf.set_text_color(60, 60, 60)
                pdf.multi_cell(0, 5, "  |  ".join(cells))
            elif line.startswith('- ') or line.startswith('* '):
                pdf.set_font("Helvetica", "", 9)
                pdf.set_text_color(34, 34, 34)
                pdf.multi_cell(0, 5.5, u'• ' + plain(line[2:]))
            else:
                pdf.set_font("Helvetica", "", 9)
                pdf.set_text_color(34, 34, 34)
                pdf.multi_cell(0, 5.5, plain(line))

        pdf.output(PDF_PATH)
        print(f"SUCCESS (fpdf2): {PDF_PATH}")
        sys.exit(0)
    except Exception as e:
        print(f"fpdf2 failed: {e}")
        sys.exit(2)

print("ERROR: No PDF library available and installation failed.")
sys.exit(3)
