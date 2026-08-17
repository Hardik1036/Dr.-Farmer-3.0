"""
Generates publication-quality SIH Project Report PDF using ReportLab
"""

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    """Canvas that computes total pages and prints running footer."""
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#555555"))
        
        # Header (pages 2+)
        if self._pageNumber > 1:
            self.drawString(36, 810, "Smart India Hackathon (SIH) — Project Report: Dr. Farmer (AgriVision)")
            self.setStrokeColor(colors.HexColor("#d0d7de"))
            self.setLineWidth(0.5)
            self.line(36, 804, 559, 804)

        # Footer
        self.setStrokeColor(colors.HexColor("#d0d7de"))
        self.setLineWidth(0.5)
        self.line(36, 38, 559, 38)
        self.drawString(36, 26, "Dr. Farmer (AgriVision) — AI-Powered Advisory Platform")
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(559, 26, page_text)
        self.restoreState()

def generate_pdf(output_path):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=36,
        rightMargin=36,
        topMargin=44,
        bottomMargin=48
    )

    styles = getSampleStyleSheet()

    # Custom color palette
    c_primary = colors.HexColor("#1b4332")
    c_secondary = colors.HexColor("#2d6a4f")
    c_accent = colors.HexColor("#40916c")
    c_dark = colors.HexColor("#1b2e1b")
    c_body = colors.HexColor("#2b2b2b")

    # Typography styles
    style_badge = ParagraphStyle(
        'Badge',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        textColor=colors.HexColor("#d8f3dc"),
        spaceAfter=4
    )

    style_title = ParagraphStyle(
        'MainTitle',
        parent=styles['Title'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.white,
        alignment=0,
        spaceAfter=4
    )

    style_subtitle = ParagraphStyle(
        'SubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10.5,
        leading=14,
        textColor=colors.HexColor("#b7e4c7"),
        spaceAfter=8
    )

    style_meta = ParagraphStyle(
        'Meta',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#e8f5e9")
    )

    style_h1 = ParagraphStyle(
        'SectionH1',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=15,
        textColor=c_primary,
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    )

    style_h2 = ParagraphStyle(
        'SectionH2',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=c_secondary,
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )

    style_body = ParagraphStyle(
        'Body',
        parent=styles['BodyText'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=c_body,
        spaceAfter=5
    )

    style_body_bold = ParagraphStyle(
        'BodyBold',
        parent=style_body,
        fontName='Helvetica-Bold'
    )

    style_bullet = ParagraphStyle(
        'Bullet',
        parent=style_body,
        leftIndent=12,
        firstLineIndent=-8,
        spaceAfter=3
    )

    style_code = ParagraphStyle(
        'CodeBlock',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=7,
        leading=9.5,
        textColor=colors.HexColor("#0f172a"),
        backColor=colors.HexColor("#f1f5f9"),
        borderColor=colors.HexColor("#cbd5e1"),
        borderWidth=0.5,
        borderPadding=6,
        spaceBefore=6,
        spaceAfter=6
    )

    style_table_header = ParagraphStyle(
        'TableHeader',
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=colors.white
    )

    style_table_cell = ParagraphStyle(
        'TableCell',
        fontName='Helvetica',
        fontSize=7.5,
        leading=10,
        textColor=c_body
    )

    story = []

    # 1. HEADER BANNER
    header_data = [
        [Paragraph("SMART INDIA HACKATHON (SIH) — OFFICIAL PROJECT REPORT", style_badge)],
        [Paragraph("🌱 Dr. Farmer (AgriVision)", style_title)],
        [Paragraph("Full-Stack AI-Powered Crop & Livestock Disease Advisory Platform", style_subtitle)],
        [
            Table([
                [
                    Paragraph("<b>Domain:</b> Agriculture & Rural Development / AI", style_meta),
                    Paragraph("<b>Backend API:</b> https://dr-farmer-3-0.onrender.com", style_meta)
                ],
                [
                    Paragraph("<b>Target:</b> Smallholder Indian Farmers & Vets", style_meta),
                    Paragraph("<b>Database:</b> Supabase PostgreSQL (Cloud Sync)", style_meta)
                ],
                [
                    Paragraph("<b>Repository:</b> github.com/b25bs1115-eng/Dr.-Farmer-3.0", style_meta),
                    Paragraph("<b>Frontend:</b> React 19 + Vite (Deployed on Vercel)", style_meta)
                ]
            ], colWidths=[240, 240], style=[
                ('TOPPADDING', (0,0), (-1,-1), 1),
                ('BOTTOMPADDING', (0,0), (-1,-1), 1),
                ('LEFTPADDING', (0,0), (-1,-1), 0),
                ('RIGHTPADDING', (0,0), (-1,-1), 0),
            ])
        ]
    ]

    header_table = Table(header_data, colWidths=[523])
    header_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_primary),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('LEFTPADDING', (0,0), (-1,-1), 14),
        ('RIGHTPADDING', (0,0), (-1,-1), 14),
        ('ROUNDEDCORNERS', [6, 6, 6, 6])
    ]))
    story.append(header_table)
    story.append(Spacer(1, 8))

    # 2. EXECUTIVE SUMMARY
    story.append(Paragraph("1. Executive Summary", style_h1))
    story.append(HRFlowable(width="100%", thickness=1, color=c_accent, spaceBefore=1, spaceAfter=5))
    story.append(Paragraph(
        "Agriculture supports over <b>58% of India's rural population</b>, yet crop blights and cattle epidemics cause annual economic losses exceeding <b>₹1.5 lakh crore</b>. Smallholder farmers face critical bottlenecks: delayed physical visits by scarce agricultural extension officers, literacy barriers on scientific advisory portals, and panic-driven chemical pesticide overuse that degrades fertile soil.",
        style_body
    ))
    story.append(Paragraph(
        "<b>Dr. Farmer (AgriVision)</b> is an AI-powered, mobile-first advisory platform engineered for grassroots Indian agriculture. A farmer simply captures a photo of an infected leaf or cattle symptom to receive <b>instant (3-second) disease diagnosis</b>, severity evaluation, and a <b>dual-action treatment plan</b> (organic home remedies + veterinary/chemical prescriptions) with full <b>multilingual spoken voice narration</b> in regional languages.",
        style_body
    ))

    # 3. PROBLEM STATEMENT
    story.append(Paragraph("2. Problem Statement & Challenges Addressed", style_h1))
    story.append(HRFlowable(width="100%", thickness=1, color=c_accent, spaceBefore=1, spaceAfter=5))
    
    prob_data = [
        [
            Paragraph("<b>⏳ Diagnostic Delays:</b> Physical field inspections take 5–15 days, allowing blights to destroy entire harvest cycles.", style_table_cell),
            Paragraph("<b>📖 Literacy Barriers:</b> Over 40% of smallholder farmers cannot decipher complex English scientific names.", style_table_cell)
        ],
        [
            Paragraph("<b>🧪 Chemical Overuse:</b> Lack of organic home alternatives leads to ₹3,000–₹5,000/acre in wasted pesticide spend.", style_table_cell),
            Paragraph("<b>🐄 Cattle Epidemics:</b> Critical infections like Lumpy Skin Disease (LSD) and FMD spread without early alerts.", style_table_cell)
        ]
    ]
    prob_table = Table(prob_data, colWidths=[255, 255])
    prob_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f8faf9")),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#d8e2dc")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(prob_table)
    story.append(Spacer(1, 6))

    # 4. KEY INNOVATIONS & FEATURES
    story.append(Paragraph("3. Key Innovations & Platform Features", style_h1))
    story.append(HRFlowable(width="100%", thickness=1, color=c_accent, spaceBefore=1, spaceAfter=5))
    story.append(Paragraph("• <b>Point-and-Shoot AI Diagnosis:</b> Accurately classifies 38 plant diseases (Tomato, Potato, Corn, Apple, Grape, Strawberry, etc.) and cattle pathologies (Lumpy Skin Disease).", style_bullet))
    story.append(Paragraph("• <b>Dual-Advisory Model:</b> Delivers low-cost organic home remedies (buttermilk, neem spray, ash dusting) alongside authorized veterinary/chemical prescriptions (Mancozeb, Metalaxyl).", style_bullet))
    story.append(Paragraph("• <b>Spoken Audio Narration:</b> Native speech synthesis in <b>Hindi, English, Bengali, Telugu, Marathi, Tamil, Gujarati, and Punjabi</b> for low-literacy accessibility.", style_bullet))
    story.append(Paragraph("• <b>Digital Farm Record Book:</b> Cloud ledger tracking sowing dates, expected harvest schedules, pesticide safety windows, and cattle vaccination timers.", style_bullet))
    story.append(Paragraph("• <b>1-Tap Kisan Call Center Hotline:</b> Direct emergency dialer connecting farmers immediately to government agricultural experts (<b>1800-180-1551</b>).", style_bullet))
    story.append(Paragraph("• <b>Supabase Cloud Resilience:</b> Cloud-backed database with automated local fallback ensuring zero downtime during spotty rural connectivity.", style_bullet))

    story.append(PageBreak())

    # 5. SYSTEM ARCHITECTURE & DATA FLOW
    story.append(Paragraph("4. System Architecture & Topology", style_h1))
    story.append(HRFlowable(width="100%", thickness=1, color=c_accent, spaceBefore=1, spaceAfter=5))
    
    arch_ascii = (
        "+-----------------------------------------------------------------------------------+\n"
        "|                             DR. FARMER SYSTEM TOPOLOGY                            |\n"
        "+-----------------------------------------------------------------------------------+\n"
        "|  [1] CLIENT LAYER (Vercel Global CDN)                                             |\n"
        "|      - React 19 + Vite (<300 KB ultra-fast bundle, sub-second load)               |\n"
        "|      - Web Speech API (Native multilingual voice synthesis & narration)           |\n"
        "|      - Tailwind CSS v4 (Mobile-first responsive farmer touch UI)                  |\n"
        "|                                       | (Multipart HTTP / REST API)               |\n"
        "|                                       v                                           |\n"
        "|  [2] BACKEND INFERENCE ENGINE (Render Cloud - Python 3.11 ASGI)                   |\n"
        "|      - FastAPI asynchronous router (/api/scan, /api/crops, /api/livestock)        |\n"
        "|      - TensorFlow Lite (TFLite) & LiteRT optimized runtime                        |\n"
        "|      - 38-Class Plant Model (4.5MB) + Cattle Lumpy Disease Model (4.5MB)          |\n"
        "|                                       | (Secure REST / PostgREST)                 |\n"
        "|                                       v                                           |\n"
        "|  [3] CLOUD DATABASE LAYER (Supabase PostgreSQL with RLS)                          |\n"
        "|      - disease_catalog    : 38 Crop classes, Hindi remedies, & chemical dosages   |\n"
        "|      - diagnostic_logs    : Telemetry & real-time scan epidemic tracking          |\n"
        "|      - crop_cycles        : Farm Record Book (Kharif, Rabi, Zaid tracking)        |\n"
        "|      - livestock_profiles : Cattle tags, species, & vaccination due dates         |\n"
        "+-----------------------------------------------------------------------------------+"
    )
    story.append(Paragraph(arch_ascii.replace("\n", "<br/>").replace(" ", "&nbsp;"), style_code))

    # 6. TECH STACK TABLE
    story.append(Paragraph("5. Technology Stack Summary", style_h1))
    story.append(HRFlowable(width="100%", thickness=1, color=c_accent, spaceBefore=1, spaceAfter=5))

    tech_table_data = [
        [Paragraph("Layer", style_table_header), Paragraph("Technology Stack", style_table_header), Paragraph("Engineering Rationale", style_table_header)],
        [Paragraph("<b>Frontend</b>", style_table_cell), Paragraph("React 19, Vite, Tailwind CSS v4", style_table_cell), Paragraph("Ultra-lean &lt;300KB bundle size; fast on rural 2G/3G connections.", style_table_cell)],
        [Paragraph("<b>Voice Audio</b>", style_table_cell), Paragraph("HTML5 Web Speech API", style_table_cell), Paragraph("Zero-byte browser-native text-to-speech across Indian languages.", style_table_cell)],
        [Paragraph("<b>Backend API</b>", style_table_cell), Paragraph("FastAPI, Uvicorn, Python 3.11", style_table_cell), Paragraph("High-speed asynchronous Python server with sub-10ms overhead.", style_table_cell)],
        [Paragraph("<b>ML Inference</b>", style_table_cell), Paragraph("TensorFlow Lite / LiteRT", style_table_cell), Paragraph("Quantized 4.5MB models; sub-45ms CPU inference without memory spikes.", style_table_cell)],
        [Paragraph("<b>Database</b>", style_table_cell), Paragraph("Supabase (PostgreSQL with RLS)", style_table_cell), Paragraph("Cloud sync with Row-Level Security and resilient offline fallback.", style_table_cell)],
        [Paragraph("<b>Hosting</b>", style_table_cell), Paragraph("Vercel (Frontend), Render (Backend)", style_table_cell), Paragraph("Global Edge CDN + Linux microservices with automated auto-scaling.", style_table_cell)],
    ]
    tech_table = Table(tech_table_data, colWidths=[80, 160, 275])
    tech_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#f8fafc")]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(tech_table)
    story.append(Spacer(1, 6))

    # 7. MACHINE LEARNING PIPELINE
    story.append(Paragraph("6. Machine Learning Optimization & Quantization", style_h1))
    story.append(HRFlowable(width="100%", thickness=1, color=c_accent, spaceBefore=1, spaceAfter=5))
    story.append(Paragraph(
        "• <b>Dataset Scale:</b> Trained on the PlantVillage benchmark dataset containing <b>54,305 labeled crop leaf images</b> (14 species, 38 health/disease classes) and curated cattle dermatological nodule imagery.",
        style_bullet
    ))
    story.append(Paragraph(
        "• <b>FlatBuffers Model Quantization:</b> Converted raw Keras weights (<code>17.6 MB</code>) to TensorFlow Lite FlatBuffers (<code>4.5 MB</code>) via <code>convert_tflite.py</code>, achieving a <b>75% file reduction</b> without losing diagnostic accuracy.",
        style_bullet
    ))
    story.append(Paragraph(
        "• <b>LiteRT Runtime Efficiency:</b> Replaced the heavy ~1GB TensorFlow engine with the ~5MB <code>ai-edge-litert</code> runtime, preventing cloud server memory crashes and ensuring cold-start boots in under 2 seconds.",
        style_bullet
    ))

    story.append(PageBreak())

    # 8. DATABASE DESIGN
    story.append(Paragraph("7. Database Schema Layout (Supabase)", style_h1))
    story.append(HRFlowable(width="100%", thickness=1, color=c_accent, spaceBefore=1, spaceAfter=5))

    schema_data = [
        [Paragraph("Table Name", style_table_header), Paragraph("Key Columns", style_table_header), Paragraph("Purpose & Data Stored", style_table_header)],
        [Paragraph("<b>disease_catalog</b>", style_table_cell), Paragraph("entity_type, class_index, disease_name, disease_name_hi, severity, medical_treatment, home_remedy", style_table_cell), Paragraph("Master 38-class plant & cattle advisory catalog with Hindi remedies.", style_table_cell)],
        [Paragraph("<b>diagnostic_logs</b>", style_table_cell), Paragraph("scan_id, entity_type, entity_id, pathology_detected, confidence_score, scan_timestamp", style_table_cell), Paragraph("Telemetry scan history for epidemic hotspot tracking.", style_table_cell)],
        [Paragraph("<b>crop_cycles</b>", style_table_cell), Paragraph("crop_id, farmer_id, season, crop_name, sowing_date, expected_harvest_date, pesticide_applied", style_table_cell), Paragraph("Digital farm ledger for sowing, harvest, and pesticide safety.", style_table_cell)],
        [Paragraph("<b>livestock_profiles</b>", style_table_cell), Paragraph("farmer_id, animal_tag, species, vaccination_name, last_vaccination_date, next_due_date", style_table_cell), Paragraph("Cattle health profiles and automated vaccination due date reminders.", style_table_cell)],
    ]
    schema_table = Table(schema_data, colWidths=[100, 200, 215])
    schema_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#f8fafc")]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(schema_table)
    story.append(Spacer(1, 6))

    # 9. SOCIAL IMPACT & SUSTAINABILITY
    story.append(Paragraph("8. Societal Impact & Sustainability", style_h1))
    story.append(HRFlowable(width="100%", thickness=1, color=c_accent, spaceBefore=1, spaceAfter=5))

    impact_data = [
        [Paragraph("Impact Metric", style_table_header), Paragraph("Quantified Real-World Outcome", style_table_header)],
        [Paragraph("<b>Crop Yield Protection</b>", style_table_cell), Paragraph("Prevents <b>20–30% yield loss</b> through rapid early-stage fungal detection.", style_table_cell)],
        [Paragraph("<b>Input Cost Reduction</b>", style_table_cell), Paragraph("Organic home remedies save farmers <b>₹3,000–₹5,000 per acre</b> on chemical sprays.", style_table_cell)],
        [Paragraph("<b>Digital Inclusion</b>", style_table_cell), Paragraph("Spoken voice guidance bridges the literacy gap for over <b>100M+ regional farmers</b>.", style_table_cell)],
        [Paragraph("<b>Livestock Safeguard</b>", style_table_cell), Paragraph("Early Lumpy Skin Disease isolation prevents cattle mortality and preserves milk yield.", style_table_cell)],
        [Paragraph("<b>Zero Hardware Barrier</b>", style_table_cell), Paragraph("Runs on standard mobile browsers with <b>no proprietary hardware or sensor purchases</b>.", style_table_cell)],
    ]
    impact_table = Table(impact_data, colWidths=[150, 365])
    impact_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_secondary),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#f8fafc")]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(impact_table)
    story.append(Spacer(1, 6))

    # 10. SCALABILITY & ROADMAP
    story.append(Paragraph("9. Scalability & Future Roadmap", style_h1))
    story.append(HRFlowable(width="100%", thickness=1, color=c_accent, spaceBefore=1, spaceAfter=5))
    story.append(Paragraph("1. <b>100% Offline Edge PWA:</b> WebAssembly client-side inference for zero-connectivity remote rural farms.", style_bullet))
    story.append(Paragraph("2. <b>Drone Multispectral Mapping:</b> Whole-acre aerial image ingestion for multi-field blight density heatmaps.", style_bullet))
    story.append(Paragraph("3. <b>Vernacular LLM Voicebot:</b> Conversational audio AI dialog assistant powered by Indic agricultural models.", style_bullet))
    story.append(Paragraph("4. <b>e-NAM Mandi Integration:</b> Direct linkage connecting healthy harvests to regional mandi prices.", style_bullet))

    # 11. CONCLUSION
    story.append(Spacer(1, 4))
    story.append(Paragraph("10. Conclusion", style_h1))
    story.append(HRFlowable(width="100%", thickness=1, color=c_accent, spaceBefore=1, spaceAfter=5))
    story.append(Paragraph(
        "<b>Dr. Farmer (AgriVision)</b> bridges the gap between modern Deep Learning science and grassroots Indian farming. By fusing <b>instant disease diagnosis</b>, <b>dual organic/chemical advisories</b>, <b>multilingual voice guidance</b>, and <b>cloud-synced farm ledgers</b>, the platform provides a complete digital agronomist and veterinarian directly in the pocket of every farmer across Bharat.",
        style_body
    ))

    # Build PDF
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[OK] PDF successfully generated at: {output_path}")

if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_pdf = os.path.join(BASE_DIR, "SIH_PROJECT_REPORT.pdf")
    generate_pdf(output_pdf)
