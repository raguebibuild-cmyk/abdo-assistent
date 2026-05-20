"""
DEGISaaS brand constants and PDF page callback.
Import in any PDF generation script to apply consistent branding across all client-facing documents.

Logo: save your logo file at assets/brand/logo.png — it will appear automatically in all PDF headers.
For best results on the dark navy header, use a PNG with transparent background.
"""
from pathlib import Path

_DIR = Path(__file__).parent
LOGO_PATH = _DIR.parent / 'assets' / 'brand' / 'logo.png'
BRAND = 'DEGISaaS'
TAGLINE = 'Built to Scale'

# Brand hex strings — pass directly to reportlab HexColor() or fpdf set_text_color()
C_NAVY   = '#012240'   # primary dark — headers, table headers, nav bar
C_AMBER  = '#e89820'   # primary accent — "SaaS" colour, dividers, highlights
C_INDIGO = '#4f4cee'   # secondary accent — "DEGI" colour, H3, labels, links
C_TEXT   = '#1e293b'   # body text
C_MUTED  = '#64748b'   # footer, captions
C_BORDER = '#e2e8f0'   # table borders, subtle rules
C_ALTROW = '#f8fafc'   # table alternating row background
C_CODEBG = '#f1f5f9'   # code block background
C_CODEFG = '#374151'   # code block text
C_BQBG   = '#fff8ed'   # blockquote background (warm amber tint)

# FPDF2 RGB equivalents (pre-computed for convenience)
RGB_NAVY   = (1,   34,  64)    # #012240
RGB_AMBER  = (232, 152, 32)    # #e89820
RGB_INDIGO = (79,  76,  238)   # #4f4cee
RGB_MUTED  = (100, 116, 139)   # #64748b


def page_callback(canvas, doc):
    """
    Reportlab page callback: draws a branded header bar and footer on every page.
    Pass to SimpleDocTemplate.build() as onFirstPage and onLaterPages.

    Header: navy bar (#012240) + amber accent strip (#e89820), with logo (if found) or brand name.
    Footer: horizontal rule + brand name left, page number right.
    """
    from reportlab.lib import colors
    from reportlab.lib.units import cm
    from reportlab.lib.pagesizes import A4

    NAVY    = colors.HexColor(C_NAVY)
    AMBER   = colors.HexColor(C_AMBER)
    WHITE   = colors.white
    INDIGO  = colors.HexColor(C_INDIGO)
    MUTED   = colors.HexColor(C_MUTED)
    BORDER  = colors.HexColor(C_BORDER)

    PAGE_W, PAGE_H = A4
    BAR_H   = 1.6 * cm
    STRIP_H = 0.15 * cm

    canvas.saveState()

    # Header: white bar
    canvas.setFillColor(WHITE)
    canvas.rect(0, PAGE_H - BAR_H, PAGE_W, BAR_H, fill=1, stroke=0)

    # Header: amber accent strip immediately below the bar
    canvas.setFillColor(AMBER)
    canvas.rect(0, PAGE_H - BAR_H - STRIP_H, PAGE_W, STRIP_H, fill=1, stroke=0)

    # Header content: logo image or brand name text
    logo = LOGO_PATH
    if logo.exists():
        max_h = BAR_H * 0.65
        max_w = max_h * 4.5  # bounding box — reportlab preserves aspect ratio within these bounds
        canvas.drawImage(
            str(logo),
            PAGE_W - max_w - 0.8 * cm,
            PAGE_H - BAR_H + (BAR_H - max_h) / 2,
            width=max_w,
            height=max_h,
            preserveAspectRatio=True,
            mask='auto',
        )
    else:
        # Fallback: render "DEGI" in indigo + "SaaS" in amber to read on white bar
        canvas.setFont('Helvetica-Bold', 13)
        right_edge = PAGE_W - 0.8 * cm
        text_y = PAGE_H - BAR_H * 0.58
        saas_w = canvas.stringWidth('SaaS', 'Helvetica-Bold', 13)
        canvas.setFillColor(AMBER)
        canvas.drawRightString(right_edge, text_y, 'SaaS')
        canvas.setFillColor(INDIGO)
        canvas.drawRightString(right_edge - saas_w, text_y, 'DEGI')

    # Footer: horizontal rule
    footer_rule_y = 0.9 * cm
    canvas.setStrokeColor(BORDER)
    canvas.setLineWidth(0.5)
    canvas.line(2 * cm, footer_rule_y, PAGE_W - 2 * cm, footer_rule_y)

    # Footer: brand name left, page number right
    canvas.setFillColor(MUTED)
    canvas.setFont('Helvetica-Oblique', 7.5)
    footer_text_y = footer_rule_y - 0.3 * cm
    canvas.drawString(2 * cm, footer_text_y, BRAND)
    canvas.drawRightString(PAGE_W - 2 * cm, footer_text_y, f'Page {canvas.getPageNumber()}')

    canvas.restoreState()
