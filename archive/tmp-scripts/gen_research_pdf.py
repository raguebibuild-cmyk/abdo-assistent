from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY

OUTPUT = ".tmp/research-ai-agentic-2026-05-10.pdf"

NAVY   = colors.HexColor("#0D1B2A")
ACCENT = colors.HexColor("#1A73E8")
LIGHT  = colors.HexColor("#F4F6FA")
MID    = colors.HexColor("#E8ECF4")
DARK   = colors.HexColor("#333333")
MUTED  = colors.HexColor("#666666")
WHITE  = colors.white

doc = SimpleDocTemplate(
    OUTPUT, pagesize=A4,
    leftMargin=2.2*cm, rightMargin=2.2*cm,
    topMargin=2.2*cm,  bottomMargin=2.2*cm,
    title="AI Agentic Trends - May 2026",
    author="Research Subagent - degiabdo",
)

styles = getSampleStyleSheet()

s_cover_title = ParagraphStyle("cover_title", fontSize=26, leading=32,
    textColor=WHITE, fontName="Helvetica-Bold", alignment=TA_LEFT, spaceAfter=6)
s_cover_sub = ParagraphStyle("cover_sub", fontSize=12, leading=16,
    textColor=colors.HexColor("#C8D8F0"), fontName="Helvetica", alignment=TA_LEFT)
s_section_label = ParagraphStyle("section_label", fontSize=8, leading=10,
    textColor=ACCENT, fontName="Helvetica-Bold", spaceBefore=18, spaceAfter=2)
s_h2 = ParagraphStyle("h2", fontSize=13, leading=18, textColor=NAVY,
    fontName="Helvetica-Bold", spaceBefore=4, spaceAfter=4)
s_body = ParagraphStyle("body", fontSize=10, leading=15, textColor=DARK,
    fontName="Helvetica", spaceAfter=6, alignment=TA_JUSTIFY)
s_why = ParagraphStyle("why", fontSize=9.5, leading=14, textColor=DARK,
    fontName="Helvetica-Oblique", spaceAfter=4, leftIndent=12, alignment=TA_JUSTIFY)
s_source_label = ParagraphStyle("source_label", fontSize=8.5, leading=12,
    textColor=MUTED, fontName="Helvetica", spaceAfter=2, leftIndent=12)
s_footer = ParagraphStyle("footer", fontSize=8, leading=10, textColor=MUTED,
    fontName="Helvetica", alignment=TA_CENTER)
s_exec_body = ParagraphStyle("exec_body", fontSize=10.5, leading=16, textColor=DARK,
    fontName="Helvetica", spaceAfter=4, alignment=TA_JUSTIFY)
s_number = ParagraphStyle("number", fontSize=28, leading=30, textColor=MID,
    fontName="Helvetica-Bold")
s_src = ParagraphStyle("src", fontSize=8.5, leading=12, textColor=DARK, fontName="Helvetica")
s_src_url = ParagraphStyle("src_url", fontSize=8, leading=11, textColor=MUTED, fontName="Helvetica")

story = []

# Cover
cover_inner = Table([
    [Paragraph("AI AGENTIC TRENDS", s_cover_title)],
    [Paragraph("Top 5 Findings for SME &amp; MENA Markets", s_cover_sub)],
    [Spacer(1, 10)],
    [Paragraph("Research Subagent  |  degiabdo  |  10 May 2026", s_cover_sub)],
], colWidths=[14*cm], style=TableStyle([
    ("BOTTOMPADDING", (0,0), (-1,-1), 4),
    ("TOPPADDING",    (0,0), (-1,-1), 4),
]))
cover = Table([[cover_inner]], colWidths=[doc.width])
cover.setStyle(TableStyle([
    ("BACKGROUND",    (0,0), (-1,-1), NAVY),
    ("TOPPADDING",    (0,0), (-1,-1), 24),
    ("BOTTOMPADDING", (0,0), (-1,-1), 24),
    ("LEFTPADDING",   (0,0), (-1,-1), 28),
    ("RIGHTPADDING",  (0,0), (-1,-1), 28),
]))
story.append(cover)
story.append(Spacer(1, 20))

