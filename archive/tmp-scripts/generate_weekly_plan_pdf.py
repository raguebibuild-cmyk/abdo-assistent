from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT

OUTPUT = r"d:\AI ZARA\ABDO ASSISTENT\blueprints\weekly-plan-2026-W19.pdf"

# ── Colours ──────────────────────────────────────────────────────────────────
NAVY     = colors.HexColor("#1A2340")
SLATE    = colors.HexColor("#2D3E5A")
TEAL     = colors.HexColor("#1B7F79")
AMBER    = colors.HexColor("#E07B39")
RED      = colors.HexColor("#C0392B")
GOLD     = colors.HexColor("#D4A843")
LIGHT_BG = colors.HexColor("#F4F6F9")
MID_BG   = colors.HexColor("#E8EDF4")
WHITE    = colors.white
DARK_TXT = colors.HexColor("#1C2333")
BODY_TXT = colors.HexColor("#2C3E50")
MUTED    = colors.HexColor("#6B7A8D")

# ── Document ─────────────────────────────────────────────────────────────────
doc = SimpleDocTemplate(
    OUTPUT,
    pagesize=A4,
    leftMargin=18*mm,
    rightMargin=18*mm,
    topMargin=16*mm,
    bottomMargin=16*mm,
)

W = A4[0] - 36*mm   # usable width

# ── Styles ───────────────────────────────────────────────────────────────────
base = getSampleStyleSheet()

def sty(name, **kw):
    s = ParagraphStyle(name, **kw)
    return s

DOC_TITLE = sty("DocTitle",
    fontName="Helvetica-Bold", fontSize=20, textColor=WHITE,
    leading=24, alignment=TA_LEFT)

DOC_META = sty("DocMeta",
    fontName="Helvetica", fontSize=8.5, textColor=colors.HexColor("#BCC8D8"),
    leading=13, alignment=TA_LEFT)

SECTION = sty("Section",
    fontName="Helvetica-Bold", fontSize=11.5, textColor=WHITE,
    leading=16, alignment=TA_LEFT)

SUB_SECTION = sty("SubSection",
    fontName="Helvetica-Bold", fontSize=10, textColor=NAVY,
    leading=14, spaceBefore=6)

BODY = sty("Body",
    fontName="Helvetica", fontSize=9, textColor=BODY_TXT,
    leading=13, spaceBefore=2)

BODY_BOLD = sty("BodyBold",
    fontName="Helvetica-Bold", fontSize=9, textColor=DARK_TXT,
    leading=13)

CALL_TITLE = sty("CallTitle",
    fontName="Helvetica-Bold", fontSize=10, textColor=NAVY,
    leading=14, spaceBefore=6)

CALL_LABEL = sty("CallLabel",
    fontName="Helvetica-Bold", fontSize=8.5, textColor=TEAL,
    leading=12)

CALL_BODY = sty("CallBody",
    fontName="Helvetica", fontSize=8.5, textColor=BODY_TXT,
    leading=12)

BULLET = sty("Bullet",
    fontName="Helvetica", fontSize=9, textColor=BODY_TXT,
    leading=13, leftIndent=12, firstLineIndent=-8)

BADGE_GREEN  = sty("BadgeGreen",  fontName="Helvetica-Bold", fontSize=8, textColor=WHITE, leading=10, alignment=TA_CENTER)
BADGE_AMBER  = sty("BadgeAmber",  fontName="Helvetica-Bold", fontSize=8, textColor=WHITE, leading=10, alignment=TA_CENTER)
BADGE_RED    = sty("BadgeRed",    fontName="Helvetica-Bold", fontSize=8, textColor=WHITE, leading=10, alignment=TA_CENTER)

FOOTER_STY = sty("Footer",
    fontName="Helvetica", fontSize=7.5, textColor=MUTED,
    leading=10, alignment=TA_CENTER)

# ── Helpers ───────────────────────────────────────────────────────────────────

def spacer(h=4):
    return Spacer(1, h*mm)

def rule(color=MID_BG, thickness=0.5):
    return HRFlowable(width="100%", thickness=thickness, color=color, spaceAfter=3, spaceBefore=3)

def section_header(title, bg=NAVY):
    data = [[Paragraph(title, SECTION)]]
    t = Table(data, colWidths=[W])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg),
        ("TOPPADDING",    (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING",   (0, 0), (-1, -1), 10),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 10),
        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [bg]),
    ]))
    return t

