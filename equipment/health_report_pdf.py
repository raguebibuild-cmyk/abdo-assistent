"""
health_report_pdf.py — DEGISaaS branded monthly business health report PDF.
Reads a structured JSON data file produced by the monthly-health-report blueprint
and renders a clean A4 report with KPI summary, client table, pipeline metrics,
and goals & milestones.

Usage:
    python equipment/health_report_pdf.py <data.json> <output.pdf>

Input JSON shape (see blueprints/monthly-health-report.md Step 5 for full spec):
    {
      "date": "YYYY-MM-DD",
      "month_label": "May 2026",
      "clients": [{"name": ..., "status": ..., "open_invoice_amount": ...,
                   "open_quote_amount": ..., "notes": ...}, ...],
      "summary": {"active_clients": 0, "prospects": 0, "closed_clients": 0,
                  "outstanding_invoices_total": 0.0, "open_quotes_total": 0.0},
      "pipeline": {"raw_leads": 0, "qualified_leads": 0, "contacted_leads": 0,
                   "conversion_rate_pct": 0.0},
      "tasks": {"open": 0, "overdue": 0},
      "goals": {"q2_goals": "...", "milestones_hit": [...], "milestones_pending": [...]}
    }
"""
import json
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
    print("Usage: python equipment/health_report_pdf.py <data.json> <output.pdf>")
    sys.exit(1)

json_path = Path(sys.argv[1])
pdf_path  = Path(sys.argv[2])

if not json_path.exists():
    print(f"Error: {json_path} not found")
    sys.exit(1)

data = json.loads(json_path.read_text(encoding='utf-8'))

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
GREEN  = colors.HexColor('#16a34a')
RED    = colors.HexColor('#dc2626')

# ── Styles ────────────────────────────────────────────────────────────────────
_base = getSampleStyleSheet()


def S(name, parent='Normal', **kw):
    return ParagraphStyle(name, parent=_base[parent], **kw)


TITLE  = S('HRTitle',  fontSize=22, textColor=NAVY,   fontName='Helvetica-Bold', leading=26, spaceAfter=4)
SUB    = S('HRSub',    fontSize=10, textColor=MUTED,  fontName='Helvetica', spaceAfter=16)
SECT   = S('HRSect',   fontSize=8,  textColor=INDIGO, fontName='Helvetica-Bold', spaceBefore=18, spaceAfter=6)
BODY   = S('HRBody',   fontSize=9.5,textColor=TEXT,   fontName='Helvetica', leading=14, spaceAfter=3)
SMALL  = S('HRSmall',  fontSize=8.5,textColor=MUTED,  fontName='Helvetica', leading=13, spaceAfter=2)
TH     = S('HRTH',     fontSize=9,  textColor=WHITE,  fontName='Helvetica-Bold')
TD     = S('HRTD',     fontSize=9.5,textColor=TEXT,   fontName='Helvetica', leading=13)
KPI_V  = S('KPIV',     fontSize=20, textColor=NAVY,   fontName='Helvetica-Bold', leading=24, alignment=1)
KPI_L  = S('KPIL',     fontSize=8,  textColor=MUTED,  fontName='Helvetica', leading=11, alignment=1)


def _esc(text) -> str:
    return str(text).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def _fmt_currency(val) -> str:
    try:
        return f"€{float(val):,.2f}"
    except (TypeError, ValueError):
        return str(val)


# ── Extract data ──────────────────────────────────────────────────────────────
month_label = data.get('month_label', data.get('date', ''))
summary     = data.get('summary', {})
pipeline    = data.get('pipeline', {})
tasks       = data.get('tasks', {})
goals       = data.get('goals', {})
clients     = data.get('clients', [])

# ── Build story ───────────────────────────────────────────────────────────────
story = []

# ── Title ─────────────────────────────────────────────────────────────────────
story.append(Spacer(1, 4))
story.append(Paragraph('Business Health Report', TITLE))
story.append(Paragraph(_esc(month_label), SUB))
story.append(HRFlowable(width='100%', thickness=2, color=AMBER, spaceAfter=18))

# ── KPI row ───────────────────────────────────────────────────────────────────
story.append(Paragraph('KEY METRICS', SECT))

kpi_data = [
    (str(summary.get('active_clients', 0)),           'Active Clients'),
    (str(summary.get('prospects', 0)),                 'Open Prospects'),
    (_fmt_currency(summary.get('outstanding_invoices_total', 0)), 'Outstanding'),
    (_fmt_currency(summary.get('open_quotes_total', 0)),          'Open Quotes'),
    (str(tasks.get('overdue', 0)),                    'Overdue Tasks'),
]

kpi_row_vals  = [[Paragraph(_esc(v), KPI_V) for v, _ in kpi_data]]
kpi_row_lbls  = [[Paragraph(_esc(l), KPI_L) for _, l in kpi_data]]
kpi_col_w     = [AVAIL_W / len(kpi_data)] * len(kpi_data)

kpi_tbl = Table(kpi_row_vals + kpi_row_lbls, colWidths=kpi_col_w)
kpi_tbl.setStyle(TableStyle([
    ('ALIGN',          (0, 0), (-1, -1), 'CENTER'),
    ('VALIGN',         (0, 0), (-1, -1), 'MIDDLE'),
    ('BOX',            (0, 0), (-1, -1), 0.5, BORDER),
    ('INNERGRID',      (0, 0), (-1, -1), 0.3, BORDER),
    ('BACKGROUND',     (0, 0), (-1, 0),  colors.HexColor('#f8fafc')),
    ('TOPPADDING',     (0, 0), (-1, 0),  10),
    ('BOTTOMPADDING',  (0, 0), (-1, 0),  4),
    ('TOPPADDING',     (0, 1), (-1, 1),  2),
    ('BOTTOMPADDING',  (0, 1), (-1, 1),  8),
]))
story.append(kpi_tbl)
story.append(Spacer(1, 10))

