from __future__ import annotations
from io import BytesIO
from datetime import datetime
from typing import Dict, List, Any, Optional

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


def _register_korean_font(font_path: str) -> str:
    """Register and return font name."""
    font_name = "NanumGothic"
    try:
        pdfmetrics.getFont(font_name)
        return font_name
    except Exception:
        pass
    pdfmetrics.registerFont(TTFont(font_name, font_path))
    return font_name


def build_report_pdf(
    *,
    font_path: str,
    student_id: str,
    student_name: str,
    unit_title: str,
    results: Dict[str, Any],
) -> bytes:
    """Create a simple PDF report (Korean-capable) and return as bytes."""
    font_name = _register_korean_font(font_path)

    buf = BytesIO()
    doc = SimpleDocTemplate(
        buf,
        pagesize=A4,
        leftMargin=18*mm,
        rightMargin=18*mm,
        topMargin=16*mm,
        bottomMargin=16*mm,
        title="학습 결과 보고서",
    )

    styles = getSampleStyleSheet()
    base = ParagraphStyle(
        "Base",
        parent=styles["Normal"],
        fontName=font_name,
        fontSize=11,
        leading=15,
        spaceAfter=6,
    )
    title_style = ParagraphStyle(
        "TitleK",
        parent=styles["Title"],
        fontName=font_name,
        fontSize=18,
        leading=22,
        spaceAfter=10,
    )
    h_style = ParagraphStyle(
        "H",
        parent=styles["Heading2"],
        fontName=font_name,
        fontSize=13,
        leading=18,
        spaceBefore=8,
        spaceAfter=6,
    )
    small = ParagraphStyle(
        "Small",
        parent=base,
        fontName=font_name,
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#374151"),
    )

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    story = []

    story.append(Paragraph("학습 결과 보고서", title_style))
    story.append(Paragraph(f"<b>단원</b>: {unit_title}", base))
    story.append(Paragraph(f"<b>학번</b>: {student_id} &nbsp;&nbsp; <b>이름</b>: {student_name}", base))
    story.append(Paragraph(f"<b>생성 시각</b>: {now}", small))
    story.append(Spacer(1, 6))

    # OX summary
    ox = results.get("ox")
    if ox and isinstance(ox, dict):
        story.append(Paragraph("개념 확인(○,×)", h_style))
        score = ox.get("score", 0)
        total = ox.get("total", 0)
        story.append(Paragraph(f"점수: <b>{score}</b> / {total}", base))

        rows = [["번호", "문항", "선택", "정답", "결과"]]
        for i, item in enumerate(ox.get("items", []), start=1):
            rows.append([
                str(i),
                item.get("q", ""),
                item.get("choice", "-"),
                item.get("answer", "-"),
                "정답" if item.get("is_correct") else "오답",
            ])

        tbl = Table(rows, colWidths=[12*mm, 110*mm, 16*mm, 16*mm, 16*mm])
        tbl.setStyle(TableStyle([
            ("FONTNAME", (0,0), (-1,-1), font_name),
            ("FONTSIZE", (0,0), (-1,-1), 9),
            ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#EEEAFE")),
            ("TEXTCOLOR", (0,0), (-1,0), colors.HexColor("#111827")),
            ("GRID", (0,0), (-1,-1), 0.5, colors.HexColor("#D1D5DB")),
            ("VALIGN", (0,0), (-1,-1), "TOP"),
            ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, colors.HexColor("#FBFBFF")]),
        ]))
        story.append(tbl)
        story.append(Spacer(1, 8))

    # Activities summary
    acts = results.get("activities")
    if acts and isinstance(acts, list):
        story.append(Paragraph("활동/실습 기록", h_style))
        for a in acts:
            name = a.get("name", "활동")
            desc = a.get("desc", "")
            story.append(Paragraph(f"• <b>{name}</b>: {desc}", base))
        story.append(Spacer(1, 4))

    # Free text (problem solving)
    note = results.get("note")
    if note:
        story.append(Paragraph("작성 내용", h_style))
        # Preserve newlines
        safe = str(note).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        safe = safe.replace("\n", "<br/>")
        story.append(Paragraph(safe, base))

    doc.build(story)
    return buf.getvalue()