def sub_header(title):
    return Paragraph(title, SUB_SECTION)

def data_table(headers, rows, col_widths, stripe=True, header_bg=SLATE, flag_col=None):
    """Generic styled table."""
    header_cells = [Paragraph(h, sty(f"TH{i}", fontName="Helvetica-Bold",
        fontSize=8, textColor=WHITE, leading=11)) for i, h in enumerate(headers)]
    table_data = [header_cells]
    for row in rows:
        cells = [Paragraph(str(c), sty(f"TD{j}", fontName="Helvetica",
            fontSize=8, textColor=BODY_TXT, leading=11)) for j, c in enumerate(row)]
        table_data.append(cells)

    t = Table(table_data, colWidths=col_widths)
    style_cmds = [
        ("BACKGROUND",    (0, 0), (-1, 0),  header_bg),
        ("TOPPADDING",    (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING",   (0, 0), (-1, -1), 7),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 7),
        ("GRID",          (0, 0), (-1, -1), 0.4, colors.HexColor("#D5DCE8")),
        ("VALIGN",        (0, 0), (-1, -1), "TOP"),
    ]
    if stripe:
        for i in range(1, len(table_data)):
            bg = LIGHT_BG if i % 2 == 1 else WHITE
            style_cmds.append(("BACKGROUND", (0, i), (-1, i), bg))
    t.setStyle(TableStyle(style_cmds))
    return t

def call_block(time_name, topic, context, prep, goal, day_color=TEAL):
    inner = [
        [Paragraph(f"{time_name}", CALL_TITLE),
         Paragraph(f"<i>{topic}</i>", sty("Topic", fontName="Helvetica-Oblique",
             fontSize=9, textColor=MUTED, leading=13))],
        [Paragraph("Context:", CALL_LABEL), Paragraph(context, CALL_BODY)],
        [Paragraph("Prep:", CALL_LABEL),    Paragraph(prep, CALL_BODY)],
        [Paragraph("Goal:", CALL_LABEL),    Paragraph(goal, CALL_BODY)],
    ]
    col_w = [22*mm, W - 22*mm - 4*mm]
    t = Table(inner, colWidths=col_w)
    t.setStyle(TableStyle([
        ("SPAN",          (0, 0), (1, 0)),
        ("BACKGROUND",    (0, 0), (-1, 0),  colors.HexColor("#EDF2F9")),
        ("BACKGROUND",    (0, 1), (-1, -1), WHITE),
        ("TOPPADDING",    (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING",   (0, 0), (-1, -1), 8),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 8),
        ("BOX",           (0, 0), (-1, -1), 0.8, day_color),
        ("LINEBELOW",     (0, 0), (-1, 0),  0.5, colors.HexColor("#D5DCE8")),
        ("VALIGN",        (0, 0), (-1, -1), "TOP"),
    ]))
    return KeepTogether([t, spacer(2)])

# ── Cover / Title Block ───────────────────────────────────────────────────────

def cover_block():
    data = [[
        Paragraph("Weekly Plan — W19 2026", DOC_TITLE),
        Paragraph("May 4 – 10", sty("WkRange",
            fontName="Helvetica-Bold", fontSize=14, textColor=colors.HexColor("#8BAAC8"),
            leading=20, alignment=TA_RIGHT)),
    ]]
    t = Table(data, colWidths=[W * 0.65, W * 0.35])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, -1), NAVY),
        ("TOPPADDING",    (0, 0), (-1, -1), 12),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING",   (0, 0), (-1, -1), 12),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 12),
        ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
    ]))
    meta_row = [[Paragraph(
        "Sources: Gmail · Google Calendar · Tasks List · RevOps pipeline framework  |  "
        "Generated: 2026-05-04  |  11 days to degiabdo launch (May 15)",
        DOC_META)]]
    meta = Table(meta_row, colWidths=[W])
    meta.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, -1), SLATE),
        ("TOPPADDING",    (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING",   (0, 0), (-1, -1), 12),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 12),
    ]))
    return [t, meta, spacer(5)]

# ── At a Glance ───────────────────────────────────────────────────────────────

