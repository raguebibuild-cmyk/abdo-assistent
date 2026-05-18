from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
import os, base64

output_path = r'D:\AI ZARA\ABDO ASSISTENT\.tmp\Project_Audit_2026-05-07.pdf'

doc = SimpleDocTemplate(output_path, pagesize=A4,
    leftMargin=2*cm, rightMargin=2*cm, topMargin=2*cm, bottomMargin=2*cm)

styles = getSampleStyleSheet()

title_style = ParagraphStyle('Title2', parent=styles['Normal'],
    fontSize=18, fontName='Helvetica-Bold', spaceAfter=4, textColor=colors.HexColor('#1a1a1a'))
subtitle_style = ParagraphStyle('Subtitle2', parent=styles['Normal'],
    fontSize=9, fontName='Helvetica', spaceAfter=16, textColor=colors.HexColor('#666666'))
section_style = ParagraphStyle('Section2', parent=styles['Normal'],
    fontSize=12, fontName='Helvetica-Bold', spaceBefore=14, spaceAfter=8,
    textColor=colors.HexColor('#1a1a1a'))
bullet_style = ParagraphStyle('Bullet2', parent=styles['Normal'],
    fontSize=9, fontName='Helvetica', spaceAfter=5, leading=13,
    leftIndent=12, textColor=colors.HexColor('#1a1a1a'))

story = []

story.append(Paragraph('Daily Project Audit', title_style))
story.append(Paragraph('2026-05-07  |  abdo-assistent repository  |  8 days to launch (2026-05-15)', subtitle_style))
story.append(HRFlowable(width='100%', thickness=1, color=colors.HexColor('#cccccc'), spaceAfter=12))

story.append(Paragraph('Executive Summary', section_style))
bullets = [
    '<b>CRITICAL</b> — 7 revenue-critical replies are 2+ days overdue (due 2026-05-05): 5 inbound leads + 2 CRM quotes. Launch is 8 days away. These must go out today.',
    '<b>HIGH</b> — CLAUDE.md is stale: lists 2 blueprints when 6 exist, and claims Google Calendar is connected when it is not.',
    '<b>HIGH</b> — Two task trackers (tasks.md vs state.md) are out of sync. Startup protocol reads tasks.md last updated 2026-04-22, missing all current live tasks.',
]
for b in bullets:
    story.append(Paragraph(f'• {b}', bullet_style))

story.append(Spacer(1, 10))
story.append(Paragraph('Issues — Sorted by Priority', section_style))

table_data = [
    ['#', 'Issue', 'Type', 'Priority', 'Suggested Fix'],
    ['1', '7 overdue lead replies\nlaboratoiremvcd, biovagoabdorag, Sami/Cedar\nWealth, Karim/DeltaLogix, Reem/Hala Ventures,\nConstruction Casablanca, Nadia/Kontrast', 'Missing action', 'CRITICAL', 'Run Client Communication\nHandler for each.\nDraft and review all 7 today.'],
    ['2', '2 audit deliveries overdue\nNajim Travel and Cotton & Stitch\nmarked [OVERDUE] in state.md', 'Missing action', 'CRITICAL', 'Confirm status.\nCommunicate proactively\nwith clients today.'],
    ['3', 'live/tasks.md stale\nNot updated since 2026-04-22.\nstate.md has 15+ live items\nnot read on startup.', 'Broken dependency', 'HIGH', 'Sync tasks.md with state.md\nor update CLAUDE.md to\nread state.md on startup.'],
    ['4', 'CLAUDE.md Blueprints table\nlists 2 of 6. Missing:\nclient-proposal-document,\nlead-update-followup,\nmonday-morning-pipeline,\nprioritisation', 'Stale data', 'HIGH', 'Add 4 missing blueprints\nto CLAUDE.md table.'],
    ['5', '.tmp/ directory missing\nmonday-morning-pipeline writes\noutput here. Workflow fails\nat Step 2.', 'Broken dependency', 'HIGH', 'mkdir .tmp\necho "*" > .tmp/.gitignore'],
    ['6', 'Google Calendar conflict\nCLAUDE.md: Connected.\nstack.md: Aspirational.', 'Conflict', 'HIGH', 'Correct CLAUDE.md\nto match stack.md.'],
    ['7', '.env file missing\nAll credentials should live\nin .env. File does not exist.', 'Missing element', 'HIGH', 'Create .env placeholder.\nAdd to .gitignore.'],
    ['8', 'decisions/ledger.md empty\n3+ weeks of decisions\nnot recorded.', 'Missing element', 'MEDIUM', 'Backfill 5-6 key\ndecisions from memory.'],
    ['9', 'focus.md priority 3 stale\n"Working out pricing" listed.\nPricing locked 2026-05-03.', 'Stale data', 'MEDIUM', 'Update to current\nlaunch sprint focus.'],
    ['10', 'wins.md Q2 goals undefined\nNo targets set.\nLaunch 8 days away.', 'Incomplete', 'MEDIUM', 'Define Q2 goals\nin next session.'],
]