# Executive Summary
story.append(Paragraph("EXECUTIVE SUMMARY", s_section_label))
story.append(HRFlowable(width="100%", thickness=1, color=ACCENT, spaceAfter=8))
story.append(Paragraph(
    "2026 is the year agentic AI crossed from experiment to infrastructure. Active production "
    "deployments jumped from <b>11% to 54%</b> of organisations in under two years, driven by "
    "standardised protocols (MCP), multi-agent architectures, and proven ROI in customer service, "
    "finance, and document operations. The critical shift: the barrier is no longer the technology "
    "-- it is integration, governance, and cost control. That gap is where the opportunity sits.",
    s_exec_body))
story.append(Spacer(1, 16))

findings = [
    {
        "n": "01",
        "title": "Adoption Is Accelerating -- The Window Is Closing Fast",
        "body": (
            "Active AI agent deployment jumped from <b>11% to 54%</b> of organisations in under "
            "two years (KPMG via Ampcome, Q1 2026). Gartner recorded a <b>1,445% surge</b> in "
            "multi-agent system inquiries between Q1 2024 and Q2 2025. The technology is no longer "
            "experimental -- it is becoming table stakes, with 40% of enterprise applications "
            "projected to include task-specific agents by end of 2026."
        ),
        "why": (
            "<b>Why it matters:</b> SMEs who delay past 2026 will be competing against businesses "
            "with 12-24 months of compounding operational advantage. In MENA markets where digital "
            "transformation cycles run 12-18 months behind Western markets, the urgency is higher, "
            "not lower -- the adoption wave arrives compressed."
        ),
        "sources": "KPMG Q1 2026 via Ampcome  |  Gartner Multi-Agent Systems Report  |  Gartner Enterprise Apps Forecast",
    },
    {
        "n": "02",
        "title": "The Deployment Gap Is the Real Opportunity for Consultancies",
        "body": (
            "<b>79% of enterprises claim AI agent adoption, but only 11-14% have reached "
            "production.</b> The primary blockers are integration with existing systems (cited by "
            "46%), data infrastructure, and governance -- not the AI technology itself. This gap "
            "between intent and execution is structural and persistent, with Gartner warning 40% "
            "of agentic projects face cancellation by 2027."
        ),
        "why": (
            "<b>Why it matters:</b> This is the exact gap an agentic workflows consultancy fills. "
            "MENA SMEs face the same blockers but with fewer internal technical resources to resolve "
            "them -- making the consultancy value proposition sharper, not weaker, in this market."
        ),
        "sources": "Svitla Agentic AI Market Trends (Apr 2026)  |  Gartner Hype Cycle for Agentic AI",
    },
    {
        "n": "03",
        "title": "Measurable ROI Arrives Within 90 Days -- In the Right Use Cases",
        "body": (
            "Production deployments are delivering concrete results: <b>84% customer service "
            "resolution rates</b>, 90% faster document processing, inventory losses cut from "
            "$5.4M to $1.6M per quarter. 25%+ of organisations see measurable ROI within 90 days. "
            "The clearest wins cluster around customer service, finance operations, document "
            "processing, and HR scheduling."
        ),
        "why": (
            "<b>Why it matters:</b> SMEs need short payback cycles. The 90-day ROI window -- tied "
            "to specific, contained use cases -- is exactly the entry point to propose. In MENA, "
            "where ROI justification is often relationship-dependent, concrete numbers from live "
            "deployments close the credibility gap faster than any pitch deck."
        ),
        "sources": "Ampcome Mid-Year Report (Apr 2026)  |  Svitla Market Trends  |  TechAhead Industry Report",
    },
    {
        "n": "04",
        "title": "MCP Is Now the Infrastructure Standard -- Not a Choice",
        "body": (
            "Model Context Protocol (MCP) crossed <b>97 million installs</b> in March 2026 and "
            "is now the default mechanism for agents to connect to tools, APIs, and data sources. "
            "Every major AI provider ships MCP-compatible tooling. The infrastructure layer has "
            "standardised faster than most analysts expected -- building on proprietary connectors "
            "today is technical debt from day one."
        ),
        "why": (
            "<b>Why it matters:</b> Any agentic workflow built today should be MCP-native. For a "
            "MENA consultancy selling agentic workflows, MCP fluency is now a baseline competency "
            "requirement -- but it remains rare enough in the region that it signals genuine "
            "expertise to clients."
        ),
        "sources": "Medium / Mohit Aggarwal (2026)  |  Anthropic MCP Install Data  |  Gartner Enterprise Apps Forecast",
    },
    {
        "n": "05",
        "title": "Cost and Governance Are Now Production-Level Requirements",
        "body": (
            "<b>40% of agentic AI projects risk cancellation by 2027</b> -- not due to technology "
            "failure, but due to cost escalation and governance gaps (Svitla, 2026). Uncontrolled "
            "token spend has become a recognised operational risk. Governance-first deployments "
            "consistently scale the fastest, while ungoverned deployments stall or get pulled back."
        ),
        "why": (
            "<b>Why it matters:</b> SMEs cannot absorb runaway AI costs or compliance failures. "
            "Selling a workflow without cost controls is selling incomplete work -- and creates "
            "churn risk. In MENA, where regulatory environments across Saudi Arabia, UAE, and Egypt "
            "are tightening around data and AI use, building compliance in from day one is also a "
            "client protection play."
        ),
        "sources": "Svitla Agentic AI Market Trends (Apr 2026)  |  Portal26 / Yahoo Finance (2026)  |  Ampcome Mid-Year Report",
    },
]