def at_a_glance():
    items = [
        ("6", "Calls this week"),
        ("2", "Overdue items"),
        ("7", "Urgent replies"),
        ("5", "Follow-ups open"),
        ("11", "Days to launch"),
    ]
    cells = []
    for val, label in items:
        inner = Table([
            [Paragraph(val, sty(f"V{val}", fontName="Helvetica-Bold",
                fontSize=22, textColor=NAVY, leading=26, alignment=TA_CENTER))],
            [Paragraph(label, sty(f"L{label}", fontName="Helvetica",
                fontSize=8, textColor=MUTED, leading=11, alignment=TA_CENTER))],
        ], colWidths=[(W / 5) - 3*mm])
        inner.setStyle(TableStyle([
            ("BACKGROUND",    (0, 0), (-1, -1), LIGHT_BG),
            ("TOPPADDING",    (0, 0), (-1, -1), 8),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ("BOX",           (0, 0), (-1, -1), 0.6, MID_BG),
            ("ALIGN",         (0, 0), (-1, -1), "CENTER"),
        ]))
        cells.append(inner)

    row = Table([cells], colWidths=[(W / 5)] * 5)
    row.setStyle(TableStyle([
        ("TOPPADDING",    (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
        ("LEFTPADDING",   (0, 0), (-1, -1), 1.5),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 1.5),
    ]))
    return [section_header("AT A GLANCE"), spacer(3), row, spacer(6)]

# ── Build Story ───────────────────────────────────────────────────────────────

story = []
story += cover_block()
story += at_a_glance()

# ── TIER 1 — Overdue ──────────────────────────────────────────────────────────
story.append(section_header("TIER 1 — OVERDUE  (Do these first)", bg=RED))
story.append(spacer(3))
story.append(Paragraph(
    "These are already late. Every additional day erodes client trust.",
    BODY))
story.append(spacer(2))
story.append(data_table(
    ["#", "Task", "Client", "Was Due", "Action"],
    [
        ["1", "Deliver audit", "Cotton & Stitch (Reema Saleh)", "2026-04-30",
         "Complete and send today. $950."],
        ["2", "Deliver audit", "Najim Travel (Layla Al Mahri)", "2026-05-02",
         "Complete and send today. $950."],
    ],
    col_widths=[8*mm, 28*mm, 55*mm, 28*mm, W - 119*mm],
    header_bg=RED,
))
story.append(spacer(6))

# ── TIER 2 — Urgent Replies ───────────────────────────────────────────────────
story.append(section_header("TIER 2 — URGENT REPLIES  (Due by end of May 5)", bg=AMBER))
story.append(spacer(3))
story.append(Paragraph(
    "All five inbound leads landed May 3. Speed-to-lead window is closing — "
    "reply before each call so they arrive warm.",
    BODY))
story.append(spacer(2))
story.append(data_table(
    ["#", "Who", "Subject", "Call Booked", "Key Context"],
    [
        ["1", "Nadia — Kontrast Personalberatung",
         "LinkedIn content automation upsell",
         "TODAY 14:00",
         "Existing client. Market research → draft posts → approval queue. Reply before call."],
        ["2", "Sami — Cedar Wealth Advisory",
         "Re: Picking this back up",
         "Wed May 6, 15:00",
         "Managing Partner. Back after partner transition. Client comms for top 50 HNW clients. USD 6.5k quoted."],
        ["3", "Karim — DeltaLogix",
         "Re: AAA Workflow Audit proposal",
         "Wed May 6, 11:00",
         "Aligned on scope. Wants audit doc format + 30-day roadmap walkthrough. Finance flagged NET 30 vs 50/50."],
        ["4", "Reem — Hala Ventures",
         "Outbound automation — intro call?",
         "Thu May 7, 08:00",
         "B2B SaaS Saudi F&amp;B. SDR drowning. Registry scraping + LinkedIn enrichment + first-touch personalisation."],
        ["5", "Construction firm, Casablanca",
         "Intro from Hicham — quote automation",
         "Fri May 8, 09:00",
         "Referral from Sahel Cafe Group. ~40 people. Custom quotes take 2-3 days — losing deals to faster competitors."],
        ["6", "CRM quote — laboratoiremvcd",
         "Re: Request for Price Quote",
         "—",
         "Follow-up sent May 3. Awaiting decision on Growth Package (€1,200 setup + €250/mo)."],
        ["7", "CRM quote — biovagoabdorag",
         "Re: price request",
         "—",
         "Follow-up sent May 3. Same package. Awaiting decision."],
    ],
    col_widths=[8*mm, 42*mm, 48*mm, 28*mm, W - 126*mm],
    header_bg=colors.HexColor("#B8601E"),
))
story.append(spacer(6))

# ── PIPELINE INTELLIGENCE ─────────────────────────────────────────────────────
story.append(section_header("PIPELINE INTELLIGENCE", bg=TEAL))
story.append(spacer(3))

story.append(sub_header("Pipeline Stage Map"))
story.append(spacer(2))
story.append(data_table(
    ["Deal", "Stage", "Value", "Close Prob", "Exp. Value", "Risk"],
    [
        ["DeltaLogix (Karim)",    "Negotiation",       "~$4k est",   "65%", "~$2,600", "Call Wed — remove 2 blockers"],
        ["Cedar Wealth (Sami)",   "Proposal",          "$6,500",     "45%", "~$2,925", "Ghost risk — quiet 2 months"],
        ["Foster & Marsh Legal",  "Proposal",          "$12,000",    "20%", "~$2,400", "STALE — 2 follow-ups, no reply"],
        ["Zayd Property",         "Proposal",          "$6,500",     "30%", "~$1,950", "STALE — 11 days, no follow-up"],
        ["Kontrast upsell (Nadia)","Customer Expansion","~$2.5k est","70%", "~$1,750", "Call today — highest trust"],
        ["Tahseen Tutoring",      "Discovery",         "$4,900",     "35%", "~$1,715", "Confirm discovery happened"],
        ["Noor Beauty Group",     "Discovery",         "~$4k est",   "40%", "~$1,600", "Call Tue"],
        ["Hala Ventures (Reem)",  "Qualified",         "~$5k est",   "20%", "~$1,000", "Call Thu"],
        ["Construction CBL",      "Qualified",         "~$3.5k est", "25%", "~$875",   "Call Fri"],
        ["Dahab Wellness",        "Discovery",         "$2,500",     "30%", "~$750",   "Confirm discovery happened"],
        ["CRM quotes x2",         "Proposal",          "€1,200 ea", "25% ea", "~$600 ea", "Follow-up sent, clock running"],
        ["Nour Aesthetics Clinic","Lead",              "TBD",        "15%", "~$450",   "No contact yet"],
    ],
    col_widths=[42*mm, 28*mm, 22*mm, 20*mm, 22*mm, W - 134*mm],
    header_bg=TEAL,
))
story.append(spacer(2))
story.append(Paragraph(
    "<b>Total pipeline expected value this week: ~$18,600</b>",
    sty("EV", fontName="Helvetica-Bold", fontSize=9, textColor=TEAL, leading=13)))
story.append(spacer(5))

story.append(sub_header("Priority by Expected Value — Where to Focus Energy"))
story.append(spacer(2))
priorities = [
    ("<b>Cedar Wealth $6.5k</b> — Highest realistic expected value this week. Re-anchor the quote firmly on Wednesday.", TEAL),
    ("<b>DeltaLogix ~$4k</b> — Closest to the line. Wednesday call is the close attempt. Remove the two blockers (doc format + payment terms) and get a signature.", TEAL),
    ("<b>Zayd Property $6.5k</b> — STALE. No follow-up in 11 days on a cold quote = near-dead without action. Contact Maya today or tomorrow.", AMBER),
    ("<b>Foster & Marsh $12k</b> — Highest nominal value but lowest probability. Two follow-ups unanswered. Third touch this week — if no reply, mark low-probability and move on.", AMBER),
    ("<b>Kontrast upsell</b> — Existing client. Easiest close. Don’t underprice it — this is proven trust, not a new sale.", TEAL),
]
for i, (text, accent) in enumerate(priorities, 1):
    row_data = [[
        Paragraph(str(i), sty(f"Num{i}", fontName="Helvetica-Bold",
            fontSize=11, textColor=WHITE, leading=14, alignment=TA_CENTER)),
        Paragraph(text, sty(f"Pri{i}", fontName="Helvetica",
            fontSize=8.5, textColor=BODY_TXT, leading=12)),
    ]]
    t = Table(row_data, colWidths=[10*mm, W - 10*mm])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (0, 0), accent),
        ("BACKGROUND",    (1, 0), (1, 0), LIGHT_BG),
        ("TOPPADDING",    (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING",   (0, 0), (-1, -1), 7),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 7),
        ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
        ("LINEBELOW",     (0, 0), (-1, -1), 0.4, colors.HexColor("#D5DCE8")),
    ]))
    story.append(t)
