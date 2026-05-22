"""
invoice_pdf.py — DEGISaaS branded invoice PDF generator.
Parses a populated invoice markdown file and renders a professional A4 invoice.

Features:
  - Brand header/footer via brand.py (logo, navy/amber)
  - Line items table: Item | Qty | Unit Price | Amount
  - Right-aligned summary block with amber-highlighted total
  - Status field: if "Paid", draws a diagonal green PAID watermark on every page
  - Auto-creates output directory if it doesn't exist

Usage:
    python equipment/invoice_pdf.py <input.md> <output.pdf>

Recommended output path:
    invoices/INV-[YYYY-MM-DD]-[ClientName].pdf
"""
import re
import sys
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    HRFlowable, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle,
)

sys.path.insert(0, str(Path(__file__).parent))
from brand import (
    page_callback as _brand_cb,
    C_NAVY, C_AMBER, C_INDIGO, C_TEXT, C_MUTED, C_BORDER, C_ALTROW,
)

if len(sys.argv) != 3:
    print("Usage: python equipment/invoice_pdf.py <input.md> <output.pdf>")
    sys.exit(1)

md_path  = Path(sys.argv[1])
pdf_path = Path(sys.argv[2])

if not md_path.exists():
    print(f"Error: {md_path} not found")
    sys.exit(1)

# ── Colours ───────────────────────────────────────────────────────────────────
PAGE_W, PAGE_H = A4
AVAIL_W = PAGE_W - 4 * cm

NAVY   = colors.HexColor(C_NAVY)
AMBER  = colors.HexColor(C_AMBER)
INDIGO = colors.HexColor(C_INDIGO)
TEXT   = colors.HexColor(C_TEXT)
MUTED  = colors.HexColor(C_MUTED)
BORDER = colors.HexColor(C_BORDER)
ALT    = colors.HexColor(C_ALTROW)
WHITE  = colors.white
# PAID watermark — green #16a34a at 18% opacity
PAID_COLOR = colors.Color(22 / 255, 163 / 255, 74 / 255, alpha=0.18)

# ── Styles ────────────────────────────────────────────────────────────────────
_base = getSampleStyleSheet()


def S(name, parent='Normal', **kw):
    return ParagraphStyle(name, parent=_base[parent], **kw)


TITLE = S('InvTitle', fontSize=26, textColor=NAVY,   fontName='Helvetica-Bold', leading=30)
NUM   = S('InvNum',   fontSize=9,  textColor=MUTED,  fontName='Helvetica', spaceBefore=3)
META  = S('Meta',     fontSize=9.5,textColor=TEXT,   fontName='Helvetica', leading=15, spaceAfter=2)
LABEL = S('Label',    fontSize=7.5,textColor=MUTED,  fontName='Helvetica-Bold', spaceAfter=2)
VAL   = S('Val',      fontSize=10, textColor=TEXT,   fontName='Helvetica', spaceAfter=0)
SECT  = S('Sect',     fontSize=8,  textColor=INDIGO, fontName='Helvetica-Bold', spaceBefore=14, spaceAfter=6)
BODY  = S('Body',     fontSize=9.5,textColor=TEXT,   fontName='Helvetica', leading=14, spaceAfter=3)
TH    = S('TH',       fontSize=9,  textColor=WHITE,  fontName='Helvetica-Bold')
TD    = S('TD',       fontSize=9.5,textColor=TEXT,   fontName='Helvetica', leading=13)
TOT_L = S('TotL',     fontSize=10, textColor=TEXT,   fontName='Helvetica-Bold')
TOT_V = S('TotV',     fontSize=11, textColor=NAVY,   fontName='Helvetica-Bold')
SMALL = S('Small',    fontSize=8.5,textColor=MUTED,  fontName='Helvetica', leading=13, spaceAfter=2)


# ── Page callbacks ────────────────────────────────────────────────────────────

def _paid_watermark(canvas, _doc):
    """Diagonal PAID watermark — drawn after the brand header/footer."""
    canvas.saveState()
    canvas.setFont('Helvetica-Bold', 100)
    canvas.setFillColor(PAID_COLOR)
    canvas.translate(PAGE_W / 2, PAGE_H / 2)
    canvas.rotate(45)
    canvas.drawCentredString(0, 0, 'PAID')
    canvas.restoreState()


def _make_page_cb(paid: bool):
    def cb(canvas, doc):
        _brand_cb(canvas, doc)
        if paid:
            _paid_watermark(canvas, doc)
    return cb


# ── Helpers ───────────────────────────────────────────────────────────────────

def _esc(text: str) -> str:
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def _bold_md(text: str) -> str:
    return re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)


def _field(raw: str, key: str) -> str:
    m = re.search(rf'\*\*{re.escape(key)}:\*\*\s*(.+?)(?:\n|$)', raw)
    return m.group(1).strip() if m else ''


# ── Parse markdown ────────────────────────────────────────────────────────────
raw = md_path.read_text(encoding='utf-8')

