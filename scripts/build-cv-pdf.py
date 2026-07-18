#!/usr/bin/env python3
"""Generate the printable CV used by the Hugo site."""

from pathlib import Path
from shutil import copy2

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    HRFlowable,
    KeepTogether,
    ListFlowable,
    ListItem,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output" / "pdf" / "mohamed-ayman-cv.pdf"
SITE_OUTPUT = ROOT / "static" / "mohamed-ayman-cv.pdf"

NAVY = colors.HexColor("#102238")
TEAL = colors.HexColor("#0F766E")
MUTED = colors.HexColor("#586779")
PALE = colors.HexColor("#E7F5F2")
RULE = colors.HexColor("#D8E2EA")


def register_fonts():
    candidates = [
        Path("/System/Library/Fonts/Supplemental/Arial.ttf"),
        Path("/Library/Fonts/Arial.ttf"),
    ]
    bold_candidates = [
        Path("/System/Library/Fonts/Supplemental/Arial Bold.ttf"),
        Path("/Library/Fonts/Arial Bold.ttf"),
    ]
    regular = next((path for path in candidates if path.exists()), None)
    bold = next((path for path in bold_candidates if path.exists()), None)
    if regular and bold:
        pdfmetrics.registerFont(TTFont("CVSans", str(regular)))
        pdfmetrics.registerFont(TTFont("CVSans-Bold", str(bold)))
        return "CVSans", "CVSans-Bold"
    return "Helvetica", "Helvetica-Bold"


FONT, FONT_BOLD = register_fonts()
BASE = getSampleStyleSheet()

STYLES = {
    "name": ParagraphStyle(
        "Name",
        parent=BASE["Title"],
        fontName=FONT_BOLD,
        fontSize=24,
        leading=27,
        textColor=NAVY,
        spaceAfter=4,
    ),
    "role": ParagraphStyle(
        "Role",
        parent=BASE["Normal"],
        fontName=FONT_BOLD,
        fontSize=11.5,
        leading=14,
        textColor=TEAL,
        spaceAfter=8,
    ),
    "contact": ParagraphStyle(
        "Contact",
        parent=BASE["Normal"],
        fontName=FONT,
        fontSize=8.2,
        leading=10.5,
        textColor=MUTED,
    ),
    "section": ParagraphStyle(
        "Section",
        parent=BASE["Heading2"],
        fontName=FONT_BOLD,
        fontSize=11.5,
        leading=14,
        textColor=NAVY,
        spaceBefore=9,
        spaceAfter=6,
        borderWidth=0,
    ),
    "body": ParagraphStyle(
        "Body",
        parent=BASE["BodyText"],
        fontName=FONT,
        fontSize=8.7,
        leading=11.5,
        textColor=NAVY,
        spaceAfter=5,
    ),
    "small": ParagraphStyle(
        "Small",
        parent=BASE["BodyText"],
        fontName=FONT,
        fontSize=8.1,
        leading=10.6,
        textColor=NAVY,
        spaceAfter=3,
    ),
    "job": ParagraphStyle(
        "Job",
        parent=BASE["Heading3"],
        fontName=FONT_BOLD,
        fontSize=9.8,
        leading=12,
        textColor=NAVY,
        spaceAfter=1,
    ),
    "date": ParagraphStyle(
        "Date",
        parent=BASE["BodyText"],
        fontName=FONT,
        fontSize=8,
        leading=10,
        textColor=MUTED,
        spaceAfter=4,
    ),
    "skill_label": ParagraphStyle(
        "SkillLabel",
        parent=BASE["BodyText"],
        fontName=FONT_BOLD,
        fontSize=8.2,
        leading=10.5,
        textColor=TEAL,
        spaceAfter=2,
    ),
    "right": ParagraphStyle(
        "Right",
        parent=BASE["BodyText"],
        fontName=FONT,
        fontSize=8,
        leading=10,
        textColor=MUTED,
        alignment=TA_RIGHT,
    ),
}