priority_colors = {
    'CRITICAL': colors.HexColor('#fdecea'),
    'HIGH': colors.HexColor('#fff3e0'),
    'MEDIUM': colors.HexColor('#e3f2fd'),
}
priority_text_colors = {
    'CRITICAL': colors.HexColor('#c0392b'),
    'HIGH': colors.HexColor('#e67e22'),
    'MEDIUM': colors.HexColor('#2980b9'),
}

col_widths = [0.8*cm, 5.4*cm, 3*cm, 2.2*cm, 4.6*cm]

table_style_cmds = [
    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
    ('FONTSIZE', (0,0), (-1,-1), 8),
    ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#2c3e50')),
    ('TEXTCOLOR', (0,0), (-1,0), colors.white),
    ('ALIGN', (0,0), (-1,-1), 'LEFT'),
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f9f9f9')]),
    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#dddddd')),
    ('TOPPADDING', (0,0), (-1,-1), 5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ('LEFTPADDING', (0,0), (-1,-1), 5),
    ('RIGHTPADDING', (0,0), (-1,-1), 5),
]

priority_col = 3
for row_idx, row in enumerate(table_data[1:], start=1):
    p = row[priority_col]
    if p in priority_colors:
        table_style_cmds.append(('BACKGROUND', (priority_col, row_idx), (priority_col, row_idx), priority_colors[p]))
        table_style_cmds.append(('TEXTCOLOR', (priority_col, row_idx), (priority_col, row_idx), priority_text_colors[p]))
        table_style_cmds.append(('FONTNAME', (priority_col, row_idx), (priority_col, row_idx), 'Helvetica-Bold'))

t = Table(table_data, colWidths=col_widths, repeatRows=1)
t.setStyle(TableStyle(table_style_cmds))
story.append(t)

story.append(Spacer(1, 14))
story.append(Paragraph('Top 3 Actions Today', section_style))
actions = [
    '<b>1. Send 7 overdue lead replies</b> — Run Client Communication Handler for each. Draft and review all 7 today.',
    '<b>2. Sync task trackers</b> — Update tasks.md to match state.md, or update CLAUDE.md startup protocol to read state.md.',
    '<b>3. Fix CLAUDE.md</b> — Update Blueprints table (4 missing), correct Google Calendar status, add .env note.',
]
for a in actions:
    story.append(Paragraph(f'• {a}', bullet_style))

story.append(Spacer(1, 16))
story.append(HRFlowable(width='100%', thickness=0.5, color=colors.HexColor('#cccccc'), spaceAfter=6))
story.append(Paragraph('Generated automatically by Daily Project Audit routine — degiabdo command centre', subtitle_style))

doc.build(story)
print('PDF created:', output_path)
print('Size:', os.path.getsize(output_path), 'bytes')

with open(output_path, 'rb') as f:
    b64 = base64.b64encode(f.read()).decode('utf-8')
print('Base64 length:', len(b64))

with open(r'D:\AI ZARA\ABDO ASSISTENT\.tmp\audit_pdf_fresh_b64.txt', 'w') as f:
    f.write(b64)
print('Base64 saved.')