story.append(spacer(5))

story.append(sub_header("Stale Deal Alerts"))
story.append(spacer(2))
story.append(Paragraph(
    "Two deals are at serious risk of expiring before May 15.",
    BODY))
story.append(spacer(2))
story.append(data_table(
    ["Deal", "Days Since Last Touch", "Status", "Action Needed"],
    [
        ["Zayd Property (Maya Al Hashemi)", "11 days",
         "Quote sent, no follow-up ever",
         "Send follow-up today — most urgent rescue"],
        ["Foster & Marsh Legal (James Foster)", "5 days",
         "Second follow-up sent, no reply",
         "Third and final touch by Wednesday"],
    ],
    col_widths=[52*mm, 35*mm, 50*mm, W - 137*mm],
    header_bg=RED,
))
story.append(spacer(2))
story.append(Paragraph(
    "RevOps benchmark: deals stale for 14+ days without contact have <b>&lt;10% close probability</b>. "
    "You have days, not weeks.",
    BODY))
story.append(spacer(5))

story.append(sub_header("Velocity Check — Can You Close Before May 15?"))
story.append(spacer(2))

vc_data = [
    [
        Paragraph("Closable before May 15", sty("VCH1", fontName="Helvetica-Bold",
            fontSize=9, textColor=WHITE, leading=12)),
        Paragraph("Future pipeline (too early)", sty("VCH2", fontName="Helvetica-Bold",
            fontSize=9, textColor=WHITE, leading=12)),
    ],
    [
        Paragraph(
            "DeltaLogix (Negotiation — call Wed)<br/>"
            "Cedar Wealth (Proposal — call Wed)<br/>"
            "Kontrast upsell (Expansion — call today)<br/>"
            "Zayd Property (Proposal — if rescued)<br/>"
            "CRM quotes x2 (Proposal — awaiting reply)<br/>"
            "Foster &amp; Marsh (possible if responds)",
            sty("VCB1", fontName="Helvetica", fontSize=8.5, textColor=BODY_TXT, leading=13)),
        Paragraph(
            "Noor Beauty (Discovery — call Tue)<br/>"
            "Hala Ventures (Qualified — call Thu)<br/>"
            "Construction CBL (Qualified — call Fri)<br/>"
            "Nour Aesthetics (Lead)<br/>"
            "Marble &amp; Co, Mohammed Tech (Lead)",
            sty("VCB2", fontName="Helvetica", fontSize=8.5, textColor=BODY_TXT, leading=13)),
    ],
]
vc_table = Table(vc_data, colWidths=[W / 2, W / 2])
vc_table.setStyle(TableStyle([
    ("BACKGROUND",    (0, 0), (0, 0), TEAL),
    ("BACKGROUND",    (1, 0), (1, 0), SLATE),
    ("BACKGROUND",    (0, 1), (0, 1), LIGHT_BG),
    ("BACKGROUND",    (1, 1), (1, 1), WHITE),
    ("TOPPADDING",    (0, 0), (-1, -1), 8),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ("LEFTPADDING",   (0, 0), (-1, -1), 10),
    ("RIGHTPADDING",  (0, 0), (-1, -1), 10),
    ("GRID",          (0, 0), (-1, -1), 0.5, colors.HexColor("#D5DCE8")),
    ("VALIGN",        (0, 0), (-1, -1), "TOP"),
]))
story.append(vc_table)
story.append(spacer(2))
story.append(Paragraph(
    "<b>Speed-to-lead:</b> The 5 new inbounds arrived May 3. Research shows contact within 5 minutes is "
    "21× more likely to qualify. You’re now at ~24 hours. Reply today — don’t lose this momentum.",
    sty("SpeedNote", fontName="Helvetica-Oblique", fontSize=8.5, textColor=AMBER,
        leading=12, borderColor=AMBER, borderWidth=0.5, borderPadding=6,
        backColor=colors.HexColor("#FEF6EC"))))
