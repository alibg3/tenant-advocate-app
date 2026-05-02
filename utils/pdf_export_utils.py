from io import BytesIO
import re

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle


### remove emojis for now :(
def _clean_markdown_line(line: str) -> str:
    line = line.strip()

    if line.startswith(">"):
        line = line.lstrip(">").strip()

    line = line.replace("⚠️", "Warning:")

    replacements = {
        "🔴 Illegal": "Illegal",
        "🟠 Unfair": "Unfair",
        "🟢 Standard": "Standard",
        "🔵 Favourable": "Favourable",
        "🔴": "Illegal",
        "🟠": "Unfair",
        "🟢": "Standard",
        "🔵": "Favourable",
    }

    for old, new in replacements.items():
        line = line.replace(old, new)

    line = " ".join(line.split())

    return line


def _markdown_to_reportlab(text: str) -> str:
    """Convert basic Markdown syntax to ReportLab-compatible HTML."""

    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    text = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"\*(.*?)\*", r"<i>\1</i>", text)

    return text


def _is_markdown_table(lines: list[str], index: int) -> bool:
    return (
        index + 1 < len(lines)
        and "|" in lines[index]
        and "|" in lines[index + 1]
        and "---" in lines[index + 1]
    )


def _parse_markdown_table(lines: list[str], start_index: int):
    table_lines = []
    index = start_index

    while index < len(lines) and "|" in lines[index]:
        table_lines.append(lines[index])
        index += 1

    rows = []

    for line in table_lines:
        cells = [
            _clean_markdown_line(cell.strip())
            for cell in line.strip().strip("|").split("|")
        ]

        if all(set(cell) <= {"-", " "} for cell in cells):
            continue

        rows.append([_markdown_to_reportlab(cell) for cell in cells])

    return rows, index


def _is_warning_line(line: str) -> bool:
    warning_keywords = [
        "Warning:",
        "not legal advice",
        "NCAT NOTICE",
        "information tool only",
    ]

    return any(keyword.lower() in line.lower() for keyword in warning_keywords)


def create_pdf_from_text(text: str, title: str = "Document") -> bytes:
    """Create a readable PDF from Markdown-like text."""

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
    )

    styles = getSampleStyleSheet()

    styles.add(
        ParagraphStyle(
            name="CustomTitle",
            parent=styles["Title"],
            fontSize=20,
            leading=26,
            spaceAfter=18,
        )
    )

    styles.add(
        ParagraphStyle(
            name="CustomHeading2",
            parent=styles["Heading2"],
            fontSize=15,
            leading=20,
            spaceBefore=14,
            spaceAfter=8,
        )
    )

    styles.add(
        ParagraphStyle(
            name="CustomHeading3",
            parent=styles["Heading3"],
            fontSize=12,
            leading=16,
            spaceBefore=10,
            spaceAfter=6,
        )
    )

    styles.add(
        ParagraphStyle(
            name="CustomBody",
            parent=styles["BodyText"],
            fontSize=10,
            leading=14,
            spaceAfter=6,
        )
    )

    styles.add(
        ParagraphStyle(
            name="WarningText",
            parent=styles["CustomBody"],
            textColor=colors.darkorange,
            backColor=colors.whitesmoke,
            borderColor=colors.orange,
            borderWidth=0.5,
            borderPadding=6,
            spaceBefore=8,
            spaceAfter=8,
        )
    )

    story = [Paragraph(title, styles["CustomTitle"])]

    lines = text.splitlines()
    index = 0

    while index < len(lines):
        line = _clean_markdown_line(lines[index])

        if not line:
            story.append(Spacer(1, 6))
            index += 1
            continue

        if line == "---":
            story.append(Spacer(1, 10))
            index += 1
            continue

        if _is_markdown_table(lines, index):
            rows, index = _parse_markdown_table(lines, index)

            if rows:
                table_data = [
                    [Paragraph(cell, styles["CustomBody"]) for cell in row]
                    for row in rows
                ]

                table = Table(table_data, hAlign="LEFT")
                table.setStyle(
                    TableStyle(
                        [
                            ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
                            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                            ("VALIGN", (0, 0), (-1, -1), "TOP"),
                            ("LEFTPADDING", (0, 0), (-1, -1), 6),
                            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                            ("TOPPADDING", (0, 0), (-1, -1), 5),
                            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                        ]
                    )
                )

                story.append(table)
                story.append(Spacer(1, 10))

            continue

        if _is_warning_line(line):
            story.append(
                Paragraph(
                    _markdown_to_reportlab(line),
                    styles["WarningText"],
                )
            )
            index += 1
            continue

        if line.startswith("## "):
            story.append(
                Paragraph(
                    _markdown_to_reportlab(line.replace("## ", "", 1)),
                    styles["CustomHeading2"],
                )
            )

        elif line.startswith("### "):
            story.append(
                Paragraph(
                    _markdown_to_reportlab(line.replace("### ", "", 1)),
                    styles["CustomHeading3"],
                )
            )

        elif line.startswith("#### "):
            story.append(
                Paragraph(
                    _markdown_to_reportlab(line.replace("#### ", "", 1)),
                    styles["CustomHeading3"],
                )
            )

        else:
            story.append(
                Paragraph(
                    _markdown_to_reportlab(line),
                    styles["CustomBody"],
                )
            )

        index += 1

    doc.build(story)

    pdf = buffer.getvalue()
    buffer.close()

    return pdf