inv_from   = _field(raw, 'From')
inv_to     = _field(raw, 'To')
inv_number = _field(raw, 'Invoice number')
inv_date   = _field(raw, 'Date')
inv_due    = _field(raw, 'Due')
status     = _field(raw, 'Status')
bank       = _field(raw, 'Bank')
iban       = _field(raw, 'IBAN')
bic        = _field(raw, 'BIC / SWIFT')
pay_ref    = _field(raw, 'Payment reference')

is_paid = status.strip().lower() == 'paid'

# Line items table — supports any number of columns
item_rows: list[list[str]] = []
in_items = False
for line in raw.splitlines():
    if re.search(r'##\s+(Line Items|Items|Services Rendered)', line):
        in_items = True
        continue
    if in_items and line.startswith('##'):
        break
    if in_items and '|' in line and not re.match(r'^\s*\|[-:| ]+\|', line):
        cells = [_esc(c.strip()) for c in line.strip().strip('|').split('|')]
        if any(cells):
            item_rows.append(cells)

# Summary — subtotal / tax / total
subtotal = tax = total_due = ''
in_sum = False
for line in raw.splitlines():
    if re.search(r'##\s+(Summary|Totals)', line):
        in_sum = True
        continue
    if in_sum and line.startswith('##'):
        break
    if in_sum and '|' in line and not re.match(r'^\s*\|[-:| ]+\|', line):
        cells = [c.strip().strip('*') for c in line.strip().strip('|').split('|')]
        if len(cells) >= 2 and cells[0]:
            lbl = cells[0].lower()
            if 'subtotal' in lbl:
                subtotal = _esc(cells[1])
            elif 'tax' in lbl or 'vat' in lbl:
                tax = _esc(cells[1])
            elif 'total' in lbl:
                total_due = _esc(cells[1])

# Notes / payment terms (plain lines after Payment Details, skipping bold fields)
notes_lines: list[str] = []
in_notes = False
for line in raw.splitlines():
    if '## Payment Details' in line:
        in_notes = True
        continue
    if in_notes:
        s = line.strip()
        if not s or s == '---':
            continue
        if re.match(r'^\*\*.+:\*\*', s):
            continue
        notes_lines.append(s)

# ── Build story ───────────────────────────────────────────────────────────────
story = []

# ── Top block: title + number (left) | dates + status (right) ─────────────────
meta_right: list = []
if inv_date:
    meta_right.append(Paragraph(f'<b>Date</b>   {_esc(inv_date)}', META))
if inv_due:
    meta_right.append(Paragraph(f'<b>Due</b>    {_esc(inv_due)}', META))
if status:
    sc = '#16a34a' if is_paid else '#dc2626'
    meta_right.append(Paragraph(
        f'<b>Status</b> <font color="{sc}"><b>{_esc(status.upper())}</b></font>', META
    ))

title_cell: list = [Paragraph('INVOICE', TITLE)]
if inv_number:
    title_cell.append(Paragraph(_esc(inv_number), NUM))

top = Table(
    [[title_cell, meta_right or [Paragraph('', META)]]],
    colWidths=[AVAIL_W * 0.55, AVAIL_W * 0.45],
)
top.setStyle(TableStyle([
    ('VALIGN',        (0, 0), (-1, -1), 'BOTTOM'),
    ('ALIGN',         (1, 0), (1, -1),  'RIGHT'),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
]))
story.append(top)
story.append(HRFlowable(width='100%', thickness=2, color=AMBER, spaceAfter=12, spaceBefore=0))

# ── From / To ─────────────────────────────────────────────────────────────────
from_cell = [Paragraph('FROM', LABEL), Paragraph(_esc(inv_from) or '—', VAL)]
to_cell   = [Paragraph('TO',   LABEL), Paragraph(_esc(inv_to)   or '—', VAL)]
addr = Table([[from_cell, to_cell]], colWidths=[AVAIL_W * 0.5, AVAIL_W * 0.5])
addr.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'TOP')]))
story.append(addr)
story.append(Spacer(1, 18))

