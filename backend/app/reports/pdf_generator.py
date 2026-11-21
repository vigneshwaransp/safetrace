import os
from pathlib import Path
from datetime import datetime, timezone
from typing import List

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    HRFlowable,
)

from app.models.case import Case
from app.models.report import Report
from app.models.evidence import EvidenceItem


def generate_complaint_pdf(
    case: Case,
    report: Report,
    evidence_items: List[EvidenceItem],
    output_path: str
) -> str:
    """
    Generate an official, professional legal Evidence & Complaint Dossier using ReportLab:
    - Formal layout for cybercrime.gov.in, police stations, NCW, and NGO submission
    - Tamper-evident cryptographic hash chain tables
    - Exact SHA-256 signatures, capture timestamps, and URLs
    """
    parent_dir = Path(output_path).parent
    parent_dir.mkdir(parents=True, exist_ok=True)

    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40,
    )

    styles = getSampleStyleSheet()

    # Define custom professional styles
    header_style = ParagraphStyle(
        "DocHeader",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=18,
        leading=22,
        textColor=colors.HexColor("#0A1A1A"),
    )

    subhead_style = ParagraphStyle(
        "DocSubHead",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#6A6A6A"),
    )

    section_heading = ParagraphStyle(
        "SectionHeading",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#1A3A3A"),
        spaceBefore=12,
        spaceAfter=6,
    )

    body_style = ParagraphStyle(
        "BodyDark",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#1A1A1A"),
    )

    body_bold = ParagraphStyle(
        "BodyBold",
        parent=body_style,
        fontName="Helvetica-Bold",
    )

    warning_box = ParagraphStyle(
        "WarningBox",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#854D0E"),
    )

    table_cell = ParagraphStyle(
        "TableCell",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8,
        leading=10,
        textColor=colors.HexColor("#0A0A0A"),
    )

    table_cell_code = ParagraphStyle(
        "TableCellCode",
        parent=styles["Normal"],
        fontName="Courier",
        fontSize=7,
        leading=9,
        textColor=colors.HexColor("#1A1A1A"),
    )

    story = []

    # 1. Document Header & Title
    story.append(Paragraph("DIGITAL EVIDENCE & CYBERCRIME COMPLAINT DOSSIER", header_style))
    story.append(Paragraph(f"Official Submission Package | Generated via SafeTrace Verification Platform", subhead_style))
    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#1A3A3A"), spaceAfter=12))

    # 2. Confidentiality & Legal Notice Box
    notice_text = (
        "<b>CONFIDENTIAL LEGAL DOCUMENT</b>: This document contains forensically preserved evidence "
        "of non-consensual image distribution and digital abuse. Intended strictly for law enforcement "
        "(e.g., cybercrime.gov.in, Police Cyber Cell), platform compliance teams, and legal counsel. "
        "Survivor identity is protected under statutory privacy guidelines."
    )
    notice_table = Table([[Paragraph(notice_text, warning_box)]], colWidths=[530])
    notice_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#FEF9C3")),
        ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#EAB308")),
        ("PADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(notice_table)
    story.append(Spacer(1, 12))

    # 3. Case Metadata Table
    now_utc_str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    complainant_name = case.pseudonym if case.is_pseudonymous else (case.user.full_name or "Anonymous Survivor")

    meta_data = [
        [Paragraph("<b>Report Number:</b>", body_style), Paragraph(report.report_number, body_style),
         Paragraph("<b>Date of Issue:</b>", body_style), Paragraph(now_utc_str, body_style)],
        [Paragraph("<b>Case Reference:</b>", body_style), Paragraph(str(case.id), table_cell_code),
         Paragraph("<b>Report Type:</b>", body_style), Paragraph(report.report_type.replace("_", " "), body_style)],
        [Paragraph("<b>Complainant / Identity:</b>", body_style), Paragraph(f"{complainant_name} {'(Pseudonym Protected)' if case.is_pseudonymous else ''}", body_style),
         Paragraph("<b>Target Platform:</b>", body_style), Paragraph(report.recipient_platform or "Cross-Platform / Cybercrime Portal", body_style)],
    ]
    meta_table = Table(meta_data, colWidths=[130, 135, 120, 145])
    meta_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#FAF5E8")),
        ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#E5E5E5")),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#E5E5E5")),
        ("PADDING", (0, 0), (-1, -1), 5),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 14))

    # 4. Applicable Legal Provisions (India & Digital Safety Statutes)
    story.append(Paragraph("Applicable Statutory Provisions", section_heading))
    statutes_text = (
        "This dossier documents unlawful publication and dissemination under applicable penal and cyber laws:<br/>"
        "• <b>Information Technology Act, 2000 (Section 66E)</b>: Punishment for violation of bodily privacy.<br/>"
        "• <b>Information Technology Act, 2000 (Section 67 & 67A)</b>: Publishing/transmitting sexually explicit or obscene material.<br/>"
        "• <b>Bharatiya Nyaya Sanhita (BNS) / IPC (Sec 354C & 354D)</b>: Offenses of Voyeurism and Cyberstalking.<br/>"
        "• <b>IT (Intermediary Guidelines and Digital Media Ethics Code) Rules, 2021 (Rule 3(2)(b))</b>: Mandatory takedown of non-consensual intimate imagery within 24 hours of notification."
    )
    story.append(Paragraph(statutes_text, body_style))
    story.append(Spacer(1, 14))

    # 5. Table of Verified Evidence Items
    story.append(Paragraph(f"Preserved Evidence Items ({len(evidence_items)} Confirmed Findings)", section_heading))

    ev_rows = [[
        Paragraph("<b>Evidence #</b>", body_bold),
        Paragraph("<b>Platform & Source URL</b>", body_bold),
        Paragraph("<b>Captured (UTC)</b>", body_bold),
        Paragraph("<b>Match Score</b>", body_bold),
        Paragraph("<b>Content SHA-256</b>", body_bold),
    ]]

    for it in evidence_items:
        ev_rows.append([
            Paragraph(it.evidence_number, table_cell),
            Paragraph(f"<b>{it.platform}</b><br/>{it.source_url}", table_cell),
            Paragraph(it.captured_at.strftime("%Y-%m-%d<br/>%H:%M:%S"), table_cell),
            Paragraph(f"<b>{it.similarity_score:.1f}%</b>", table_cell),
            Paragraph(it.content_sha256[:20] + "...<br/>" + it.content_sha256[20:40] + "...", table_cell_code),
        ])

    ev_table = Table(ev_rows, colWidths=[75, 185, 80, 65, 125])
    ev_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#EBE6D6")),
        ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#CCCCCC")),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#E5E5E5")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("PADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(ev_table)
    story.append(Spacer(1, 14))

    # 6. Tamper-Evident Cryptographic Hash Chain Audit Trail
    story.append(Paragraph("Tamper-Evident Cryptographic Audit Trail (Hash Chain)", section_heading))
    chain_expl = (
        "Each evidence record is permanently bound to the preceding record through a SHA-256 cryptographic hash chain, "
        "ensuring verifiable authenticity and preventing retrospective tampering or injection."
    )
    story.append(Paragraph(chain_expl, body_style))
    story.append(Spacer(1, 6))

    chain_rows = [[
        Paragraph("<b>Evidence #</b>", body_bold),
        Paragraph("<b>Previous Evidence Hash</b>", body_bold),
        Paragraph("<b>Block Signature (SHA-256)</b>", body_bold),
    ]]

    for it in evidence_items:
        chain_rows.append([
            Paragraph(it.evidence_number, table_cell),
            Paragraph(it.previous_evidence_hash[:32] + ("..." if len(it.previous_evidence_hash) > 32 else ""), table_cell_code),
            Paragraph(it.evidence_hash[:32] + "...", table_cell_code),
        ])

    chain_table = Table(chain_rows, colWidths=[80, 225, 225])
    chain_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#EBE6D6")),
        ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#CCCCCC")),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#E5E5E5")),
        ("PADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(chain_table)
    story.append(Spacer(1, 14))

    # 7. Official Submission Next Steps
    story.append(Paragraph("Official Complaint Submission Checklist", section_heading))
    steps_text = (
        "1. <b>National Cybercrime Portal</b>: Visit <u>cybercrime.gov.in</u> and select 'Report Crime Against Women/Children'. Attach this PDF as certified annexure.<br/>"
        "2. <b>National Helpline Support</b>: Call <b>1930</b> for Cybercrime assistance or <b>181</b> for 24x7 Women Helpline services in India.<br/>"
        "3. <b>Platform Escalation</b>: Submit takedown notices citing Rule 3(2)(b) of the IT Rules 2021 to designated platform Grievance Officers.<br/>"
        "4. <b>Global Hash Protection</b>: Create a proactive cross-platform blocklist via <u>StopNCII.org</u>."
    )
    story.append(Paragraph(steps_text, body_style))

    doc.build(story)
    return output_path