story.append(spacer(8))

# ── TIER 3 — Call Schedule ────────────────────────────────────────────────────
story.append(section_header("TIER 3 — CALL SCHEDULE AND PREP", bg=SLATE))
story.append(spacer(4))

day_calls = [
    ("Monday May 4", [
        ("14:00 — Nadia, Kontrast Personalberatung", "LinkedIn automation upsell",
         "Existing client. Onboarding automation already delivered. Now wants a LinkedIn content pipeline.",
         "Have a rough scope ready — market research inputs → AI drafting in their voice → review/approval queue. Come with a price range.",
         "Agree scope and pricing. If confirmed, book a follow-up to define inputs.",
         TEAL),
    ]),
    ("Tuesday May 5", [
        ("08:00 — R.Abdo, Noor Beauty Group", "Onboarding automation — discovery",
         "Inbound lead. 14-person beauty retail group, Dubai, 4 locations. Manual onboarding ~8h/week.",
         "Standard discovery questions: current process, volume, biggest pain point, who owns it. Bring the onboarding automation case study angle.",
         "Qualify, identify scope, agree next step.",
         colors.HexColor("#2980B9")),
    ]),
    ("Wednesday May 6", [
        ("11:00 — Karim, DeltaLogix", "AAA proposal walkthrough (Google Meet)",
         "COO. Scope agreed. Sticking points: audit doc format, 30-day implementation roadmap, and payment terms.",
         "Have a sample audit doc structure ready. Position on payment terms (suggest 50/50 — avoid NET 30 at this stage). Map out a 30-day roadmap outline.",
         "Remove the last objections. Get the signature or a clear blocker.",
         AMBER),
        ("15:00 — Sami, Cedar Wealth Advisory", "Client comms re-kickoff",
         "Managing Partner. Was in progress, went quiet March due to partner transition. Back now.",
         "Recap the original scope: top 50 HNW client draft replies, pulled from client history + tone, reviewable before send.",
         "Re-confirm scope and timeline. Re-anchor the USD 6.5k quote.",
         AMBER),
    ]),
    ("Thursday May 7", [
        ("08:00 — Reem, Hala Ventures", "Outbound automation — intro call",
         "Head of Growth, B2B SaaS, Saudi F&amp;B. SDR is doing manual sourcing and enrichment.",
         "Have the outbound automation workflow overview ready. Lead with the SDR time saving angle. Know your pricing range for this scope.",
         "Qualify need and budget. Agree on a proposal call or send a scoped proposal by end of week.",
         colors.HexColor("#6C3483")),
    ]),
    ("Friday May 8", [
        ("09:00 — Construction firm, Casablanca", "Quote automation — intro call",
         "Referred by Hicham at Sahel Cafe Group. ~40 people. Every quote is custom — 2–3 day turnaround — losing deals to faster competitors.",
         "The Sahel Cafe reference is a strong trust anchor — lead with it. Focus questions on: quote types, volume per month, what makes them custom, who signs off.",
         "Understand the problem, qualify fit, agree next step.",
         TEAL),
    ]),
]