story.append(Paragraph("TOP 5 FINDINGS", s_section_label))
story.append(HRFlowable(width="100%", thickness=1, color=ACCENT, spaceAfter=10))

for f in findings:
    inner = Table([
        [Paragraph(f["title"], s_h2)],
        [Paragraph(f["body"],  s_body)],
        [Paragraph(f["why"],   s_why)],
        [Paragraph(f["sources"], s_source_label)],
    ], colWidths=[13.0*cm], style=TableStyle([
        ("TOPPADDING",    (0,0), (-1,-1), 2),
        ("BOTTOMPADDING", (0,0), (-1,-1), 2),
        ("LEFTPADDING",   (0,0), (-1,-1), 0),
        ("RIGHTPADDING",  (0,0), (-1,-1), 0),
    ]))
    card = Table([[Paragraph(f["n"], s_number), inner]],
                 colWidths=[1.6*cm, 13.4*cm])
    card.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), LIGHT),
        ("TOPPADDING",    (0,0), (-1,-1), 14),
        ("BOTTOMPADDING", (0,0), (-1,-1), 14),
        ("LEFTPADDING",   (0,0), (-1,-1), 14),
        ("RIGHTPADDING",  (0,0), (-1,-1), 14),
        ("VALIGN",        (0,0), (-1,-1), "TOP"),
    ]))
    story.append(KeepTogether([card, Spacer(1, 10)]))

# Sources
story.append(Spacer(1, 8))
story.append(Paragraph("SOURCES", s_section_label))
story.append(HRFlowable(width="100%", thickness=1, color=ACCENT, spaceAfter=8))

sources = [
    ("Agentic AI Market Trends 2025-2026: 5 Shifts That Matter",       "svitla.com"),
    ("Gartner: 40% of Enterprise Apps Will Feature AI Agents by 2026", "gartner.com"),
    ("Enterprise AI Agents 2026: Mid-Year Report on What's Working",   "ampcome.com"),
    ("Agentic AI in 2026: Autonomous Agents Crossed the Chasm",        "medium.com/@mohit15856"),
    ("NVIDIA and ServiceNow Partner on Autonomous AI Agents",          "blogs.nvidia.com"),
    ("Portal26 Launches AI Agentic Cost Controls",                     "yahoo.com/finance"),
    ("Top Use Cases of Agentic AI in 2026 Across Industries",          "techaheadcorp.com"),
    ("AI Agent Adoption 2026: What the Data Shows",                    "joget.com"),
]

src_rows = [[Paragraph(f"<b>{i+1}.</b>  {t}", s_src), Paragraph(u, s_src_url)]
            for i, (t, u) in enumerate(sources)]
src_table = Table(src_rows, colWidths=[11.5*cm, 3.5*cm])
src_table.setStyle(TableStyle([
    ("TOPPADDING",    (0,0), (-1,-1), 4),
    ("BOTTOMPADDING", (0,0), (-1,-1), 4),
    ("LINEBELOW",     (0,0), (-1,-1), 0.3, MID),
    ("VALIGN",        (0,0), (-1,-1), "TOP"),
]))
story.append(src_table)

# Footer
story.append(Spacer(1, 20))
story.append(HRFlowable(width="100%", thickness=0.5, color=MID, spaceAfter=6))
story.append(Paragraph(
    "Research Subagent  |  degiabdo  |  10 May 2026  |  raguebi.mba@gmail.com",
    s_footer))

doc.build(story)
print("PDF generated:", OUTPUT)
