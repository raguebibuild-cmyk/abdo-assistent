"""
generate_research_pdf.py
One-job script: reads a markdown file path as argv[1], outputs a PDF at argv[2].
Uses reportlab if available, falls back to fpdf2.
"""
import sys
import os
import re
from pathlib import Path as _Path
_equipdir = str(_Path(__file__).parent)
if _equipdir not in sys.path:
    sys.path.insert(0, _equipdir)
from brand import page_callback as _brand_cb

def strip_markdown(text):
    """Minimal markdown to plain text for PDF rendering."""
    # Remove code blocks
    text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
    # Remove inline code
    text = re.sub(r'`([^`]+)`', r'\1', text)
    # Remove bold/italic
    text = re.sub(r'\*\*\*(.+?)\*\*\*', r'\1', text)
    text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
    text = re.sub(r'\*(.+?)\*', r'\1', text)
    # Remove links — keep text
    text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
    # Remove horizontal rules
    text = re.sub(r'^-{3,}$', '', text, flags=re.MULTILINE)
    # Remove table rows (pipes)
    text = re.sub(r'^\|.*\|$', '', text, flags=re.MULTILINE)
    return text

def generate_with_reportlab(md_path, pdf_path, content):
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import mm
    from reportlab.lib import colors
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
    from reportlab.lib.enums import TA_LEFT, TA_CENTER

    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=A4,
        rightMargin=20*mm,
        leftMargin=20*mm,
        topMargin=20*mm,
        bottomMargin=20*mm
    )

    styles = getSampleStyleSheet()

    style_h1 = ParagraphStyle(
        'H1', parent=styles['Heading1'],
        fontSize=18, spaceAfter=6, textColor=colors.HexColor('#012240'),
        leading=22
    )
    style_h2 = ParagraphStyle(
        'H2', parent=styles['Heading2'],
        fontSize=13, spaceAfter=4, spaceBefore=10,
        textColor=colors.HexColor('#012240'), leading=18
    )
    style_h3 = ParagraphStyle(
        'H3', parent=styles['Heading3'],
        fontSize=11, spaceAfter=3, spaceBefore=8,
        textColor=colors.HexColor('#4f4cee'), leading=15
    )
    style_body = ParagraphStyle(
        'Body', parent=styles['Normal'],
        fontSize=9.5, spaceAfter=4, leading=14
    )
    style_meta = ParagraphStyle(
        'Meta', parent=styles['Normal'],
        fontSize=8.5, textColor=colors.HexColor('#666666'), spaceAfter=3, leading=12
    )
    style_label = ParagraphStyle(
        'Label', parent=styles['Normal'],
        fontSize=9, textColor=colors.HexColor('#4f4cee'),
        spaceAfter=2, leading=12, fontName='Helvetica-Bold'
    )
    style_footer = ParagraphStyle(
        'Footer', parent=styles['Normal'],
        fontSize=8, textColor=colors.grey, alignment=TA_CENTER, leading=10
    )

    story = []
    lines = content.split('\n')

    i = 0
    while i < len(lines):
        line = lines[i].rstrip()

        if line.startswith('# ') and not line.startswith('## '):
            story.append(Paragraph(line[2:], style_h1))
            story.append(Spacer(1, 4*mm))
        elif line.startswith('## '):
            story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#cccccc'), spaceAfter=2))
            story.append(Paragraph(line[3:], style_h2))
        elif line.startswith('### '):
            story.append(Paragraph(line[4:], style_h3))
        elif line.startswith('**') and line.endswith('**') and ':' not in line:
            story.append(Paragraph(line.strip('*'), style_label))
        elif line.startswith('**') and ':**' in line:
            # Bold label: value
            clean = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', line)
            clean = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', clean)
            story.append(Paragraph(clean, style_body))
        elif line.startswith('- ') or line.startswith('* '):
            bullet_text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', line[2:])
            bullet_text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', bullet_text)
            story.append(Paragraph(f'• {bullet_text}', style_body))
        elif line.startswith('|') and '|' in line[1:]:
            # Skip table lines (rendered inline in sections)
            pass
        elif line.startswith('---'):
            story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#eeeeee'), spaceBefore=2, spaceAfter=2))
        elif line.startswith('*') and line.endswith('*') and not line.startswith('**'):
            story.append(Paragraph(f'<i>{line.strip("*")}</i>', style_footer))
        elif line.strip() == '':
            story.append(Spacer(1, 2*mm))
        else:
            clean = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', line)
            clean = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', clean)
            story.append(Paragraph(clean, style_body))

        i += 1

    doc.build(story, onFirstPage=_brand_cb, onLaterPages=_brand_cb)
    print(f"PDF generated: {pdf_path}")

def generate_with_fpdf(md_path, pdf_path, content):
    from fpdf import FPDF

    class PDF(FPDF):
        def header(self):
            pass
        def header(self):
            self.set_fill_color(1, 34, 64)      # #012240 navy
            self.rect(0, 0, self.w, 12, 'F')
            self.set_fill_color(232, 152, 32)    # #e89820 amber
            self.rect(0, 12, self.w, 1.2, 'F')
            self.set_font('Helvetica', 'B', 10)
            self.set_text_color(255, 255, 255)
            self.set_y(2)
            self.cell(0, 8, 'degiabdo', align='R')
            self.ln(6)
        def footer(self):
            self.set_y(-12)
            self.set_font('Helvetica', 'I', 7)
            self.set_text_color(100, 116, 139)   # #64748b muted
            self.cell(0, 5, f'degiabdo  |  Page {self.page_no()}', align='C')

    pdf = PDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_margins(20, 20, 20)

    plain = strip_markdown(content)
    lines = plain.split('\n')

    for line in lines:
        line = line.rstrip()
        if not line:
            pdf.ln(3)
            continue
        # Detect headings by original markdown (we run both passes)
        pdf.set_font('Helvetica', '', 9)
        pdf.set_text_color(30, 30, 30)
        pdf.multi_cell(0, 5, line)

    pdf.output(pdf_path)
    print(f"PDF generated (fpdf fallback): {pdf_path}")

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python generate_research_pdf.py <input.md> <output.pdf>")
        sys.exit(1)

    md_path = sys.argv[1]
    pdf_path = sys.argv[2]

    if not os.path.exists(md_path):
        print(f"Error: markdown file not found: {md_path}")
        sys.exit(1)

    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Ensure output directory exists
    os.makedirs(os.path.dirname(pdf_path), exist_ok=True)

    # Try reportlab first, then fpdf2
    try:
        generate_with_reportlab(md_path, pdf_path, content)
    except ImportError:
        print("reportlab not found, trying fpdf2...")
        try:
            generate_with_fpdf(md_path, pdf_path, content)
        except ImportError:
            print("Neither reportlab nor fpdf2 available. Install one: pip install reportlab OR pip install fpdf2")
            sys.exit(2)
