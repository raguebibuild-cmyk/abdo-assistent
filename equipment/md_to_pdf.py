import re
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    HRFlowable, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle,
)

PAGE_W, PAGE_H = A4

NAVY            = colors.HexColor('#1a3a5c')
BLUE            = colors.HexColor('#2563eb')
CODE_BG         = colors.HexColor('#f1f5f9')
CODE_FG         = colors.HexColor('#374151')
ALT_ROW         = colors.HexColor('#f8fafc')
BORDER          = colors.HexColor('#e2e8f0')
HR_COLOR        = colors.HexColor('#cbd5e1')
BLOCKQUOTE_BG   = colors.HexColor('#fffbeb')
BLOCKQUOTE_LINE = colors.HexColor('#f59e0b')
TEXT            = colors.HexColor('#1e293b')
MUTED           = colors.HexColor('#64748b')


def make_styles():
    base = getSampleStyleSheet()

    def s(name, parent='Normal', **kw):
        return ParagraphStyle(name, parent=base[parent], **kw)

    return {
        'h1': s('H1', 'Title', fontSize=20, textColor=NAVY,
                spaceAfter=4, spaceBefore=0, leading=26, fontName='Helvetica-Bold'),
        'h2': s('H2', 'Heading2', fontSize=13, textColor=NAVY,
                spaceAfter=4, spaceBefore=14, leading=18, fontName='Helvetica-Bold'),
        'h3': s('H3', 'Heading3', fontSize=11, textColor=BLUE,
                spaceAfter=3, spaceBefore=10, leading=15, fontName='Helvetica-Bold'),
        'body': s('Body', 'Normal', fontSize=9.5, textColor=TEXT,
                  leading=14, spaceAfter=3, fontName='Helvetica'),
        'bullet': s('Bullet', 'Normal', fontSize=9.5, textColor=TEXT,
                    leading=13, spaceAfter=2, leftIndent=14, fontName='Helvetica'),
        'bq': s('BQ', 'Normal', fontSize=9, leading=13,
                textColor=colors.HexColor('#92400e'), leftIndent=10, rightIndent=10,
                spaceBefore=4, spaceAfter=4, fontName='Helvetica-Oblique'),
        'footer': s('Footer', 'Normal', fontSize=8.5, textColor=MUTED,
                    fontName='Helvetica-Oblique'),
    }


def xml_escape(text):
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def inline_fmt(text):
    parts = re.split(r'(`[^`\n]+`)', text)
    out = []
    for seg in parts:
        if seg.startswith('`') and seg.endswith('`') and len(seg) > 1:
            inner = xml_escape(seg[1:-1])
            out.append(f'<font name="Courier" size="8.5" color="#4b5563">{inner}</font>')
        else:
            s = xml_escape(seg)
            s = re.sub(r'\*\*([^*\n]+)\*\*', lambda m: '<b>' + m.group(1) + '</b>', s)
            s = re.sub(r'(?<!\*)\*([^*\n]+)\*(?!\*)', lambda m: '<i>' + m.group(1) + '</i>', s)
            out.append(s)
    return ''.join(out)


def build_table(raw_lines, styles):
    rows = []
    for line in raw_lines:
        if re.match(r'^\s*\|[-:| ]+\|\s*$', line):
            continue
        cells = [c.strip() for c in line.strip().strip('|').split('|')]
        rows.append(cells)
    if not rows:
        return None

    avail = PAGE_W - 4 * cm
    col_count = max(len(r) for r in rows)
    col_widths = [avail / col_count] * col_count

    fmt_rows = []
    for ri, row in enumerate(rows):
        while len(row) < col_count:
            row.append('')
        if ri == 0:
            cell_style = ParagraphStyle(
                'TH', parent=styles['body'],
                fontName='Helvetica-Bold', textColor=colors.white, fontSize=9)
        else:
            cell_style = styles['body']
        fmt_rows.append([Paragraph(inline_fmt(c), cell_style) for c in row])

    tbl = Table(fmt_rows, colWidths=col_widths, repeatRows=1)
    tbl.setStyle(TableStyle([
        ('BACKGROUND',     (0, 0), (-1, 0),  NAVY),
        ('TEXTCOLOR',      (0, 0), (-1, 0),  colors.white),
        ('FONTNAME',       (0, 0), (-1, 0),  'Helvetica-Bold'),
        ('FONTSIZE',       (0, 0), (-1, -1), 9),
        ('GRID',           (0, 0), (-1, -1), 0.4, BORDER),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, ALT_ROW]),
        ('VALIGN',         (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING',     (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING',  (0, 0), (-1, -1), 5),
        ('LEFTPADDING',    (0, 0), (-1, -1), 7),
        ('RIGHTPADDING',   (0, 0), (-1, -1), 7),
    ]))
    return tbl


def build_code_block(code_lines, styles):
    while code_lines and not code_lines[-1].strip():
        code_lines.pop()
    if not code_lines:
        return []

    line_style = ParagraphStyle(
        'CodeLine', fontName='Courier', fontSize=7.5, leading=11,
        textColor=CODE_FG, leftIndent=10, rightIndent=10,
        spaceAfter=0, spaceBefore=0, backColor=CODE_BG,
    )

    top_bar = Table([['']], colWidths=[PAGE_W - 4 * cm], rowHeights=[4])
    top_bar.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), CODE_BG),
        ('LINEABOVE',  (0, 0), (-1, 0),  0.5, BORDER),
        ('LINEBEFORE', (0, 0), (0, -1),  0.5, BORDER),
        ('LINEAFTER',  (0, 0), (-1, -1), 0.5, BORDER),
    ]))
    bottom_bar = Table([['']], colWidths=[PAGE_W - 4 * cm], rowHeights=[4])
    bottom_bar.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), CODE_BG),
        ('LINEBELOW',  (0, 0), (-1, -1), 0.5, BORDER),
        ('LINEBEFORE', (0, 0), (0, -1),  0.5, BORDER),
        ('LINEAFTER',  (0, 0), (-1, -1), 0.5, BORDER),
    ]))

    flowables = [Spacer(1, 3), top_bar]
    for ln in code_lines:
        escaped = xml_escape(ln) if ln.strip() else '&nbsp;'
        flowables.append(Paragraph(escaped, line_style))
    flowables.append(bottom_bar)
    flowables.append(Spacer(1, 5))
    return flowables


