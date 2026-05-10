"""
check_and_gen_pdf.py — check available PDF libs and generate the brief PDF.
"""
import subprocess, sys, os

md_path = r"d:\AI ZARA\ABDO ASSISTENT\.tmp\research-brief-ai-agentic-2026-05-10.md"
pdf_path = r"d:\AI ZARA\ABDO ASSISTENT\.tmp\research-brief-ai-agentic-2026-05-10.pdf"

# Check available libraries
for pkg in ["reportlab", "fpdf2", "fpdf"]:
    try:
        __import__(pkg.replace("2","").replace("-",""))
        print(f"FOUND: {pkg}")
    except ImportError:
        print(f"NOT FOUND: {pkg}")

# Try pip list
result = subprocess.run([sys.executable, "-m", "pip", "list"], capture_output=True, text=True)
for line in result.stdout.splitlines():
    if any(x in line.lower() for x in ["reportlab","fpdf","weasyprint","pdfkit","pypdf"]):
        print(f"PIP: {line}")