for day, calls in day_calls:
    day_label = Table([[Paragraph(day, sty("DayLabel",
        fontName="Helvetica-Bold", fontSize=9.5, textColor=NAVY, leading=13))]],
        colWidths=[W])
    day_label.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, -1), MID_BG),
        ("TOPPADDING",    (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING",   (0, 0), (-1, -1), 10),
    ]))
    story.append(day_label)
    story.append(spacer(2))
    for time_name, topic, context, prep, goal, accent in calls:
        story.append(call_block(time_name, topic, context, prep, goal, accent))

story.append(spacer(4))

# ── TIER 4 — Follow-Ups ───────────────────────────────────────────────────────
story.append(section_header("TIER 4 — PIPELINE FOLLOW-UPS  (By May 7)", bg=NAVY))
story.append(spacer(3))
story.append(data_table(
    ["#", "Who", "Deal", "Due", "Status"],
    [
        ["1", "Foster & Marsh Legal (James Foster)",
         "$12k — document review automation", "May 7",
         "Second follow-up sent April 29. Third touch needed."],
        ["2", "Zayd Property (Maya Al Hashemi)",
         "$6.5k — real estate automation", "May 7",
         "Quote sent April 23. First follow-up overdue."],
        ["3", "Tahseen Tutoring (Hala Mansour)",
         "$4.9k — FAQ + scheduling agent", "May 6",
         "Discovery was scheduled April 30 — confirm completed or reschedule."],
        ["4", "Dahab Wellness (Yara Al Otaibi)",
         "$2.5k — wellness automation", "May 6",
         "Discovery was scheduled May 1 — confirm completed or reschedule."],
        ["5", "Nour Aesthetics Clinic (Dr. Reem Hamdan)",
         "TBD — lead qualification bot", "May 7",
         "Send discovery questions. Medical aesthetics Dubai."],
    ],
    col_widths=[8*mm, 50*mm, 50*mm, 16*mm, W - 124*mm],
))
story.append(spacer(6))