def section(title):
    return [
        Spacer(1, 2),
        Paragraph(title.upper(), STYLES["section"]),
        HRFlowable(width="100%", thickness=0.7, color=RULE, spaceBefore=0, spaceAfter=5),
    ]


def bullets(items, level=0):
    return ListFlowable(
        [ListItem(Paragraph(item, STYLES["small"]), leftIndent=8) for item in items],
        bulletType="bullet",
        start="circle",
        leftIndent=12 + level * 6,
        bulletFontName=FONT,
        bulletFontSize=5,
        bulletColor=TEAL,
        spaceAfter=4,
    )


def job(title, company, dates, location, items):
    heading = Table(
        [[Paragraph(f"{title} - {company}", STYLES["job"]), Paragraph(f"{dates}<br/>{location}", STYLES["right"]) ]],
        colWidths=[126 * mm, 44 * mm],
    )
    heading.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
    ]))
    return KeepTogether([heading, bullets(items), Spacer(1, 3)])


def skill_block(label, text):
    return [Paragraph(label, STYLES["skill_label"]), Paragraph(text, STYLES["small"])]


def page_decoration(canvas, doc):
    width, height = A4
    canvas.saveState()
    canvas.setFillColor(TEAL)
    canvas.rect(0, height - 5 * mm, width, 5 * mm, stroke=0, fill=1)
    canvas.setStrokeColor(RULE)
    canvas.setLineWidth(0.6)
    canvas.line(20 * mm, 14 * mm, width - 20 * mm, 14 * mm)
    canvas.setFont(FONT, 7.5)
    canvas.setFillColor(MUTED)
    canvas.drawString(20 * mm, 9 * mm, "Mohamed Ayman Abdelbaset | CV")
    canvas.drawRightString(width - 20 * mm, 9 * mm, f"Page {doc.page}")
    canvas.restoreState()