def convert(src: Path, dst: Path):
    styles = make_styles()
    story = []
    lines = src.read_text(encoding='utf-8').splitlines()

    in_code = False
    code_fence = None
    code_buf = []
    table_buf = []

    def flush_table():
        if table_buf:
            tbl = build_table(list(table_buf), styles)
            if tbl:
                story.append(Spacer(1, 4))
                story.append(tbl)
                story.append(Spacer(1, 6))
            table_buf.clear()

    def flush_code():
        if code_buf:
            story.extend(build_code_block(list(code_buf), styles))
            code_buf.clear()

    i = 0
    while i < len(lines):
        line = lines[i]

        fence_open = re.match(r'^(`{3,4})', line)
        if not in_code and fence_open:
            flush_table()
            code_fence = fence_open.group(1)
            in_code = True
            i += 1
            continue

        if in_code:
            closing = re.match(r'^(`{3,4})\s*$', line)
            if closing and closing.group(1) == code_fence:
                flush_code()
                in_code = False
                code_fence = None
            else:
                code_buf.append(line)
            i += 1
            continue

        if line.strip().startswith('|'):
            table_buf.append(line)
            i += 1
            continue
        else:
            flush_table()

        m = re.match(r'^(#{1,3}) (.+)', line)
        if m:
            level = len(m.group(1))
            text = inline_fmt(m.group(2))
            story.append(Paragraph(text, styles[f'h{level}']))
            if level == 1:
                story.append(HRFlowable(width='100%', thickness=2, color=NAVY, spaceAfter=8))
            elif level == 2:
                story.append(HRFlowable(width='100%', thickness=0.5, color=BORDER, spaceAfter=4))
            i += 1
            continue

        if re.match(r'^-{3,}\s*$', line):
            story.append(Spacer(1, 4))
            story.append(HRFlowable(width='100%', thickness=0.5, color=HR_COLOR, spaceAfter=4))
            i += 1
            continue

        if line.startswith('> '):
            content = inline_fmt(line[2:])
            bq = Table([[Paragraph(content, styles['bq'])]], colWidths=[PAGE_W - 4 * cm])
            bq.setStyle(TableStyle([
                ('BACKGROUND',    (0, 0), (-1, -1), BLOCKQUOTE_BG),
                ('LINEBEFORE',    (0, 0), (0, -1),  3, BLOCKQUOTE_LINE),
                ('BOX',           (0, 0), (-1, -1), 0.5, BLOCKQUOTE_LINE),
                ('LEFTPADDING',   (0, 0), (-1, -1), 12),
                ('RIGHTPADDING',  (0, 0), (-1, -1), 12),
                ('TOPPADDING',    (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ]))
            story.append(Spacer(1, 4))
            story.append(bq)
            story.append(Spacer(1, 6))
            i += 1
            continue

        bullet_m = re.match(r'^(\s*)- (.+)', line)
        if bullet_m:
            indent = len(bullet_m.group(1)) // 2
            content = bullet_m.group(2)
            cb_m = re.match(r'^\[([ x])\] (.+)', content)
            if cb_m:
                box = '&#9745;' if cb_m.group(1) == 'x' else '&#9744;'
                text = f'{box} {inline_fmt(cb_m.group(2))}'
            else:
                text = f'&#8226; {inline_fmt(content)}'
            sty = ParagraphStyle(f'B{indent}', parent=styles['bullet'], leftIndent=14 + indent * 14)
            story.append(Paragraph(text, sty))
            i += 1
            continue

        num_m = re.match(r'^(\s*)(\d+)\. (.+)', line)
        if num_m:
            indent = len(num_m.group(1)) // 2
            text = f'{num_m.group(2)}. {inline_fmt(num_m.group(3))}'
            sty = ParagraphStyle(f'N{indent}', parent=styles['bullet'], leftIndent=14 + indent * 14)
            story.append(Paragraph(text, sty))
            i += 1
            continue

        if re.match(r'^\*[^*].+[^*]\*$', line):
            story.append(Spacer(1, 6))
            story.append(Paragraph(line[1:-1], styles['footer']))
            i += 1
            continue

        if not line.strip():
            story.append(Spacer(1, 3))
            i += 1
            continue

        story.append(Paragraph(inline_fmt(line), styles['body']))
        i += 1

    flush_table()
    flush_code()

    doc = SimpleDocTemplate(
        str(dst), pagesize=A4,
        leftMargin=2*cm, rightMargin=2*cm,
        topMargin=2*cm, bottomMargin=2*cm,
        author='degiabdo — Abderrahim',
    )
    doc.build(story)
    print(f'  -> {dst}')


if __name__ == '__main__':
    import sys
    if len(sys.argv) == 3:
        convert(Path(sys.argv[1]), Path(sys.argv[2]))
    else:
        print("Usage: python md_to_pdf.py <input.md> <output.pdf>")
        sys.exit(1)