# ── Line items table ──────────────────────────────────────────────────────────
if len(item_rows) > 1:
    story.append(Paragraph('LINE ITEMS', SECT))
    n_cols = max(len(r) for r in item_rows)

    # Proportional widths: Item (wide) | Qty | Unit Price | Amount
    if n_cols == 4:
        col_w = [AVAIL_W * 0.46, AVAIL_W * 0.10, AVAIL_W * 0.22, AVAIL_W * 0.22]
    elif n_cols == 3:
        col_w = [AVAIL_W * 0.55, AVAIL_W * 0.22, AVAIL_W * 0.23]
    elif n_cols == 2:
        col_w = [AVAIL_W * 0.75, AVAIL_W * 0.25]
    else:
        col_w = [AVAIL_W / n_cols] * n_cols

    fmt = []
    for i, row in enumerate(item_rows):
        while len(row) < n_cols:
            row.append('')
        sty = TH if i == 0 else TD
        fmt.append([Paragraph(c, sty) for c in row])

    items_tbl = Table(fmt, colWidths=col_w, repeatRows=1)
    items_tbl.setStyle(TableStyle([
        ('BACKGROUND',     (0, 0),  (-1, 0),  NAVY),
        ('TEXTCOLOR',      (0, 0),  (-1, 0),  WHITE),
        ('GRID',           (0, 0),  (-1, -1), 0.4, BORDER),
        ('ROWBACKGROUNDS', (0, 1),  (-1, -1), [WHITE, ALT]),
        ('VALIGN',         (0, 0),  (-1, -1), 'MIDDLE'),
        # Right-align every column except the first (item description)
        ('ALIGN',          (1, 0),  (-1, -1), 'RIGHT'),
        ('TOPPADDING',     (0, 0),  (-1, -1), 7),
        ('BOTTOMPADDING',  (0, 0),  (-1, -1), 7),
        ('LEFTPADDING',    (0, 0),  (-1, -1), 8),
        ('RIGHTPADDING',   (0, 0),  (-1, -1), 8),
    ]))
    story.append(items_tbl)
    story.append(Spacer(1, 14))

# ── Summary block — right-aligned ─────────────────────────────────────────────
summary_rows = []
if subtotal:
    summary_rows.append([Paragraph('Subtotal', BODY), Paragraph(subtotal, BODY)])
if tax:
    summary_rows.append([Paragraph('Tax', BODY), Paragraph(tax, BODY)])
if total_due:
    summary_rows.append([
        Paragraph('<b>TOTAL DUE</b>', TOT_L),
        Paragraph(f'<b>{total_due}</b>', TOT_V),
    ])

if summary_rows:
    half = AVAIL_W * 0.2
    stbl = Table(summary_rows, colWidths=[half, half], hAlign='RIGHT')
    style_cmds = [
        ('GRID',          (0, 0),  (-1, -2), 0.4, BORDER),
        ('LINEBELOW',     (0, -2), (-1, -2), 0.4, BORDER),
        ('ALIGN',         (1, 0),  (1, -1),  'RIGHT'),
        ('TOPPADDING',    (0, 0),  (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0),  (-1, -1), 6),
        ('LEFTPADDING',   (0, 0),  (-1, -1), 8),
        ('RIGHTPADDING',  (0, 0),  (-1, -1), 8),
    ]
    if total_due:
        last = len(summary_rows) - 1
        style_cmds += [
            ('BACKGROUND', (0, last), (-1, last), colors.HexColor('#fff8ed')),
            ('LINEABOVE',  (0, last), (-1, last), 1.5, AMBER),
            ('BOX',        (0, last), (-1, last), 1.0, AMBER),
        ]
    stbl.setStyle(TableStyle(style_cmds))
    story.append(stbl)
    story.append(Spacer(1, 18))

# ── Payment details ───────────────────────────────────────────────────────────
if bank or iban or bic:
    story.append(HRFlowable(width='100%', thickness=0.5, color=BORDER, spaceAfter=8))
    story.append(Paragraph('PAYMENT DETAILS', SECT))
    pay_rows = []
    for lbl, val in [('Bank', bank), ('IBAN', iban), ('BIC / SWIFT', bic), ('Reference', pay_ref)]:
        if val:
            pay_rows.append([Paragraph(f'<b>{lbl}</b>', BODY), Paragraph(_esc(val), BODY)])
    ptbl = Table(pay_rows, colWidths=[AVAIL_W * 0.22, AVAIL_W * 0.78])
    ptbl.setStyle(TableStyle([
        ('ROWBACKGROUNDS', (0, 0), (-1, -1), [WHITE, ALT]),
        ('TOPPADDING',     (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING',  (0, 0), (-1, -1), 5),
        ('LEFTPADDING',    (0, 0), (-1, -1), 8),
        ('RIGHTPADDING',   (0, 0), (-1, -1), 8),
    ]))
    story.append(ptbl)
    story.append(Spacer(1, 14))

# ── Notes / payment terms ─────────────────────────────────────────────────────
for line in notes_lines:
    story.append(Paragraph(_bold_md(_esc(line)), SMALL))

# ── Render ────────────────────────────────────────────────────────────────────
pdf_path.parent.mkdir(parents=True, exist_ok=True)
page_cb = _make_page_cb(paid=is_paid)
doc = SimpleDocTemplate(
    str(pdf_path), pagesize=A4,
    leftMargin=2 * cm, rightMargin=2 * cm,
    topMargin=2.2 * cm, bottomMargin=2 * cm,
    author='degiabdo — Abderrahim',
    title=f'Invoice {inv_number}',
)
doc.build(story, onFirstPage=page_cb, onLaterPages=page_cb)
print(f'Invoice PDF: {pdf_path}')