# ── Client status table ───────────────────────────────────────────────────────
if clients:
    story.append(Paragraph('CLIENT STATUS', SECT))
    header = ['Client', 'Status', 'Open Invoice', 'Open Quote', 'Notes']
    rows   = [[Paragraph(c, TH) for c in header]]

    for cl in clients:
        status_str = cl.get('status', '—')
        status_col = GREEN if status_str == 'Active' else (MUTED if status_str == 'Closed' else AMBER)
        rows.append([
            Paragraph(_esc(cl.get('name', '—')), TD),
            Paragraph(f'<font color="{status_col.hexval() if hasattr(status_col,"hexval") else status_col}">'
                      f'<b>{_esc(status_str)}</b></font>', TD),
            Paragraph(_esc(_fmt_currency(cl.get('open_invoice_amount', 0))
                           if cl.get('open_invoice_amount') else '—'), TD),
            Paragraph(_esc(_fmt_currency(cl.get('open_quote_amount', 0))
                           if cl.get('open_quote_amount') else '—'), TD),
            Paragraph(_esc(cl.get('notes', '') or '—'), TD),
        ])

    col_w = [AVAIL_W * w for w in [0.22, 0.14, 0.15, 0.15, 0.34]]
    cl_tbl = Table(rows, colWidths=col_w, repeatRows=1)
    cl_tbl.setStyle(TableStyle([
        ('BACKGROUND',    (0, 0),  (-1, 0),  NAVY),
        ('GRID',          (0, 0),  (-1, -1), 0.4, BORDER),
        ('ROWBACKGROUNDS',(0, 1),  (-1, -1), [WHITE, ALT]),
        ('VALIGN',        (0, 0),  (-1, -1), 'MIDDLE'),
        ('TOPPADDING',    (0, 0),  (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0),  (-1, -1), 6),
        ('LEFTPADDING',   (0, 0),  (-1, -1), 8),
        ('RIGHTPADDING',  (0, 0),  (-1, -1), 8),
    ]))
    story.append(cl_tbl)
    story.append(Spacer(1, 10))

# ── Pipeline ──────────────────────────────────────────────────────────────────
story.append(Paragraph('LEAD PIPELINE', SECT))

raw_n     = pipeline.get('raw_leads', 0)
qual_n    = pipeline.get('qualified_leads', 0)
cont_n    = pipeline.get('contacted_leads', 0)
conv_rate = pipeline.get('conversion_rate_pct', 0.0)

pipe_rows = [
    [Paragraph('Raw leads',       BODY), Paragraph(_esc(str(raw_n)),  BODY)],
    [Paragraph('Qualified leads', BODY), Paragraph(_esc(str(qual_n)), BODY)],
    [Paragraph('Contacted',       BODY), Paragraph(_esc(str(cont_n)), BODY)],
    [Paragraph('Conversion rate', BODY), Paragraph(_esc(f'{conv_rate:.1f}%'), BODY)],
]
pipe_tbl = Table(pipe_rows, colWidths=[AVAIL_W * 0.4, AVAIL_W * 0.2], hAlign='LEFT')
pipe_tbl.setStyle(TableStyle([
    ('ROWBACKGROUNDS', (0, 0), (-1, -1), [WHITE, ALT]),
    ('GRID',          (0, 0), (-1, -1), 0.4, BORDER),
    ('ALIGN',         (1, 0), (1, -1),  'RIGHT'),
    ('TOPPADDING',    (0, 0), (-1, -1), 5),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ('LEFTPADDING',   (0, 0), (-1, -1), 8),
    ('RIGHTPADDING',  (0, 0), (-1, -1), 8),
]))
story.append(pipe_tbl)
story.append(Spacer(1, 10))

# ── Goals & Milestones ────────────────────────────────────────────────────────
story.append(Paragraph('GOALS & MILESTONES', SECT))

q2_goals = goals.get('q2_goals', '')
if q2_goals:
    story.append(Paragraph(f'<b>Q2 Goals:</b> {_esc(q2_goals)}', BODY))

milestones_hit     = goals.get('milestones_hit', [])
milestones_pending = goals.get('milestones_pending', [])

if milestones_hit:
    story.append(Paragraph('<b>Completed</b>', SMALL))
    for m in milestones_hit:
        story.append(Paragraph(f'<font color="#16a34a">✓</font> {_esc(m)}', BODY))

if milestones_pending:
    story.append(Paragraph('<b>Pending</b>', SMALL))
    for m in milestones_pending:
        story.append(Paragraph(f'○ {_esc(m)}', BODY))

if not milestones_hit and not milestones_pending:
    story.append(Paragraph('No milestones defined — update intel/wins.md.', SMALL))

story.append(Spacer(1, 6))
story.append(HRFlowable(width='100%', thickness=0.5, color=BORDER, spaceAfter=6))
story.append(Paragraph(f'Generated {_esc(data.get("date", ""))} — degiabdo internal use only.', SMALL))

# ── Render ────────────────────────────────────────────────────────────────────
pdf_path.parent.mkdir(parents=True, exist_ok=True)
doc = SimpleDocTemplate(
    str(pdf_path), pagesize=A4,
    leftMargin=2 * cm, rightMargin=2 * cm,
    topMargin=2.2 * cm, bottomMargin=2 * cm,
    author='degiabdo — Abderrahim',
    title=f'Business Health Report — {month_label}',
)
doc.build(story, onFirstPage=_brand_cb, onLaterPages=_brand_cb)
print(f'Health report PDF: {pdf_path}')