def build_story():
    story = [
        Paragraph("Mohamed Ayman Abdelbaset", STYLES["name"]),
        Paragraph("Solutions Architect | DevOps and Cloud Infrastructure", STYLES["role"]),
        Table(
            [[
                Paragraph("Diemen, Netherlands | mohamedayman@hotmail.com", STYLES["contact"]),
                Paragraph(
                    '<a color="#0F766E" href="https://www.linkedin.com/in/mohamed-abdelbasset-b29b5b66/">LinkedIn</a> | '
                    '<a color="#0F766E" href="https://github.com/moabdelbasset">GitHub</a>',
                    STYLES["right"],
                ),
            ]],
            colWidths=[116 * mm, 54 * mm],
            style=TableStyle([
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
            ]),
        ),
    ]

    story += section("Profile")
    story.append(Paragraph(
        "Solutions-focused infrastructure engineer with <b>10+ years</b> across Linux and Unix, infrastructure automation, and enterprise cloud delivery. I combine hands-on product knowledge with solution design, customer guidance, and ownership of complex escalations. Strongest with <b>Terraform, Ansible/AAP, Kubernetes, OpenShift, and Linux</b> across AWS, Azure, GCP, and Oracle Cloud. Red Hat Certified Architect working toward a Solutions Architect path.",
        STYLES["body"],
    ))

    story += section("Selected impact")
    story.append(bullets([
        "Architected and automated a multi-cloud Terraform Enterprise deployment approach across AWS, Azure, and GCP.",
        "Led on-premises to Oracle Cloud migrations across EMEA and introduced Terraform and Ansible into delivery workflows.",
        "Served as a technical authority for enterprise customers on Terraform Enterprise, Bitbucket, and Bamboo.",
        "Implemented Exadata, SuperCluster, PCA, and ZFSSA engineered systems for customers across the region.",
        "Maintained customer trust with an NPS above 85% in the current IBM role.",
    ]))

    story += section("Core skills")
    skill_data = [
        ("Cloud platforms", "AWS | Google Cloud | Microsoft Azure | Oracle Cloud Infrastructure"),
        ("Architecture and delivery", "Multi-cloud design | Migration planning | Solution scoping | Customer enablement"),
        ("Infrastructure as code", "Terraform | Terraform Enterprise | Ansible | AAP | Execution Environments | GitOps"),
        ("Containers and delivery", "Kubernetes | OpenShift | Docker | GitHub Actions | Bitbucket | Bamboo"),
        ("Systems", "RHEL | Linux | Solaris | AIX | HP-UX | TCP/IP | MPLS | Monitoring"),
    ]
    rows = []
    for index in range(0, len(skill_data), 2):
        row = []
        for label, text in skill_data[index:index + 2]:
            row.append(skill_block(label, text))
        if len(row) == 1:
            row.append([])
        rows.append(row)
    skills_table = Table(rows, colWidths=[84 * mm, 84 * mm], hAlign="LEFT")
    skills_table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(skills_table)

    story += section("Experience")
    story += [
        job("Senior Terraform Support Engineer", "IBM", "Oct 2025 - Present", "Amsterdam", [
            "Architected and automated multi-cloud Terraform Enterprise deployments across AWS, Azure, and GCP.",
            "Act as the primary technical authority for key enterprise clients on platform infrastructure and architecture.",
            "Advise on deployment design and operational best practice while keeping internal runbooks current.",
        ]),
        job("Senior DevTools Support Engineer", "Atlassian", "Mar 2022 - Sep 2025", "Amsterdam", [
            "Owned complex, high-impact enterprise cases across Bitbucket and Bamboo as a dual-product engineer.",
            "Partnered with Tier 3 and Engineering on critical architectural issues and recurring product problems.",
            "Created training, internal documentation, and customer-facing knowledge articles; advised on CI/CD design.",
        ]),
        job("Principal Technical Support Engineer", "Dell RSA", "Jan 2021 - Feb 2022", "Cairo", [
            "Owned highest-severity escalations, root-cause analysis, and preventive fixes end to end.",
            "Validated patches and features in lab, mentored engineers, and supported technical pre-sales work.",
        ]),
        PageBreak(),
    ]

    story += section("Experience continued")
    story += [
        job("Senior Delivery / Implementation Engineer", "Oracle ACS", "Nov 2017 - Dec 2020", "Egypt", [
            "Led on-premises to Oracle Cloud migrations from design through delivery across EMEA.",
            "Introduced Terraform, Ansible, and automation scripts into delivery workflows.",
            "Implemented Exadata, SuperCluster, PCA, and ZFSSA engineered systems.",
        ]),
        job("Senior Systems Engineer", "Vodafone Egypt", "Aug 2014 - Nov 2017", "Cairo", [
            "Designed and operated highly available virtualized environments on Oracle T5 and IBM Power7.",
            "Led Unix-side delivery for billing, CRM, DR drills, upgrades, and online SAN migrations.",
            "Supported more than 200 servers in a 24x7 data center across RHEL, Solaris, and Exadata.",
        ]),
        job("Linux System Administrator", "4GTSS", "Mar 2013 - Aug 2014", "Cairo", [
            "Administered Number Portability systems across six countries using RHEL, Ubuntu, Fedora, CentOS, and Solaris.",
            "Worked across Django, Celery, RabbitMQ, and MySQL Galera.",
        ]),
        job("Network Management Solutions Engineer", "Orange", "Jan 2012 - Mar 2013", "Cairo", [
            "Supported a multi-vendor site migration and a 12-site telecom interconnect over IP/MPLS and ATM networks.",
        ]),
    ]

    story += section("Selected projects")
    story.append(bullets([
        "<b>Containerized AAP 2.6 home lab:</b> Built an all-in-one Proxmox-based environment for execution environments, controller workflows, and automation development.",
        "<b>Engineering blog:</b> Hugo site deployed through GitHub Actions and GitHub Pages for project case studies and practical DevOps notes.",
        "<b>Public engineering board:</b> Learning and project work tracked openly in GitHub Projects and seeded programmatically.",
    ]))

    story += section("Education")
    story.append(Paragraph("<b>MBA, Digital Transformation</b> - ESLSCA, Paris | 2023", STYLES["small"]))
    story.append(Paragraph("<b>B.Sc., Electrical, Electronics and Communications Engineering</b> - Arab Academy for Science and Technology | 2011", STYLES["small"]))
    story.append(PageBreak())

    story += section("Certifications")
    certification_groups = [
        ("Infrastructure as code and automation", [
            "Red Hat Certified Specialist in Developing Automation with Ansible Automation Platform (EX374) - 2026",
            "HashiCorp Certified: Terraform Associate",
            "Red Hat Certified Specialist in Automation with Ansible",
        ]),
        ("Kubernetes, containers, and orchestration", [
            "Red Hat Certified Specialist in OpenShift Administration",
            "Red Hat Certified Specialist in Containers and Kubernetes",
            "Docker Certified Associate",
        ]),
        ("Red Hat and Linux", [
            "Red Hat Certified Architect (RHCA)",
            "Red Hat Certified Engineer (RHCE)",
            "Red Hat Certified System Administrator",
            "Red Hat specialists: system monitoring and performance tuning; clustering and storage; server hardening; deployment and systems management",
        ]),
        ("Cloud", [
            "AWS Certified Solutions Architect - Associate",
            "Oracle Cloud Infrastructure Certified Associate Architect",
            "Oracle Cloud Infrastructure Cloud Operations Associate",
        ]),
        ("Virtualization, storage, networking, and service management", [
            "VMware Certified Professional 6.5 - Data Center Virtualization",
            "Veritas Certified Storage Foundation for Unix 6.1 Administration",
            "Oracle Solaris 11 Advanced System Administrator",
            "CCNA | CCNA Security | ITIL v3 Foundation",
        ]),
        ("Databases", [
            "MongoDB Certified DBA Associate",
        ]),
    ]
    cert_rows = []
    for index in range(0, len(certification_groups), 2):
        cells = []
        for label, items in certification_groups[index:index + 2]:
            cells.append([Paragraph(label, STYLES["skill_label"]), bullets(items)])
        cert_rows.append(cells)
    cert_table = Table(cert_rows, colWidths=[84 * mm, 84 * mm], hAlign="LEFT")
    cert_table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    story.append(cert_table)

    story += section("Languages")
    story.append(Paragraph("<b>English:</b> Full professional | <b>Dutch:</b> Limited working", STYLES["body"]))

    story += section("Links")
    story.append(Paragraph(
        '<a color="#0F766E" href="https://blog.aymantech.net">blog.aymantech.net</a> | '
        '<a color="#0F766E" href="https://github.com/moabdelbasset">github.com/moabdelbasset</a> | '
        '<a color="#0F766E" href="https://www.linkedin.com/in/mohamed-abdelbasset-b29b5b66/">LinkedIn profile</a>',
        STYLES["body"],
    ))
    return story


def main():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    doc = BaseDocTemplate(
        str(OUTPUT),
        pagesize=A4,
        leftMargin=20 * mm,
        rightMargin=20 * mm,
        topMargin=16 * mm,
        bottomMargin=18 * mm,
        title="Mohamed Ayman Abdelbaset - CV",
        author="Mohamed Ayman Abdelbaset",
        subject="Solutions architecture, DevOps, cloud infrastructure, and automation",
    )
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="main")
    doc.addPageTemplates(PageTemplate(id="cv", frames=[frame], onPage=page_decoration))
    doc.build(build_story())
    SITE_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    copy2(OUTPUT, SITE_OUTPUT)
    print(f"Created {OUTPUT}")
    print(f"Published {SITE_OUTPUT}")


if __name__ == "__main__":
    main()