# ── TIER 5 — Launch Countdown ─────────────────────────────────────────────────
story.append(section_header("TIER 5 — MAY 15 LAUNCH COUNTDOWN  (11 days)", bg=GOLD))
story.append(spacer(3))
story.append(data_table(
    ["Item", "Priority", "Notes"],
    [
        ["Build invoice template", "Must-have",
         "Needed before first invoice is sent. Nothing goes out without it."],
        ["Build audit template", "Must-have",
         "Must be client-customised — not generic. Two overdue audits make this urgent."],
        ["Launch website / landing page", "Must-have",
         "degiabdo official opening. 11 days."],
        ["Close first paying client", "Core goal",
         "DeltaLogix (Wednesday call) is the most likely candidate this week."],
        ["Define Q2 goals collaboratively", "Medium",
         "No deadline yet — schedule a session before May 10."],
    ],
    col_widths=[60*mm, 28*mm, W - 88*mm],
    header_bg=colors.HexColor("#A07820"),
))
story.append(spacer(6))

# ── WEEK SUMMARY ──────────────────────────────────────────────────────────────
story.append(section_header("WEEK SUMMARY", bg=NAVY))
story.append(spacer(3))

days = [
    ("Monday", "today",
     "Reply to all 7 urgents now — the 21× speed-to-lead window is closing. "
     "Follow up Zayd Property (stale rescue). Prep and run Nadia call at 14:00. "
     "Deliver Cotton & Stitch audit."),
    ("Tuesday", "May 5",
     "Deliver Najim Travel audit. Run Noor Beauty discovery at 08:00. "
     "Follow up Foster & Marsh (third touch). Start invoice template."),
    ("Wednesday", "May 6",
     "Two close attempts: DeltaLogix at 11:00 (remove the two blockers, get a decision), "
     "Cedar Wealth at 15:00 (re-anchor $6.5k). Highest expected-value day of the week."),
    ("Thursday", "May 7",
     "Run Hala Ventures intro at 08:00. Confirm Tahseen and Dahab discovery status. "
     "Send Nour Aesthetics discovery questions. Start audit template."),
    ("Friday", "May 8",
     "Run Casablanca construction intro at 09:00. Review pipeline — mark stale deals as lost "
     "or last-touch. Update Tasks List. Push website work."),
]

for day, sub, text in days:
    row = [[
        Paragraph(f"<b>{day}</b><br/><font size=7 color='#8899AA'>{sub}</font>",
            sty(f"DS{day}", fontName="Helvetica-Bold", fontSize=9, textColor=NAVY,
                leading=13, alignment=TA_CENTER)),
        Paragraph(text, BODY),
    ]]
    t = Table(row, colWidths=[22*mm, W - 22*mm])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (0, 0), LIGHT_BG),
        ("BACKGROUND",    (1, 0), (1, 0), WHITE),
        ("TOPPADDING",    (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("LEFTPADDING",   (0, 0), (-1, -1), 8),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 8),
        ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
        ("LINEBELOW",     (0, 0), (-1, -1), 0.4, colors.HexColor("#D5DCE8")),
        ("BOX",           (0, 0), (-1, -1), 0.4, colors.HexColor("#D5DCE8")),
    ]))
    story.append(t)

story.append(spacer(5))
story.append(Paragraph(
    "<b>Close target this week:</b> DeltaLogix or Cedar Wealth (or both). "
    "Either one = first paying client before May 15.",
    sty("CloseTarget", fontName="Helvetica-Bold", fontSize=9.5, textColor=TEAL,
        leading=14, borderColor=TEAL, borderWidth=1, borderPadding=8,
        backColor=colors.HexColor("#EAF7F6"))))
story.append(spacer(6))

# ── Footer row ────────────────────────────────────────────────────────────────
story.append(rule(color=MID_BG, thickness=0.8))
story.append(Paragraph(
    "Next step: Update live/state.md at session end. "
    "Move this file to archive/ when the week closes.  |  "
    "degiabdo — Agentic Workflows Consultancy  |  © 2026",
    FOOTER_STY))

# ── Build ─────────────────────────────────────────────────────────────────────
doc.build(story)
print(f"PDF saved to: {OUTPUT}")
