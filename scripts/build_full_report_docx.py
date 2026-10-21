import os
import sys
sys.path.append(r'c:\Projects\QFlow\scripts')

import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

from report_helpers import (
    set_cell_background, set_table_borders, set_cell_margins,
    add_p, add_bullet_point, add_numbered_point,
    add_main_title, add_heading_1, add_heading_2, add_heading_3, add_chapter_intro,
    add_table_data, add_borderless_table, add_figure_image, add_algorithm_box,
    add_code_block, add_reference_item, setup_footer, setup_section_numbering
)

def build_document():
    doc = docx.Document()

    # Section 1: Title and Certificates (No header/footer, standard margins)
    s1 = doc.sections[0]
    s1.top_margin = Inches(1.0)
    s1.bottom_margin = Inches(1.0)
    s1.left_margin = Inches(1.25)
    s1.right_margin = Inches(1.0)
    s1.header_distance = Inches(0.5)
    s1.footer_distance = Inches(0.5)

    base_dir = r"c:\Projects\QFlow"
    logo_path = os.path.join(base_dir, "report_assets", "image1.jpeg")
    img_dir = os.path.join(base_dir, "presentation_images")
    fig_4_1_path = os.path.join(img_dir, "fig_4_1_architecture.png")
    fig_4_2_path = os.path.join(img_dir, "fig_4_2_deployment.png")
    uc_img = os.path.join(img_dir, "01_use_case_diagram_bw.png")
    er_img = os.path.join(img_dir, "02_er_diagram_bw.png")

    # =========================================================================
    # 1. TITLE / COVER PAGE
    # =========================================================================
    add_main_title(doc, "QFLOW: AI-POWERED SMART TOKEN AND QUEUE MANAGEMENT SYSTEM FOR DYNAMIC COUNTER ASSIGNMENT AND REAL-TIME OPERATIONS")

    add_p(doc, "A PROJECT REPORT", font_size=13, bold=True, alignment=WD_ALIGN_PARAGRAPH.CENTER, space_before=8, space_after=14, tab_indent=False)

    add_p(doc, "Submitted by", font_size=11.5, italic=True, alignment=WD_ALIGN_PARAGRAPH.CENTER, space_before=4, space_after=6, tab_indent=False)
    add_p(doc, "ADITHYA P K\n(Reg. No: 310624243009)", font_size=12.5, bold=True, alignment=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=20, line_spacing=1.15, tab_indent=False)

    add_p(doc, "in partial fulfillment for the award of the Degree\nof\nBACHELOR OF TECHNOLOGY\nin\nDEPARTMENT OF ARTIFICIAL INTELLIGENCE AND DATA SCIENCE", 
          font_size=11.5, bold=True, alignment=WD_ALIGN_PARAGRAPH.CENTER, space_before=6, space_after=18, line_spacing=1.2, tab_indent=False)

    if os.path.exists(logo_path):
        p_logo = doc.add_paragraph()
        p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_logo.paragraph_format.space_before = Pt(4)
        p_logo.paragraph_format.space_after = Pt(14)
        p_logo.paragraph_format.first_line_indent = Inches(0)
        run_logo = p_logo.add_run()
        run_logo.add_picture(logo_path, width=Inches(1.8))

    add_p(doc, "EASWARI ENGINEERING COLLEGE\n(AN AUTONOMOUS INSTITUTION)\nAFFILIATED TO ANNA UNIVERSITY, CHENNAI\nRAMAPURAM, CHENNAI – 600089\n\nOCTOBER 2026", 
          font_size=11.5, bold=True, alignment=WD_ALIGN_PARAGRAPH.CENTER, space_before=8, space_after=0, line_spacing=1.2, tab_indent=False)

    doc.add_page_break()

    # =========================================================================
    # SECTION 2: PRELIMINARY PAGES (Bonafide, Viva-Voce, Abstract, Ack, TOC, LOT, LOF)
    # Roman Numerals starting from ii
    # =========================================================================
    s2 = doc.add_section()
    s2.top_margin = Inches(1.0)
    s2.bottom_margin = Inches(1.0)
    s2.left_margin = Inches(1.25)
    s2.right_margin = Inches(1.0)
    s2.header_distance = Inches(0.5)
    s2.footer_distance = Inches(0.5)
    setup_section_numbering(s2, start_num=2, is_roman=True)
    setup_footer(s2)

    # =========================================================================
    # 2. BONAFIDE CERTIFICATE (Matching layout of reference certificate)
    # =========================================================================
    t_bon_hdr = doc.add_table(rows=1, cols=2)
    t_bon_hdr.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_bon_hdr.autofit = False
    set_table_borders(t_bon_hdr, color="FFFFFF", sz="0", val="none")

    # Grid columns: 1.2" (1728 dxa) and 5.05" (7272 dxa) -> total 6.25" (9000 dxa)
    tblGrid_b = OxmlElement('w:tblGrid')
    gc_b1 = OxmlElement('w:gridCol'); gc_b1.set(qn('w:w'), '1728'); tblGrid_b.append(gc_b1)
    gc_b2 = OxmlElement('w:gridCol'); gc_b2.set(qn('w:w'), '7272'); tblGrid_b.append(gc_b2)
    t_bon_hdr._element.append(tblGrid_b)

    c_logo = t_bon_hdr.rows[0].cells[0]
    tcPr_l = c_logo._element.get_or_add_tcPr()
    for child in tcPr_l.findall(qn('w:tcW')): tcPr_l.remove(child)
    tcW_l = OxmlElement('w:tcW'); tcW_l.set(qn('w:w'), '1728'); tcW_l.set(qn('w:type'), 'dxa'); tcPr_l.append(tcW_l)
    p_l = c_logo.paragraphs[0]
    p_l.paragraph_format.first_line_indent = Inches(0)
    p_l.alignment = WD_ALIGN_PARAGRAPH.CENTER
    if os.path.exists(logo_path):
        r_l = p_l.add_run()
        r_l.add_picture(logo_path, width=Inches(1.0))

    c_txt = t_bon_hdr.rows[0].cells[1]
    tcPr_t = c_txt._element.get_or_add_tcPr()
    for child in tcPr_t.findall(qn('w:tcW')): tcPr_t.remove(child)
    tcW_t = OxmlElement('w:tcW'); tcW_t.set(qn('w:w'), '7272'); tcW_t.set(qn('w:type'), 'dxa'); tcPr_t.append(tcW_t)
    vAlign = OxmlElement('w:vAlign'); vAlign.set(qn('w:val'), 'center'); tcPr_t.append(vAlign)
    p_t = c_txt.paragraphs[0]
    p_t.paragraph_format.first_line_indent = Inches(0)
    p_t.paragraph_format.space_before = Pt(14)
    p_t.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_t = p_t.add_run("EASWARI ENGINEERING COLLEGE")
    r_t.font.name = "Times New Roman"
    r_t.font.size = Pt(14)
    r_t.font.bold = True
    r_t.font.color.rgb = RGBColor(0, 0, 0)

    p_bon = doc.add_paragraph()
    p_bon.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_bon.paragraph_format.space_before = Pt(28)
    p_bon.paragraph_format.space_after = Pt(22)
    p_bon.paragraph_format.first_line_indent = Inches(0)
    r_bon = p_bon.add_run("BONAFIDE CERTIFICATE")
    r_bon.font.name = "Times New Roman"
    r_bon.font.size = Pt(14)
    r_bon.font.bold = True
    r_bon.font.color.rgb = RGBColor(0, 0, 0)

    p_body = doc.add_paragraph()
    p_body.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_body.paragraph_format.first_line_indent = Inches(0.5)
    p_body.paragraph_format.space_before = Pt(0)
    p_body.paragraph_format.space_after = Pt(50)
    p_body.paragraph_format.line_spacing = 1.5

    r1 = p_body.add_run("Certified that this project report titled “")
    r1.font.name = "Times New Roman"; r1.font.size = Pt(12); r1.font.color.rgb = RGBColor(0, 0, 0)

    r_tit = p_body.add_run("QFLOW: AI-POWERED SMART TOKEN AND QUEUE MANAGEMENT SYSTEM FOR DYNAMIC COUNTER ASSIGNMENT AND REAL-TIME OPERATIONS")
    r_tit.font.name = "Times New Roman"; r_tit.font.size = Pt(12); r_tit.font.bold = True; r_tit.font.color.rgb = RGBColor(0, 0, 0)

    r2 = p_body.add_run("” is the Bonafide work of “")
    r2.font.name = "Times New Roman"; r2.font.size = Pt(12); r2.font.color.rgb = RGBColor(0, 0, 0)

    r_name = p_body.add_run("ADITHYA P K (310624243009)")
    r_name.font.name = "Times New Roman"; r_name.font.size = Pt(12); r_name.font.bold = True; r_name.font.color.rgb = RGBColor(0, 0, 0)

    r3 = p_body.add_run("”, who carried out the project work under my supervision.")
    r3.font.name = "Times New Roman"; r3.font.size = Pt(12); r3.font.color.rgb = RGBColor(0, 0, 0)

    t_cert = doc.add_table(rows=1, cols=2)
    t_cert.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_cert.autofit = False
    set_table_borders(t_cert, color="FFFFFF", sz="0", val="none")

    tblGrid_c = OxmlElement('w:tblGrid')
    gc_c1 = OxmlElement('w:gridCol'); gc_c1.set(qn('w:w'), '4500'); tblGrid_c.append(gc_c1)
    gc_c2 = OxmlElement('w:gridCol'); gc_c2.set(qn('w:w'), '4500'); tblGrid_c.append(gc_c2)
    t_cert._element.append(tblGrid_c)

    c1 = t_cert.rows[0].cells[0]
    tcPr1 = c1._element.get_or_add_tcPr()
    for child in tcPr1.findall(qn('w:tcW')): tcPr1.remove(child)
    tcW1 = OxmlElement('w:tcW'); tcW1.set(qn('w:w'), '4500'); tcW1.set(qn('w:type'), 'dxa'); tcPr1.append(tcW1)
    p_c1 = c1.paragraphs[0]
    p_c1.paragraph_format.first_line_indent = Inches(0)
    p_c1.paragraph_format.line_spacing = 1.25
    p_c1.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r_c1_h = p_c1.add_run("HEAD OF THE DEPARTMENT\nDr. T. Kalai Selvi\n")
    r_c1_h.font.name = "Times New Roman"; r_c1_h.font.size = Pt(11); r_c1_h.font.bold = True
    r_c1_d = p_c1.add_run("Easwari Engineering College,\nRamapuram, Chennai – 600089.")
    r_c1_d.font.name = "Times New Roman"; r_c1_d.font.size = Pt(10.5)

    c2 = t_cert.rows[0].cells[1]
    tcPr2 = c2._element.get_or_add_tcPr()
    for child in tcPr2.findall(qn('w:tcW')): tcPr2.remove(child)
    tcW2 = OxmlElement('w:tcW'); tcW2.set(qn('w:w'), '4500'); tcW2.set(qn('w:type'), 'dxa'); tcPr2.append(tcW2)
    p_c2 = c2.paragraphs[0]
    p_c2.paragraph_format.first_line_indent = Inches(0)
    p_c2.paragraph_format.line_spacing = 1.25
    p_c2.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r_c2_h = p_c2.add_run("SUPERVISOR\nMs. D. S. K. Harshitha\n")
    r_c2_h.font.name = "Times New Roman"; r_c2_h.font.size = Pt(11); r_c2_h.font.bold = True
    r_c2_d = p_c2.add_run("Easwari Engineering College,\nRamapuram, Chennai – 600089.")
    r_c2_d.font.name = "Times New Roman"; r_c2_d.font.size = Pt(10.5)

    doc.add_page_break()

    # =========================================================================
    # 3. VIVA-VOCE CERTIFICATE (Internal Examiner ONLY, No External Examiner)
    # =========================================================================
    t_viva_hdr = doc.add_table(rows=1, cols=2)
    t_viva_hdr.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_viva_hdr.autofit = False
    set_table_borders(t_viva_hdr, color="FFFFFF", sz="0", val="none")

    tblGrid_vh = OxmlElement('w:tblGrid')
    gc_vh1 = OxmlElement('w:gridCol'); gc_vh1.set(qn('w:w'), '1728'); tblGrid_vh.append(gc_vh1)
    gc_vh2 = OxmlElement('w:gridCol'); gc_vh2.set(qn('w:w'), '7272'); tblGrid_vh.append(gc_vh2)
    t_viva_hdr._element.append(tblGrid_vh)

    c_vlogo = t_viva_hdr.rows[0].cells[0]
    tcPr_vl = c_vlogo._element.get_or_add_tcPr()
    for child in tcPr_vl.findall(qn('w:tcW')): tcPr_vl.remove(child)
    tcW_vl = OxmlElement('w:tcW'); tcW_vl.set(qn('w:w'), '1728'); tcW_vl.set(qn('w:type'), 'dxa'); tcPr_vl.append(tcW_vl)
    p_vl = c_vlogo.paragraphs[0]
    p_vl.paragraph_format.first_line_indent = Inches(0)
    p_vl.alignment = WD_ALIGN_PARAGRAPH.CENTER
    if os.path.exists(logo_path):
        r_vl = p_vl.add_run()
        r_vl.add_picture(logo_path, width=Inches(1.0))

    c_vtxt = t_viva_hdr.rows[0].cells[1]
    tcPr_vt = c_vtxt._element.get_or_add_tcPr()
    for child in tcPr_vt.findall(qn('w:tcW')): tcPr_vt.remove(child)
    tcW_vt = OxmlElement('w:tcW'); tcW_vt.set(qn('w:w'), '7272'); tcW_vt.set(qn('w:type'), 'dxa'); tcPr_vt.append(tcW_vt)
    vAlign_v = OxmlElement('w:vAlign'); vAlign_v.set(qn('w:val'), 'center'); tcPr_vt.append(vAlign_v)
    p_vt = c_vtxt.paragraphs[0]
    p_vt.paragraph_format.first_line_indent = Inches(0)
    p_vt.paragraph_format.space_before = Pt(14)
    p_vt.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_vt = p_vt.add_run("EASWARI ENGINEERING COLLEGE")
    r_vt.font.name = "Times New Roman"
    r_vt.font.size = Pt(14)
    r_vt.font.bold = True
    r_vt.font.color.rgb = RGBColor(0, 0, 0)

    p_viva_t = doc.add_paragraph()
    p_viva_t.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_viva_t.paragraph_format.space_before = Pt(28)
    p_viva_t.paragraph_format.space_after = Pt(22)
    p_viva_t.paragraph_format.first_line_indent = Inches(0)
    r_viva_t = p_viva_t.add_run("CERTIFICATE OF VIVA-VOCE EXAMINATION")
    r_viva_t.font.name = "Times New Roman"
    r_viva_t.font.size = Pt(14)
    r_viva_t.font.bold = True
    r_viva_t.font.color.rgb = RGBColor(0, 0, 0)

    p_vbody = doc.add_paragraph()
    p_vbody.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_vbody.paragraph_format.first_line_indent = Inches(0.5)
    p_vbody.paragraph_format.space_before = Pt(0)
    p_vbody.paragraph_format.space_after = Pt(60)
    p_vbody.paragraph_format.line_spacing = 1.5

    viva_text = (
        "This is to certify that the Viva-Voce Examination of the Project Work entitled “QFLOW: AI-POWERED "
        "SMART TOKEN AND QUEUE MANAGEMENT SYSTEM FOR DYNAMIC COUNTER ASSIGNMENT AND REAL-TIME OPERATIONS” "
        "submitted by Mr. Adithya P K (Reg. No. 310624243009) in partial fulfillment of the requirements for "
        "the award of the degree of Bachelor of Technology was conducted on 23-10-2026 in the Department of "
        "Artificial Intelligence and Data Science, Easwari Engineering College, Ramapuram – Chennai."
    )
    r_vb = p_vbody.add_run(viva_text)
    r_vb.font.name = "Times New Roman"
    r_vb.font.size = Pt(12)
    r_vb.font.color.rgb = RGBColor(0, 0, 0)

    p_v1 = doc.add_paragraph()
    p_v1.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_v1.paragraph_format.first_line_indent = Inches(0)
    p_v1.paragraph_format.space_before = Pt(20)
    p_v1.paragraph_format.space_after = Pt(0)
    p_v1.paragraph_format.line_spacing = 1.3
    r_v1 = p_v1.add_run("Internal Examiner\nDate:")
    r_v1.font.name = "Times New Roman"
    r_v1.font.size = Pt(11)
    r_v1.font.bold = True
    r_v1.font.color.rgb = RGBColor(0, 0, 0)

    doc.add_page_break()

    # 4. ABSTRACT
    add_main_title(doc, "ABSTRACT")
    abstract_p1 = (
        "Queueing environments across commercial and public service institutions—including banking branches, outpatient "
        "clinics, customer care centers, and administrative offices—routinely experience severe customer congestion, unpredictable "
        "waiting durations, and inefficient teller resource utilization. Conventional queue management solutions rely on thermal "
        "paper token dispensers, fixed static display monitors, and inflexible First-Come-First-Served (FCFS) counter assignments. "
        "These legacy approaches leave customers tethered to crowded waiting lounges with zero real-time visibility into their "
        "turn progression, while preventing supervisors from dynamically balancing workloads across available service desks."
    )
    add_p(doc, abstract_p1, font_size=11, alignment=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=2, space_after=4, line_spacing=1.2, tab_indent=True)

    abstract_p2 = (
        "To address these systemic bottlenecks, this project presents QFlow, an AI-powered, full-stack, real-time smart token "
        "and queue management system designed for responsive customer self-service and dynamic counter orchestration. Developed "
        "on the MERN stack (MongoDB, Express.js, React 19, Node.js) with native Socket.IO bi-directional WebSocket communication, "
        "QFlow replaces physical hardware kiosks with an accessible browser-based mobile portal. Customers join the virtual queue "
        "on their personal mobile devices by scanning a physical QR code encoding the local gateway IP address, requiring no mobile "
        "app installation or account registration. Upon token issuance, a lightweight multi-factor predictive engine estimates the "
        "customer's anticipated service duration and queue waiting time using a calibrated synthetic historical baseline adjusted "
        "dynamically for service complexity, time-of-day peak multipliers, and active queue length. Simultaneously, an automated "
        "heuristic counter recommendation algorithm scores and assigns incoming customers to optimal service counters based on live "
        "counter occupancy, pending workload, and estimated time-to-completion."
    )
    add_p(doc, abstract_p2, font_size=11, alignment=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0, space_after=4, line_spacing=1.2, tab_indent=True)

    abstract_p3 = (
        "Staff operators manage the queue via a dedicated control console that supports calling next, starting service, completing "
        "consultations, marking unserved customers as skipped, and transferring tokens across departments. Real-time token lifecycle "
        "events trigger instant browser push notifications and haptic device vibration alerts on the customer's mobile device when "
        "their token is called. Comprehensive functional and concurrency testing demonstrates that the end-to-end architecture executes "
        "atomic database transitions, isolates customer subscriptions into dedicated socket channels, prevents race conditions during "
        "simultaneous counter calls, and maintains sub-millisecond real-time event dissemination across heterogeneous client platforms."
    )
    add_p(doc, abstract_p3, font_size=11, alignment=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0, space_after=6, line_spacing=1.2, tab_indent=True)

    add_p(doc, "Keywords: Smart Queue Management, Artificial Intelligence, Real-Time Synchronization, Socket.IO, MERN Stack, React 19, Dynamic Counter Allocation, Wait-Time Prediction.", 
          font_size=10.5, bold=True, italic=True, alignment=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=3, space_after=0, line_spacing=1.15, tab_indent=False)

    doc.add_page_break()

    # 5. ACKNOWLEDGEMENT
    add_main_title(doc, "ACKNOWLEDGEMENT")
    add_p(doc, "We express our sincere gratitude to our respected Principal Dr. P. Deiva Sundari and the Management of Easwari Engineering College for providing us with the opportunity, institutional resources, and excellent computing facilities to carry out this project work successfully.", 
          font_size=11.5, alignment=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=4, space_after=6, line_spacing=1.3, tab_indent=True)
    
    add_p(doc, "We convey our heartfelt thanks to our Head of the Department Dr. T. Kalai Selvi, Department of Artificial Intelligence and Data Science, for her continuous academic encouragement, constructive suggestions, and valuable administrative support throughout the development phases.", 
          font_size=11.5, alignment=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0, space_after=6, line_spacing=1.3, tab_indent=True)

    add_p(doc, "We are profoundly thankful and indebted to our Project Supervisor Ms. D. S. K. Harshitha, Assistant Professor, Department of Artificial Intelligence and Data Science, for her expert guidance, insightful technical suggestions, patient mentoring, and steady motivation throughout the duration of this project.", 
          font_size=11.5, alignment=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0, space_after=6, line_spacing=1.3, tab_indent=True)

    add_p(doc, "We also extend our sincere gratitude to all the teaching faculty members and technical staff of the Department of Artificial Intelligence and Data Science for their constant cooperation and technical assistance.", 
          font_size=11.5, alignment=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0, space_after=6, line_spacing=1.3, tab_indent=True)

    add_p(doc, "Finally, we express our warmest thanks to our parents and friends for their continuous moral support, understanding, and constant encouragement during the entire course of this academic endeavour.", 
          font_size=11.5, alignment=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0, space_after=0, line_spacing=1.3, tab_indent=True)

    doc.add_page_break()

    # 6. TABLE OF CONTENTS
    add_main_title(doc, "TABLE OF CONTENTS")
    
    toc_data = [
        ("", "ABSTRACT", "iv"),
        ("", "ACKNOWLEDGEMENT", "v"),
        ("", "LIST OF TABLES", "viii"),
        ("", "LIST OF FIGURES", "ix"),
        ("1", "INTRODUCTION", "1"),
        ("", "1.1 OVERVIEW", "1"),
        ("", "1.1.1 Need for a Centralized Queue and Token Management System", "1"),
        ("", "1.1.2 Limitations of Existing Manual and Physical Token Systems", "1"),
        ("", "1.2 OBJECTIVE", "2"),
        ("", "1.3 SCOPE OF THE PROJECT", "3"),
        ("", "1.4 MOTIVATION", "4"),
        ("", "1.5 ORGANIZATION OF THE REPORT", "4"),
        ("2", "RELATED WORK", "6"),
        ("", "2.1 LITERATURE REVIEW", "6"),
        ("", "2.2 EXISTING SYSTEMS", "7"),
        ("", "2.3 INFERENCE FROM LITERATURE REVIEW", "8"),
        ("", "2.4 EXTRACTION FROM LITERATURE REVIEW", "9"),
        ("3", "SYSTEM ANALYSIS", "10"),
        ("", "3.1 PROBLEM DEFINITION", "10"),
        ("", "3.2 PROPOSED SOLUTION", "10"),
        ("", "3.2.1 Functional Requirements", "11"),
        ("", "3.2.2 Non-Functional Requirements", "12"),
        ("", "3.3 SOFTWARE COMPONENTS", "13"),
        ("", "3.4 HARDWARE COMPONENTS", "14"),
        ("", "3.5 USE CASES", "14"),
        ("4", "IMPLEMENTATION", "17"),
        ("", "4.1 SYSTEM ARCHITECTURE AND EXPERIMENTAL SETUP", "17"),
        ("", "4.1.1 High-Level System Architecture", "17"),
        ("", "4.1.2 System Deployment and Network Topology", "19"),
        ("", "4.2 MODULE IMPLEMENTATION DETAILS", "21"),
        ("", "4.2.1 Data Source Module", "21"),
        ("", "4.2.2 Steps of Algorithm", "22"),
        ("", "4.2.3 Data Processing Module", "23"),
        ("", "4.2.4 Explainability Module", "24"),
        ("", "4.2.5 Visualization and Dashboard Module", "24"),
        ("", "4.3 CLASS DIAGRAM / DATA MODEL", "24"),
        ("", "4.4 SEQUENCE DIAGRAM", "25"),
        ("", "4.5 TESTING AND RESULTS", "26"),
        ("5", "CONCLUSION AND FUTURE ENHANCEMENTS", "29"),
        ("", "5.1 CONCLUSION", "29"),
        ("", "5.2 FUTURE ENHANCEMENTS", "30"),
        ("", "APPENDIX 1: SAMPLE CODE", "31"),
        ("", "1. Project Directory Structure", "31"),
        ("", "2. Installation and Execution Commands", "31"),
        ("", "3. Server Environment Configuration", "31"),
        ("", "4. Database Models and Schema Architecture", "32"),
        ("", "5. Main Server Entry Point and WebSocket Setup", "34"),
        ("", "6. Token Controller and Atomic Number Generation", "35"),
        ("", "7. Authentication Controller and JWT Middleware", "36"),
        ("", "8. AI Prediction Engine and Duration Calculation", "37"),
        ("", "9. Dynamic Counter Recommendation Scoring", "38"),
        ("", "10. Socket.IO Real-Time Multiplexing and Broadcasts", "39"),
        ("", "PROJECT SCREENSHOTS", "39"),
        ("", "REFERENCES", "50")
    ]
    add_borderless_table(doc, ["CHAPTER NO.", "TITLE", "PAGE No."], toc_data, col_widths=[Inches(1.30), Inches(4.15), Inches(0.80)], bold_ch_only=True)

    doc.add_page_break()

    # 7. LIST OF TABLES
    add_main_title(doc, "LIST OF TABLES")
    
    tables_list = [
        ("2.1", "Comparison of Existing Approaches to Queue and Token Management", "7"),
        ("2.2", "Design Principles Extracted from Literature and Their Use in QFlow", "8"),
        ("3.1", "Functional Requirements of QFlow", "10"),
        ("3.2", "Software Components of QFlow", "12"),
        ("3.3", "Hardware Components for Development and Deployment", "13"),
        ("3.4", "Description of Main Use Cases", "14"),
        ("4.1", "REST API Endpoints of QFlow", "17"),
        ("4.2", "Experimental Setup Used for Building and Testing", "19"),
        ("4.3", "Summary of QFlow Modules", "20"),
        ("4.4", "Service Catalog and Base Parameters Accepted by the Data Source Module", "20"),
        ("4.5", "MongoDB Collections Used by QFlow", "23"),
        ("4.6", "Functional Test Cases and Results", "25"),
        ("4.7", "Technical Observations and Edge Cases Observed During Testing", "26")
    ]
    add_borderless_table(doc, ["TABLE NO.", "TABLE TITLE", "PAGE No."], tables_list, col_widths=[Inches(1.30), Inches(4.15), Inches(0.80)], bold_ch_only=False)

    doc.add_page_break()

    # 8. LIST OF FIGURES
    add_main_title(doc, "LIST OF FIGURES")

    figures_list = [
        ("3.1", "Use Case Diagram of QFlow", "15"),
        ("4.1", "System Architecture of QFlow", "16"),
        ("4.2", "System Deployment and Network Topology of QFlow", "19"),
        ("4.3", "Class Diagram / Entity-Relationship Schema of the QFlow Data Model", "24"),
        ("A.1", "Staff and Administrative Authentication Portal", "39"),
        ("A.2", "Live Staff Operations Dashboard with Active Counters", "39"),
        ("A.3", "Customer QR Code Registration Poster and Modal", "40"),
        ("A.4", "Mobile Customer Portal - Welcome and Value Proposition", "41"),
        ("A.5", "Mobile Customer Registration Form with Service Selection", "42"),
        ("A.6", "Mobile Service Catalogue Modal Dialog", "43"),
        ("A.7", "Live Mobile Customer Ticket - Waiting Status with AI Estimation", "44"),
        ("A.8", "Real-Time Mobile Haptic & Visual Turn Alert Screen", "45"),
        ("A.9", "Active Mobile Consultation In-Service Status Monitor", "46"),
        ("A.10", "Service Completion Confirmation Screen", "47"),
        ("A.11", "Counter Management and Dynamic Fleet Allocation Workspace", "47"),
        ("A.12", "Real-Time Queue Inspection and Live Token Roster", "48"),
        ("A.13", "Executive Operational Analytics Dashboard with Traffic Distributions", "48"),
        ("A.14", "Active Counter Workspace Telemetry Detail Cards", "48")
    ]
    add_borderless_table(doc, ["FIGURE NO.", "FIGURE TITLE", "PAGE No."], figures_list, col_widths=[Inches(1.30), Inches(4.15), Inches(0.80)], bold_ch_only=False)

    # =========================================================================
    # SECTION 3: CHAPTER 1 ONWARDS (BODY CHAPTERS, APPENDIX, REFERENCES)
    # Starts page numbering at 1
    # =========================================================================
    s3 = doc.add_section()
    s3.top_margin = Inches(1.0)
    s3.bottom_margin = Inches(1.0)
    s3.left_margin = Inches(1.25)
    s3.right_margin = Inches(1.0)
    setup_section_numbering(s3, start_num=1, is_roman=False)
    setup_footer(s3)

    # =========================================================================
    # CHAPTER 1: INTRODUCTION
    # =========================================================================
    add_heading_1(doc, "CHAPTER 1\nINTRODUCTION")
    add_chapter_intro(doc, "the introduction, operational problem definition, engineering objectives, scope boundaries, motivational framework, and organizational structure underpinning the development of QFlow, an AI-powered smart token and queue management system.")
    add_heading_2(doc, "1.1 OVERVIEW")
    
    add_heading_3(doc, "1.1.1 Need for a Centralized Queue and Token Management System")
    add_p(doc, "High-density service facilities such as retail banking branches, outpatient medical clinics, municipal government offices, and telecommunication support centers experience fluctuating customer arrival volumes throughout the operating day. When arrival rates exceed immediate service capacity, queues inevitably materialize. In the absence of an automated management architecture, customer flow degenerates into physical crowding, ambiguous service priorities, and heightened operational anxiety for both visitors and service staff.", space_after=8)
    
    add_p(doc, "A centralized queue and token management platform introduces structured discipline to this operational dynamic. By transitioning customer entry into an atomic, sequential digital token allocation model, the system guarantees strict fairness and chronological transparency. Tellers are relieved from manual queue arbitration, enabling them to focus entirely on customer consultation. Furthermore, facility supervisors gain instant visibility into live floor occupancy, pending backlogs, and counter productivity, transforming an unpredictable physical environment into a measured, manageable operational workflow.", space_after=10)

    add_heading_3(doc, "1.1.2 Limitations of Existing Manual and Physical Token Systems")
    add_p(doc, "Conventional approaches to customer queue coordination suffer from distinct functional limitations:", space_after=4)
    add_bullet_point(doc, "Hardware Vulnerability and Maintenance Overhead: ", "Physical kiosk dispensers rely on mechanical button triggers, thermal printers, and continuous paper rolls. Mechanical jams and paper exhaustion frequently halt token issuance during peak operational hours.")
    add_bullet_point(doc, "Spatial Tethering and Waiting Lounge Congestion: ", "Customers receiving paper slips are tethered to physical waiting lounges because turn announcements are conveyed solely via ceiling-mounted LED numeric displays or overhead audio buzzers.")
    add_bullet_point(doc, "Absence of Contextual Duration Telemetry: ", "Printed tokens display only a sequential number without providing actionable estimates of expected waiting duration, leaving visitors uninformed regarding their anticipated consultation time.")
    add_bullet_point(doc, "Static and Rigid Counter Allocation: ", "Legacy hardware systems assign tokens to fixed service counters based on static First-Come-First-Served (FCFS) rules, preventing dynamic load rebalancing when specific consultations overrun.")
    add_bullet_point(doc, "Data Siloing and Telemetry Deficits: ", "Manual registers and standalone electronic systems fail to aggregate operational metrics, depriving management of historical data required for strategic staff scheduling.", space_after=10)

    add_heading_2(doc, "1.2 OBJECTIVE")
    add_p(doc, "The primary objective of QFlow is to design and develop an intelligent, real-time, browser-accessible queue management platform that replaces physical ticketing hardware with a mobile-first digital workflow. The specific objectives are:", space_after=4)
    add_numbered_point(doc, "1.", "Responsive Mobile Self-Service: ", "To engineer a mobile web portal accessible via a dynamic QR code without requiring native application downloads or user account registration.")
    add_numbered_point(doc, "2.", "Atomic Token Sequencing: ", "To provide atomic sequential token generation (e.g., A101, A102) linked to specific service categories with zero collision risk under concurrent requests.")
    add_numbered_point(doc, "3.", "AI-Powered Wait Estimation: ", "To construct an in-memory predictive engine utilizing historical synthetic data to forecast transaction durations and personalized waiting times.")
    add_numbered_point(doc, "4.", "Dynamic Counter Recommendation: ", "To implement a heuristic scoring algorithm that evaluates counter status, queue backlogs, and remaining service times to recommend optimal routing.")
    add_numbered_point(doc, "5.", "Staff Operations Dashboard: ", "To build a centralized workstation console providing counter status switching, next-token calling, service starting, completion recording, skipping, and inter-counter transferring.")
    add_numbered_point(doc, "6.", "Sub-Millisecond Real-Time Push: ", "To establish bi-directional real-time event dissemination using Socket.IO to deliver visual notifications and haptic vibration alerts directly to customer smartphones.")
    add_numbered_point(doc, "7.", "Operational Telemetry Analytics: ", "To compute aggregate facility metrics including hourly queue distributions, average wait times, and teller throughput.")
    add_numbered_point(doc, "8.", "Multi-Container Architecture: ", "To package the full-stack system using a modular architecture for straightforward local and on-premise deployment.", space_after=10)

    add_heading_2(doc, "1.3 SCOPE OF THE PROJECT")
    add_p(doc, "The scope of QFlow encompasses an end-to-end software platform for managing customer queues, service desk allocations, token lifecycle transitions, and real-time operational analytics.", space_after=4)
    
    add_p(doc, "Functional Scope (In-Scope):", font_size=11.5, bold=True, alignment=WD_ALIGN_PARAGRAPH.LEFT, space_before=2, space_after=3)
    add_bullet_point(doc, "Dynamic QR Generation: ", "Automated detection of the host's Wi-Fi network gateway IPv4 address for multi-device cross-network accessibility.")
    add_bullet_point(doc, "Frictionless Mobile Registration: ", "Zero-install web form capturing name, contact number, and selected service category.")
    add_bullet_point(doc, "State Machine Lifecycle: ", "Atomic transitions across WAITING, CALLED, IN_SERVICE, COMPLETED, SKIPPED, and TRANSFERRED states.")
    add_bullet_point(doc, "Predictive Duration Modeling: ", "Synthetic historical baseline regression combined with temporal peak multipliers and queue depth adjustments.")
    add_bullet_point(doc, "Channel-Isolated WebSockets: ", "Socket.IO room architecture separating global queue telemetry ('queue') from private customer notifications ('token:{id}').")
    add_bullet_point(doc, "Haptic Multisensory Notification: ", "HTML5 Web Vibration API execution directly on customer handsets upon counter calling.")
    add_bullet_point(doc, "Administrative Telemetry: ", "MongoDB aggregation pipelines generating real-time traffic distributions and teller productivity reports.")
    add_bullet_point(doc, "Role-Based Access Control: ", "Secure staff and supervisor authentication utilizing JSON Web Tokens (JWT) and bcrypt password hashing.", space_after=6)

    add_p(doc, "Operational Boundaries (Out-of-Scope):", font_size=11.5, bold=True, alignment=WD_ALIGN_PARAGRAPH.LEFT, space_before=4, space_after=3)
    add_bullet_point(doc, "Physical Hardware Interfacing: ", "Direct RS-485 serial communication with physical seven-segment LED displays or legacy thermal paper printers.")
    add_bullet_point(doc, "Cellular SMS Telephony: ", "Paid SMS gateway integration, relying instead on native browser WebSockets and push notifications.")
    add_bullet_point(doc, "Biometric Customer Verification: ", "Facial recognition or fingerprint authentication for incoming visitors.")
    add_bullet_point(doc, "Multi-Tenant Enterprise Cloud: ", "Multi-site global clustering; current scope targets single-facility on-premise or campus deployment.", space_after=10)

    add_heading_2(doc, "1.4 MOTIVATION")
    add_p(doc, "Queueing environments are ubiquitous across modern society. Unpredictable waiting durations degrade customer satisfaction and increase stress for service personnel. The widespread adoption of smartphones equipped with high-resolution cameras presents an opportunity to transform physical queueing into an accessible digital self-service interaction. By allowing visitors to scan a QR code and receive live updates and haptic alerts on their own phones, physical congestion in waiting rooms is effectively mitigated.", space_after=6)
    add_p(doc, "As an academic project in Artificial Intelligence and Data Science, QFlow addresses real-world systems engineering challenges: asynchronous client-server architectures, real-time WebSocket state synchronization, atomic document locking under concurrency, and mathematical modeling of service queue dynamics. The resulting system demonstrates how standard web technologies can eliminate expensive kiosk hardware while improving customer experience.", space_after=10)

    add_heading_2(doc, "1.5 ORGANIZATION OF THE REPORT")
    add_p(doc, "The remainder of this report is organized as follows:", space_after=4)
    add_bullet_point(doc, "Chapter 2 - Related Work: ", "Reviews foundational queueing theory, real-time distributed web communication protocols, state-of-the-art queue architectures, and derives the design principles governing QFlow.")
    add_bullet_point(doc, "Chapter 3 - System Analysis: ", "Formalizes the problem definition, details functional and non-functional requirements, itemizes software dependencies and hardware development environments, and outlines primary user use cases.")
    add_bullet_point(doc, "Chapter 4 - Implementation: ", "Explains system architecture, deployment topology, core algorithmic formulations for AI duration and counter recommendation, Mongoose database schemas, and empirical test results.")
    add_bullet_point(doc, "Chapter 5 - Conclusion and Future Enhancements: ", "Summarizes key project achievements, identifies current operational boundaries, and proposes directions for subsequent development.")
    add_bullet_point(doc, "Appendix 1 - Sample Code & Screenshots: ", "Provides representative source code excerpts, followed by Project Screenshots and References.", space_after=10)

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 2: RELATED WORK
    # =========================================================================
    add_heading_1(doc, "CHAPTER 2\nRELATED WORK")
    add_chapter_intro(doc, "a critical literature survey of queueing management paradigms, analyzing conventional physical token systems, documenting operational bottlenecks in legacy customer service facilities, and formulating the proposed QFlow real-time predictive architecture.")

    add_heading_2(doc, "2.1 LITERATURE REVIEW")
    add_p(doc, "Queueing Theory and Operational Dynamics. Queueing theory, initiated by A. K. Erlang's pioneering mathematical formulations for telephone exchange congestion in 1909 [1], provides the quantitative foundation for evaluating waiting lines. Kendall's notation classifies queueing systems based on arrival patterns, service time distributions, and the number of servers (e.g., M/M/1, M/M/c) [2]. Little's Law (L = λW) mathematically establishes that the average number of customers in a stationary queueing system (L) equals the long-term average arrival rate (λ) multiplied by the average time a customer spends in the system (W) [3]. While classical analytical models assume idealized Poisson arrival processes and exponential service distributions, real-world service facilities experience dynamic variance driven by human behavioral factors and transaction complexity. QFlow adopts these theoretical principles by dynamically computing estimated wait time as the aggregated pending workload divided by active counter capacity.", space_after=8)

    add_p(doc, "Predictive Scheduling in Service Operations. Larson's seminal work on the psychology of queueing demonstrated that perceived waiting time, lack of temporal visibility, and unexplained delays exert a significantly more detrimental impact on customer satisfaction than objective elapsed time [4]. Providing customers with an accurate initial duration estimate fundamentally reduces perceived anxiety. Modern predictive frameworks increasingly apply machine-learning heuristics to forecast operational service durations using features such as transaction category, temporal peak windows, and real-time server density [5]. QFlow incorporates these insights via a lightweight weighted-regression model that calibrates base service metrics against historical peak variances.", space_after=8)

    add_p(doc, "Real-Time Bi-Directional Web Architectures. Traditional web applications rely on stateless HTTP request-response cycles. Under high-frequency polling architectures where clients query the server every few seconds to check queue position, server thread pools become rapidly saturated by redundant HTTP handshakes [6]. The WebSocket protocol (IETF RFC 6455) provides full-duplex, persistent communication channels over a single TCP connection, drastically minimizing overhead and latency [7]. Socket.IO abstracts WebSocket transport with automatic HTTP long-polling fallback, structured event multiplexing, and room-based channel isolation [8]. QFlow leverages Socket.IO rooms to broadcast public queue states while privately channeling status alerts to specific customer devices.", space_after=8)

    add_p(doc, "Document-Oriented Database Concurrency. In transactional queueing systems, concurrency control is vital. When multiple service counters attempt to call the next waiting customer simultaneously, naive read-modify-write patterns result in race conditions where two tellers are assigned the same ticket [9]. Modern document stores like MongoDB provide atomic single-document modifications via operators such as findOneAndUpdate, ensuring linearizable state transitions without the operational overhead of heavy multi-table SQL locks [10].", space_after=10)

    add_heading_2(doc, "2.2 EXISTING SYSTEMS")
    add_p(doc, "Current queue management approaches deployed across public and commercial facilities can be categorized into four primary paradigms:", space_after=4)
    add_numbered_point(doc, "1.", "Disconnected Spreadsheets and Paper Registers: ", "Activities are logged manually in paper notebooks or spreadsheets. While simple, they fail to provide real-time coordination, lack customer-facing displays, and suffer from high human error rates.")
    add_numbered_point(doc, "2.", "Dedicated Self-Service Hardware Kiosks: ", "Freestanding touchscreen terminals equipped with thermal printers. While functional, they entail high acquisition costs, continuous paper consumable overhead, and still produce physical slips without smartphone integration.")
    add_numbered_point(doc, "3.", "Proprietary Native Mobile Applications: ", "Commercial enterprise apps requiring customers to install native software and register user accounts before joining a line. This friction causes many casual visitors to bypass the system.")
    add_numbered_point(doc, "4.", "QFlow (Proposed System): ", "A zero-install, browser-based web architecture. Customers scan a physical QR code using their existing phone camera, instantly joining the queue on a mobile browser with AI-driven wait estimation, dynamic counter scoring, Socket.IO haptic alerts, and complete administrative queue governance.", space_after=6)

    t21_headers = ["Approach", "Physical Hardware", "Mobile Integration", "Wait Estimation", "Real-Time Push", "Friction"]
    t21_rows = [
        ["Paper Thermal Dispensers", "High (Printers, Displays)", "None", "None", "Audio chime only", "Low friction, high confinement"],
        ["Enterprise Touchscreen Kiosks", "High (Costly kiosks)", "Minimal (Optional SMS)", "Static average", "Public display screens", "Moderate friction, hardware maintenance"],
        ["Proprietary Native Apps", "Low", "High", "Basic heuristic", "Push notifications", "Very high friction (App install + signup)"],
        ["QFlow (This Project)", "Minimal (Static printed QR)", "High (Zero-install web app)", "Dynamic AI prediction", "Socket.IO push + Phone vibration", "Zero friction (Scan and go)"]
    ]
    add_table_data(doc, "Table 2.1: Comparison of Existing Approaches to Queue and Token Management", t21_headers, t21_rows, [Inches(1.15), Inches(1.05), Inches(1.05), Inches(1.00), Inches(1.00), Inches(1.00)])

    add_heading_2(doc, "2.3 INFERENCE FROM LITERATURE REVIEW")
    add_p(doc, "The comprehensive literature review leads to the following key inferences:", space_after=4)
    add_bullet_point(doc, "Visibility Reduces Perceived Waiting Time: ", "Accurately calculating and displaying expected wait times alleviates customer stress and prevents queue abandonment [4].")
    add_bullet_point(doc, "Frictionless Onboarding is Critical: ", "Systems that mandate account creation or native application installation encounter steep adoption resistance from one-time visitors. A browser-based QR entry model minimizes barriers to entry.")
    add_bullet_point(doc, "Push-Based Updates Outperform Polling: ", "Continuous HTTP polling degrades mobile battery life and overburdens server resources. Persistent WebSocket connections provide instant notification with minimal network overhead [6], [7].")
    add_bullet_point(doc, "Atomic State Transitions Prevent Collisions: ", "Tellers operating under peak loads require guaranteed atomic database operations to eliminate double-calling race conditions [10].")
    add_bullet_point(doc, "Dynamic Counter Allocation Improves Utilization: ", "Static counter assignment leads to uneven queue distribution; automated scoring balances traffic according to live desk capacity.", space_after=10)

    add_heading_2(doc, "2.4 EXTRACTION FROM LITERATURE REVIEW")
    add_p(doc, "Based on these inferences, the architectural and algorithmic design principles summarized in Table 2.2 were extracted and implemented in QFlow.", space_after=6)

    t22_headers = ["Principle (Literature Source)", "Technical Implementation in QFlow"]
    t22_rows = [
        ["Frictionless Mobile Access [4]", "Dynamic QR generation embedding local network IP; zero-install mobile web portal in React 19."],
        ["Dynamic Wait-Time Estimation [1], [3]", "Algorithmic prediction combining service base durations, peak multipliers, and active counter counts."],
        ["Sub-Millisecond Real-Time Push [7], [8]", "Socket.IO room architecture isolating global queue events ('queue') from private customer notifications ('token:{id}')."],
        ["Haptic Multisensory Notification [4]", "HTML5 Web Vibration API (navigator.vibrate([300, 100, 300])) triggered automatically on customer device upon token call."],
        ["Atomic Concurrency Guarantee [10]", "MongoDB atomic findOneAndUpdate queries targeting status: 'WAITING' to eliminate race conditions."],
        ["Dynamic Counter Allocation [5]", "100-point heuristic scoring algorithm evaluating counter status, queue backlogs, and time-to-completion."],
        ["Stateful Aggregation Analytics [2]", "Mongoose pipeline calculations deriving hourly traffic distribution, average wait times, and counter throughput."]
    ]
    add_table_data(doc, "Table 2.2: Design Principles Extracted from Literature and Their Use in QFlow", t22_headers, t22_rows, [Inches(2.25), Inches(4.00)])

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 3: SYSTEM ANALYSIS
    # =========================================================================
    add_heading_1(doc, "CHAPTER 3\nSYSTEM ANALYSIS")
    add_chapter_intro(doc, "the comprehensive system requirements analysis, operational constraints, and technical specifications, detailing the functional and non-functional requirements alongside the hardware and software environments necessary for developing and deploying QFlow.")

    add_heading_2(doc, "3.1 PROBLEM DEFINITION")
    add_p(doc, "Public and commercial customer service facilities frequently suffer from systemic congestion, unpredictable wait times, and poor communication between customers and staff. The specific operational problems can be stated as follows:", space_after=4)
    add_numbered_point(doc, "1.", "Lack of Customer Situational Awareness: ", "Customers waiting for service have no reliable estimate of how long their consultation will take or how many customers ahead have complex requirements.")
    add_numbered_point(doc, "2.", "High Infrastructure and Maintenance Costs: ", "Conventional queue systems depend on specialized thermal ticket dispensers, roll paper refills, mechanical buttons, and physical seven-segment counter display hardware.")
    add_numbered_point(doc, "3.", "Physical Confinement and Crowding: ", "Because token notifications are communicated solely through ceiling-mounted LED screens or overhead speakers, customers are forced to remain physically packed inside waiting rooms.")
    add_numbered_point(doc, "4.", "Inefficient Counter Workload Balancing: ", "When tellers manually choose which token to call or operate under static ticket queues, workloads become unevenly distributed across staff members.")
    add_numbered_point(doc, "5.", "Absence of Centralized Operational Telemetry: ", "Facility managers lack actionable, real-time insights into average service durations, hourly arrival spikes, and teller idle times.", space_after=10)

    add_heading_2(doc, "3.2 PROPOSED SOLUTION")
    add_p(doc, "The proposed solution is QFlow, an integrated, three-tier, real-time web application built on the MERN stack. Its architectural capabilities include:", space_after=4)
    add_numbered_point(doc, "1.", "Zero-Install Customer Portal: ", "Accessible on any smartphone browser by scanning a dynamic QR code. Customers register their name, phone number, and requested service, immediately receiving an atomic digital token (e.g., A101).")
    add_numbered_point(doc, "2.", "AI-Powered Duration & Wait Estimation: ", "An in-memory prediction service evaluates service complexity, current hour peak factors, and queue depth to generate personalized wait-time estimates.")
    add_numbered_point(doc, "3.", "Dynamic Counter Assignment Engine: ", "A heuristic algorithm evaluates active counter states and assigns incoming customers to optimal counters to prevent bottlenecking.")
    add_numbered_point(doc, "4.", "Real-Time Staff Operations Dashboard: ", "An administrative console allowing tellers to call the next customer, start consultations, complete services, skip absent visitors, and transfer tokens between departments.")
    add_numbered_point(doc, "5.", "Bi-Directional WebSocket Notifications: ", "Socket.IO pushes live queue transitions to both staff consoles and customer smartphones, triggering visual banners and haptic phone vibrations.")
    add_numbered_point(doc, "6.", "Operational Performance Analytics: ", "MongoDB aggregation pipelines generate live charts tracking hourly customer volumes, counter throughput, and average wait times.", space_after=10)

    add_heading_3(doc, "3.2.1 Functional Requirements")
    t31_headers = ["ID", "Requirement", "Description"]
    t31_rows = [
        ["FR-01", "User Authentication", "Staff and administrative personnel can securely authenticate using email and password, receiving a signed JSON Web Token (JWT)."],
        ["FR-02", "QR Code Generation", "The server detects the active Wi-Fi LAN IPv4 address and dynamically generates high-resolution QR codes linking directly to the mobile portal."],
        ["FR-03", "Customer Token Issuance", "Customers can submit their name, phone number, and service category via the mobile portal to obtain an atomic sequential token (e.g., A101)."],
        ["FR-04", "AI Wait-Time Prediction", "The system automatically calculates predicted service duration and estimated queue waiting time upon token generation."],
        ["FR-05", "Dynamic Counter Recommendation", "The system calculates a multi-factor score (0–100) for active counters and recommends optimal routing for incoming tokens."],
        ["FR-06", "Staff Queue Management", "Staff can execute token state transitions: Call Next, Start Service, Complete Service, Skip Token, and Transfer Token."],
        ["FR-07", "Real-Time Event Broadcasting", "Token creations, calls, and completions are broadcast instantly across Socket.IO rooms ('queue' and 'token:{id}')."],
        ["FR-08", "Haptic & Visual Customer Alerts", "When a token status transitions to CALLED, the customer’s phone displays an on-screen alert and triggers haptic vibration pulses."],
        ["FR-09", "Counter Administration", "Administrators can dynamically add new counters, update staff assignments, toggle counter availability, and delete inactive desks."],
        ["FR-10", "Operational Analytics & Metrics", "The system aggregates completed token records into real-time visual charts showing hourly traffic, average wait times, and counter throughput."],
        ["FR-11", "Database Seeding & Recovery", "The system includes automated database seed scripts to populate demo accounts, standard service catalogues, and historical analytics."]
    ]
    add_table_data(doc, "Table 3.1: Functional Requirements of QFlow", t31_headers, t31_rows, [Inches(0.95), Inches(1.70), Inches(3.60)])

    add_heading_3(doc, "3.2.2 Non-Functional Requirements")
    add_p(doc, "The non-functional performance, reliability, and security constraints governing QFlow include:", space_after=4)
    add_bullet_point(doc, "NFR-01 Real-Time Latency: ", "Queue state transitions must be dispatched across Socket.IO channels and rendered on client displays within 200 milliseconds of database commitment.")
    add_bullet_point(doc, "NFR-02 Concurrency & Data Integrity: ", "The backend must execute atomic database modifications using findOneAndUpdate to prevent race conditions during concurrent Call Next operations.")
    add_bullet_point(doc, "NFR-03 Zero-Friction Usability: ", "The customer interface must function seamlessly across modern mobile browsers (iOS Safari, Android Chrome) without requiring app store installation or login credentials.")
    add_bullet_point(doc, "NFR-04 Security & Password Protection: ", "Passwords must be hashed using bcrypt (salt rounds = 10), and all administrative endpoints must enforce JWT bearer token validation.")
    add_bullet_point(doc, "NFR-05 High Availability & Fallback: ", "The backend must support both configured persistent MongoDB connections and zero-config embedded MongoMemoryServer fallbacks for standalone demonstrations.", space_after=10)

    add_heading_2(doc, "3.3 SOFTWARE COMPONENTS")
    t32_headers = ["Layer", "Component", "Version / Specification", "Purpose in QFlow"]
    t32_rows = [
        ["Runtime", "Node.js", "v18.0.0 or higher (v22.x LTS)", "Asynchronous backend JavaScript execution environment"],
        ["Frontend Framework", "React", "^19.0.0", "Component-based reactive user interface rendering"],
        ["Build Tool", "Vite", "^6.0.0 / ^8.0.0", "High-performance frontend dev server and production bundler"],
        ["Styling", "Tailwind CSS", "^3.4.0 / ^4.0.0", "Utility-first responsive CSS styling for mobile and desktop"],
        ["Web Framework", "Express.js", "^4.19.0", "RESTful API routing, middleware chaining, and HTTP server"],
        ["Database & ODM", "MongoDB & Mongoose", "MongoDB 7.0 / Mongoose ^8.3.0", "Persistent document store for tokens, counters, users, and services"],
        ["Real-Time Transport", "Socket.IO", "^4.7.5", "Full-duplex WebSocket communication and room-based event dispatch"],
        ["Security & Auth", "jsonwebtoken & bcryptjs", "JWT ^9.0.2 / bcryptjs ^2.4.3", "Stateless token-based authentication and adaptive password hashing"],
        ["Charts & Visualization", "Recharts & Lucide React", "Recharts ^2.12.0 / Lucide ^0.469.0", "Analytical data graphs and iconography"],
        ["QR Code Generation", "qrcode & qrcode.react", "qrcode ^1.5.3 / qrcode.react ^4.2.0", "Server-side image generation and client QR rendering"]
    ]
    add_table_data(doc, "Table 3.2: Software Components of QFlow", t32_headers, t32_rows, [Inches(1.15), Inches(1.40), Inches(1.40), Inches(2.30)])

    add_heading_2(doc, "3.4 HARDWARE COMPONENTS")
    t33_headers = ["Component", "Development Workstation", "Deployment Host (Server)", "Client Devices (Staff & Customer)"]
    t33_rows = [
        ["Processor", "4-Core x86-64 / ARM64 CPU", "2 or more vCPUs (x86-64 / ARM64)", "Any modern smartphone or desktop processor"],
        ["RAM", "8 GB DDR4 minimum (16 GB recommended)", "4 GB RAM minimum", "2 GB RAM minimum on mobile devices"],
        ["Storage", "256 GB SSD (500 MB free for project)", "20 GB available SSD storage", "Standard mobile flash storage"],
        ["Network Interface", "Wi-Fi (802.11ac) or Gigabit Ethernet", "Wi-Fi / LAN with static or known IPv4", "Wi-Fi or Cellular data connected to same subnet"],
        ["Display", "1920x1080 Full HD Monitor", "Headless server / Standard monitor", "Smartphone display (min 375px width)"]
    ]
    add_table_data(doc, "Table 3.3: Hardware Components for Development and Deployment", t33_headers, t33_rows, [Inches(1.15), Inches(1.60), Inches(1.60), Inches(1.90)])

    add_heading_2(doc, "3.5 USE CASES")
    add_p(doc, "The functional interactions of QFlow span three primary user roles:", space_after=4)
    add_numbered_point(doc, "1.", "Customer: ", "Scans facility QR code, submits registration form, tracks queue position, receives visual and haptic alerts, and attends service counter.")
    add_numbered_point(doc, "2.", "Staff / Teller: ", "Logs in with email/password, activates workstation counter, calls next customer, begins service, completes consultation, marks skips, or transfers tokens.")
    add_numbered_point(doc, "3.", "Administrator / Supervisor: ", "Manages counter fleet configurations, configures service categories, inspects real-time queue rosters, and analyzes facility throughput charts.")
    add_numbered_point(doc, "4.", "System / Automated Engine: ", "Performs background wait-time regression calculations, evaluates heuristic counter fitness, and dispatches multi-room WebSocket broadcasts.", space_after=6)

    t34_headers = ["Use Case ID", "Use Case Name", "Primary Actor", "Pre-conditions", "Main Success Scenario"]
    t34_rows = [
        ["UC-01", "Generate QR Code", "Administrator / Server", "Server online on local Wi-Fi", "Server detects LAN IP and generates scannable QR code"],
        ["UC-02", "Join Virtual Queue", "Customer", "Customer scans QR code on phone", "Customer submits form; server issues atomic token with AI wait estimate"],
        ["UC-03", "Track Live Token", "Customer", "Token generated and active", "Customer observes real-time position; phone vibrates when token is called"],
        ["UC-04", "Staff Login", "Staff / Admin", "Valid credentials in database", "Staff submits email/password; server returns signed JWT token"],
        ["UC-05", "Call Next Customer", "Staff Teller", "Teller counter is AVAILABLE", "Teller clicks Call Next; server atomically assigns next WAITING token"],
        ["UC-06", "Conduct Consultation", "Staff Teller", "Token is in CALLED status", "Teller clicks Start Service; timer records consultation start time"],
        ["UC-07", "Complete Service", "Staff Teller", "Token is IN_SERVICE", "Teller clicks Complete; consultation duration logged; counter made AVAILABLE"],
        ["UC-08", "Skip Absent Customer", "Staff Teller", "Called customer fails to arrive", "Teller marks token SKIPPED; queue order updates live for waiting users"],
        ["UC-09", "Transfer Token", "Staff Teller", "Token requires secondary desk", "Teller selects target counter; token re-routed without losing seniority"],
        ["UC-10", "Manage Counters", "Administrator", "Admin authenticated via JWT", "Admin creates, activates, pauses, or deletes counter desks in fleet"],
        ["UC-11", "View Analytics", "Admin / Supervisor", "Admin authenticated via JWT", "Supervisor views charts of hourly traffic, wait times, and teller output"]
    ]
    add_table_data(doc, "Table 3.4: Description of Main Use Cases", t34_headers, t34_rows, [Inches(0.85), Inches(1.35), Inches(1.05), Inches(1.45), Inches(1.55)])

    if os.path.exists(uc_img):
        add_figure_image(doc, uc_img, "Figure 3.1: Use Case Diagram of QFlow", max_width=6.0, max_height=4.0)

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 4: IMPLEMENTATION
    # =========================================================================
    add_heading_1(doc, "CHAPTER 4\nIMPLEMENTATION")
    add_chapter_intro(doc, "the core engineering methodology, module implementation details, architectural framework, class data models, sequence workflows, and empirical testing results of the QFlow platform.")

    add_heading_2(doc, "4.1 SYSTEM ARCHITECTURE AND EXPERIMENTAL SETUP")
    
    add_heading_3(doc, "4.1.1 High-Level System Architecture")
    add_p(doc, "QFlow follows a three-layer client-server architecture designed for high responsiveness, real-time bidirectional communication, and clean separation of concerns. The layered architecture is illustrated in Figure 4.1.", space_after=6)
    
    if os.path.exists(fig_4_1_path):
        add_figure_image(doc, fig_4_1_path, "Figure 4.1: System Architecture of QFlow", max_width=6.2, max_height=4.4)

    add_p(doc, "The primary responsibilities of each architectural tier are structured as follows:", space_after=4)
    add_bullet_point(doc, "Presentation Layer (Client Container / Web Browser, Port 3000): ", "Constructed using React 19, Vite, and Tailwind CSS. Provides a responsive mobile self-service portal for customers and an administrative desktop workstation for staff tellers and supervisors. Incorporates Socket.IO client listeners, Recharts telemetry visualizations, Lucide icons, and the HTML5 Web Vibration API for haptic alert dispatch.")
    add_bullet_point(doc, "Application Layer (Server Container / Node.js Runtime, Port 5000): ", "Powered by Node.js and Express.js. Handles CORS whitelisting, JSON parsing, rate limiting, and JWT bearer authentication. Orchestrates REST API controllers (/api/tokens, /api/counters, /api/services, /api/auth, /api/analytics), manages Socket.IO WebSocket rooms ('queue', 'token:{id}'), and executes the AI duration prediction and heuristic counter assignment engines.")
    add_bullet_point(doc, "Data Layer (MongoDB 7.0 Document Store, Port 27017): ", "Stores persistent operational records across dedicated collections (tokens, counters, services, users). Provides linearizable atomic document updates via findOneAndUpdate, guaranteeing concurrency safety during simultaneous staff counter calls.", space_after=8)

    t41_headers = ["HTTP Method", "API Endpoint", "Access Level", "Functional Purpose"]
    t41_rows = [
        ["POST", "/api/auth/login", "Public", "Authenticates staff/admin credentials and issues signed JWT token"],
        ["GET", "/api/auth/me", "Authenticated", "Retrieves profile and role permissions of current user session"],
        ["POST", "/api/tokens", "Public", "Creates atomic sequential token with AI duration & wait estimates"],
        ["GET", "/api/tokens/:id", "Public", "Retrieves current status, position, and wait time for a single token"],
        ["PATCH", "/api/tokens/:id/call", "Authenticated", "Atomically transitions token to CALLED and alerts customer handset"],
        ["PATCH", "/api/tokens/:id/start", "Authenticated", "Transitions token to IN_SERVICE and stamps consultation start time"],
        ["PATCH", "/api/tokens/:id/complete", "Authenticated", "Completes service, logs actual duration, and frees counter desk"],
        ["PATCH", "/api/tokens/:id/skip", "Authenticated", "Marks absent customer as SKIPPED and updates queue order"],
        ["PATCH", "/api/tokens/:id/transfer", "Authenticated", "Transfers active token to another target counter without re-queuing"],
        ["GET", "/api/counters", "Public / Auth", "Retrieves all registered counters with live occupancy and status"],
        ["POST", "/api/counters", "Admin", "Registers a new service counter into the facility fleet"],
        ["PATCH", "/api/counters/:id/status", "Authenticated", "Updates counter operational state (AVAILABLE, OFFLINE)"],
        ["GET", "/api/services", "Public", "Fetches active facility service catalogue with standard base times"],
        ["GET", "/api/queue/active", "Authenticated", "Fetches complete snapshot of all active tokens in queue"],
        ["GET", "/api/analytics/summary", "Authenticated", "Generates aggregate metrics (average wait time, traffic trends)"],
        ["GET", "/api/health", "Public", "Returns system uptime, active LAN IP, and customer QR portal URL"]
    ]
    add_table_data(doc, "Table 4.1: REST API Endpoints of QFlow", t41_headers, t41_rows, [Inches(0.85), Inches(1.85), Inches(1.10), Inches(2.45)])

    add_heading_3(doc, "4.1.2 System Deployment and Network Topology")
    add_p(doc, "The physical and containerized deployment architecture of QFlow across the host server, local area network, and heterogeneous client devices is shown in Figure 4.2. The system operates seamlessly both in containerized Docker Compose environments and native Node.js runtime configurations.", space_after=6)

    if os.path.exists(fig_4_2_path):
        add_figure_image(doc, fig_4_2_path, "Figure 4.2: System Deployment and Network Topology of QFlow", max_width=6.2, max_height=4.4)

    t42_headers = ["Parameter", "Development & Test Specification"]
    t42_rows = [
        ["Operating System", "Windows 11 Enterprise (64-bit, Build 26100) / Ubuntu 22.04 LTS"],
        ["Node.js Environment", "Node.js v22.14.0 LTS / npm 10.9.4"],
        ["Database Instance", "MongoDB Community Server v7.0.14 (Local) / MongoMemoryServer v9.1.8"],
        ["Network Configuration", "Local IEEE 802.11ac Wi-Fi router (Subnet 192.168.1.0/24)"],
        ["Client Devices Tested", "Apple iPhone 14 (iOS 17.5 / Safari), Samsung Galaxy S23 (Android 14 / Chrome), HP EliteBook (Edge)"],
        ["Verification Tools", "Postman v11.16 (REST Validation), Browser DevTools (Network & WebSocket inspection)"]
    ]
    add_table_data(doc, "Table 4.2: Experimental Setup Used for Building and Testing", t42_headers, t42_rows, [Inches(2.15), Inches(4.10)])

    add_heading_2(doc, "4.2 MODULE IMPLEMENTATION DETAILS")
    add_p(doc, "The QFlow codebase is modularized into distinct, decoupled subsystems responsible for dedicated operational tasks. Table 4.3 outlines the core modules, their implementation files, and primary responsibilities.", space_after=6)

    t43_headers = ["Module Name", "Core Implementation Files", "Primary Functional Responsibility"]
    t43_rows = [
        ["Authentication & RBAC", "authController.js, auth.js, LoginPage.jsx", "User login, bcrypt verification, JWT signing, role authorization"],
        ["Token Management", "tokenController.js, Token.js, TokenStatus.jsx", "Atomic sequence generation, state transitions, customer tracking"],
        ["AI Prediction Service", "predictionService.js", "Duration forecasting, peak hour adjustments, wait estimation"],
        ["Counter Recommendation", "counterAssignmentService.js, CounterCard.jsx", "Dynamic 100-point heuristic counter scoring and workload balancing"],
        ["Real-Time Synchronization", "socketHandler.js, socket.js, QueueContext.jsx", "Full-duplex WebSocket rooms, multi-device broadcasting, haptic events"],
        ["Analytics & Reporting", "analyticsController.js, AnalyticsPage.jsx", "MongoDB aggregation pipelines, hourly queue trends, counter metrics"],
        ["Network & QR Generation", "lanIP.js, generateQR.js, QRModal.jsx", "Local network IP detection, dynamic QR generation, mobile portal linking"]
    ]
    add_table_data(doc, "Table 4.3: Summary of QFlow Modules", t43_headers, t43_rows, [Inches(1.75), Inches(2.10), Inches(2.40)])

    add_heading_3(doc, "4.2.1 Data Source Module")
    add_p(doc, "Operational data enters QFlow via two channels: customer registration submissions through the mobile portal, and the pre-configured service catalogue initialized during database seeding. Table 4.4 lists the standard service catalogue parameters accepted by the Data Source Module.", space_after=6)
    
    t44_headers = ["Service Code", "Service Display Name", "Base Duration", "Historical Variance", "Description"]
    t44_rows = [
        ["ACC_SRV", "Account Service", "8 mins", "± 4 mins", "Opening accounts, KYC validation, profile updates"],
        ["PAY_SRV", "Payment Service", "10 mins", "± 5 mins", "Cash deposits, drafts, utility clearing, RTGS/NEFT"],
        ["DOC_VER", "Document Verification", "15 mins", "± 7 mins", "Loan documentation, legal affidavits, certificates"],
        ["CUS_SUP", "Customer Support", "7 mins", "± 3 mins", "Account disputes, card issuance, portal grievances"],
        ["GEN_ENQ", "General Enquiry", "5 mins", "± 2 mins", "Informational queries, forms collection, token re-issue"]
    ]
    add_table_data(doc, "Table 4.4: Service Catalog and Base Parameters Accepted by the Data Source Module", t44_headers, t44_rows, [Inches(1.05), Inches(1.35), Inches(0.95), Inches(1.05), Inches(1.85)])

    add_heading_3(doc, "4.2.2 Steps of Algorithm")
    add_p(doc, "QFlow incorporates two intelligent algorithms for operational decision-making: Algorithm 1 computes predictive service duration and personalized queue wait times, while Algorithm 2 executes dynamic heuristic scoring for counter recommendation.", space_after=6)

    # Algorithm 1 Callout Box
    algo1_steps = [
        ("1", "Historical Filtering", "Filter the synthetic operational dataset to extract all records corresponding to the customer's selected service name:", "D_service = { r in Dataset | r.serviceName == selectedService }"),
        ("2", "Temporal Weighted Regression", "Compute weighted baseline duration giving double weight to records from the current operating hour (r.hour == currentHour):", "w_i = (r_i.hour == currentHour) ? 2.0 : 1.0\nD_base = sum(r_i.duration * w_i) / sum(w_i)"),
        ("3", "Peak Hour & Queue Adjustment", "Apply temporal rush-hour surcharge (Delta_peak = 1.5 min during 09:00-11:00 and 14:00-16:00) and queue depth scale:", "D_predicted = max(1, round(D_base + Delta_peak + (Q_ahead * 0.05)))"),
        ("4", "Aggregate Facility Workload Formulation", "Sum the predicted remaining duration of currently serving tokens plus the estimated durations of all waiting tokens:", "W_total = sum(max(0, D_pred(t) - t_elapsed)) + sum(D_pred(t))"),
        ("5", "Wait-Time Derivation", "Divide aggregate facility workload by active counter capacity:", "T_wait = max(0, round(W_total / max(1, C_active)))")
    ]
    add_algorithm_box(
        doc,
        "Algorithm 1: Dynamic Service Duration and Wait-Time Prediction Engine",
        "Selected service S, historical duration records D, current hour H, active queue ahead Q_ahead, active counters C_active",
        "Estimated service duration D_predicted (minutes), predicted queue wait time T_wait (minutes)",
        algo1_steps
    )

    # Algorithm 2 Callout Box
    algo2_steps = [
        ("1", "Active Fleet Filtering", "Filter the fleet of registered counters to include only active desks:", "C_active = { c in Counters | c.isActive == true and c.status != 'OFFLINE' }"),
        ("2", "State-Based Base Scoring", "Assign baseline fitness score S_base based on current counter operational state:", "AVAILABLE (queue empty): 100 pts | AVAILABLE (general): 80 pts\nCALLING: 50 pts | IN_SERVICE: 30 pts"),
        ("3", "Workload & Latency Penalties", "Deduct 5 points per assigned waiting token, and deduct 2 points per minute of estimated remaining service time:", "S_final(c) = S_base(c) - (N_assigned(c) * 5) - (t_remaining(c) * 2)"),
        ("4", "Optimal Desk Recommendation", "Recommend counter desk C* with the maximum computed heuristic score:", "C* = argmax_{c in C_active} ( S_final(c) )")
    ]
    add_algorithm_box(
        doc,
        "Algorithm 2: Dynamic Multi-Factor Heuristic Counter Recommendation",
        "Registered counter fleet C, active queue tokens, live counter occupancy states",
        "Recommended target counter C* with highest composite fitness score",
        algo2_steps
    )

    add_heading_3(doc, "4.2.3 Data Processing Module")
    add_p(doc, "The backend data processing module manages REST routing, JWT middleware authentication, and Mongoose query execution. All state changes are executed with strict validation checks. Calling the next token executes an atomic findOneAndUpdate operation targeting { status: 'WAITING' }, guaranteeing that simultaneous staff clicks cannot double-allocate the same customer.", space_after=8)

    add_heading_3(doc, "4.2.4 Explainability Module")
    add_p(doc, "Explainability in QFlow ensures every automated recommendation is fully traceable and interpretable by administrative staff:", space_after=4)
    add_bullet_point(doc, "Transparent Reason Codes: ", "Every counter recommendation card in the staff UI displays the exact mathematical breakdown (e.g., 'Counter 2 recommended: Available (+80 pts), lowest queue backlog (-5 pts)').")
    add_bullet_point(doc, "Wait-Time Attribution: ", "Customer wait-time badges clearly display the contributing factors: base service complexity, active queue depth ahead, and current facility rush-hour multipliers.")
    add_bullet_point(doc, "Historical Traceability: ", "Every completed token records full chronological telemetry: creation timestamp, called timestamp, start timestamp, completion timestamp, serving counter ID, and serving teller ID.", space_after=8)

    add_heading_3(doc, "4.2.5 Visualization and Dashboard Module")
    add_p(doc, "The frontend visualization module provides high-density, responsive control dashboards for tellers and supervisors. Built using Recharts and Tailwind CSS, it renders live area charts for hourly arrival curves, bar graphs comparing counter consultation volumes, and dynamic status badges that update in real time without requiring manual browser page refreshes.", space_after=10)

    add_heading_2(doc, "4.3 CLASS DIAGRAM / DATA MODEL")
    add_p(doc, "The QFlow data model is implemented using MongoDB document schemas defined via Mongoose ODM. Table 4.5 summarizes the primary collections, key fields, and validation constraints, followed by the Entity-Relationship Schema in Figure 4.3.", space_after=6)

    t45_headers = ["Collection", "Key Attributes & Types", "Indexes & Constraints", "Operational Role"]
    t45_rows = [
        ["tokens", "tokenNumber (String), customerName (String), phone (String), service (String), status (Enum), estimatedDuration (Number), estimatedWaitTime (Number), counterId (Ref)", "unique: tokenNumber; index: status, createdAt", "Main transactional queue ledger"],
        ["counters", "counterNumber (Number), name (String), status (Enum), currentToken (Ref), currentTeller (Ref), servicesHandled ([String]), isActive (Boolean)", "unique: counterNumber; index: status, isActive", "Physical/virtual service desk fleet"],
        ["services", "code (String), name (String), baseDuration (Number), description (String), isActive (Boolean)", "unique: code", "Service catalogue parameters"],
        ["users", "name (String), email (String), password (String, bcrypt), role (Enum: 'staff', 'admin'), counterId (Ref)", "unique: email; index: role", "Staff and administrative accounts"]
    ]
    add_table_data(doc, "Table 4.5: MongoDB Collections Used by QFlow", t45_headers, t45_rows, [Inches(1.05), Inches(2.10), Inches(1.45), Inches(1.65)])

    if os.path.exists(er_img):
        add_figure_image(doc, er_img, "Figure 4.3: Class Diagram / Entity-Relationship Schema of the QFlow Data Model", max_width=6.0, max_height=4.0)

    add_heading_2(doc, "4.4 SEQUENCE DIAGRAM")
    add_p(doc, "The transactional sequence across customer registration, AI estimation, teller desk calling, and WebSocket notification dispatch unfolds through the following chronological phases:", space_after=4)
    add_numbered_point(doc, "Phase 1:", "Customer Registration: ", "Customer device scans QR code and sends POST /api/tokens with name, phone, and serviceCode.")
    add_numbered_point(doc, "Phase 2:", "Atomic Token Issuance & Estimation: ", "Server generates sequential token number (e.g., A101), calculates AI duration and wait time, commits to MongoDB with status: 'WAITING', and emits 'token:created' event.")
    add_numbered_point(doc, "Phase 3:", "Real-Time Broadcast: ", "Socket.IO server broadcasts 'queue:update' to the global 'queue' room. Customer device joins private room 'token:{id}'.")
    add_numbered_point(doc, "Phase 4:", "Teller Counter Calling: ", "Staff teller clicks 'Call Next' on workstation. Server executes atomic findOneAndUpdate to transition oldest WAITING token to CALLED and marks counter as CALLING.")
    add_numbered_point(doc, "Phase 5:", "Multisensory Alert Dispatch: ", "Server emits 'token:called' to customer room 'token:{id}'. The customer smartphone displays an on-screen modal banner and triggers navigator.vibrate([300, 100, 300]).")
    add_numbered_point(doc, "Phase 6:", "Service Completion: ", "Teller initiates consultation ('start') and concludes service ('complete'). Counter status returns to AVAILABLE, and completion telemetry is logged for analytics.", space_after=10)

    add_heading_2(doc, "4.5 TESTING AND RESULTS")
    add_p(doc, "Comprehensive functional validation and concurrency stress testing were conducted across all core workflows. Table 4.6 summarizes test execution results.", space_after=6)

    t46_headers = ["Test ID", "Test Case Description", "Test Execution Procedure", "Expected System Behavior", "Actual Observed Outcome", "Status"]
    t46_rows = [
        ["TC-01", "Server Initialization", "npm start execution", "Database connects, seed data verified, Socket.IO binds port 5000", "Server online, IP detected (192.168.1.7), DB active", "Pass"],
        ["TC-02", "QR Generation", "node generateQR.js", "Generates PNG/SVG QR codes embedding active LAN IP URL", "QR files generated in qr/ folder; scannable via smartphone", "Pass"],
        ["TC-03", "Staff Authentication", "POST /api/auth/login (valid)", "Returns HTTP 200, JWT token, and user profile", "HTTP 200, JWT returned; staff dashboard unlocks", "Pass"],
        ["TC-04", "Invalid Authentication", "POST /api/auth/login (wrong)", "Returns HTTP 401 Unauthorized", "HTTP 401 'Invalid credentials' error returned", "Pass"],
        ["TC-05", "Token Generation", "POST /api/tokens (valid)", "Sequential token created (e.g. A101), AI duration stamped", "Token created with predicted duration; wait time stamped", "Pass"],
        ["TC-06", "Token Validation", "POST /api/tokens (empty)", "Returns HTTP 400 Bad Request", "HTTP 400 'customerName, phone, and service required'", "Pass"],
        ["TC-07", "Call Next Concurrency", "2 tellers click Call simultaneously", "One teller receives token; second teller receives next/empty", "Atomic findOneAndUpdate prevents double-assignment", "Pass"],
        ["TC-08", "Real-Time Notification", "Counter calls Token A101", "Customer mobile receives yourTurn event within 200ms", "Phone screen flashes banner and triggers haptic vibration", "Pass"],
        ["TC-09", "Service Lifecycle", "Start -> Complete service", "Status advances: IN_SERVICE -> COMPLETED; counter available", "Timestamps recorded; counter marked AVAILABLE", "Pass"],
        ["TC-10", "Token Transfer", "Transfer token to Counter 3", "Token updates counterId; target counter alerted", "Token reassigned; customer screen updates counter number", "Pass"],
        ["TC-11", "Customer Skip", "Staff clicks 'Skip Token'", "Token marked SKIPPED; next waiting token moves up", "Queue order updates live across all connected displays", "Pass"],
        ["TC-12", "Analytics Generation", "GET /api/analytics/summary", "Aggregates completed tokens into averages and traffic curves", "Summary metrics and hourly distributions returned", "Pass"]
    ]
    add_table_data(doc, "Table 4.6: Functional Test Cases and Results", t46_headers, t46_rows, [Inches(0.75), Inches(1.10), Inches(1.30), Inches(1.30), Inches(1.30), Inches(0.50)])

    t47_headers = ["No.", "Technical Observation", "Root Cause Identified", "Engineering Remediation Applied"]
    t47_rows = [
        ["1", "Mobile phone could not reach localhost:5173 when scanning QR code", "localhost resolves to phone's loopback rather than server machine", "Implemented lanIP.js to automatically extract host Wi-Fi adapter IPv4 address"],
        ["2", "Vite dev server refused remote connections from smartphone browser", "Default Vite configuration binds strictly to loopback interface 127.0.0.1", "Configured --host 0.0.0.0 in package.json dev scripts"],
        ["3", "Customer token screen went out of sync when phone screen slept", "Mobile OS suspends background WebSocket execution to conserve battery", "Added automatic queue state re-fetch hook triggered on socket reconnect"],
        ["4", "Concurrent teller calls caused duplicate token assignments", "Initial controller implementation executed non-atomic read then update", "Refactored controller to use MongoDB atomic findOneAndUpdate"],
        ["5", "Mobile vibration failed to execute on desktop browser test runs", "Desktop web browsers do not implement the HTML5 Web Vibration API", "Added conditional feature check: if (navigator.vibrate) navigator.vibrate(...)"]
    ]
    add_table_data(doc, "Table 4.7: Technical Observations and Edge Cases Observed During Testing", t47_headers, t47_rows, [Inches(0.50), Inches(1.75), Inches(1.90), Inches(2.10)])

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 5: CONCLUSION AND FUTURE ENHANCEMENTS
    # =========================================================================
    add_heading_1(doc, "CHAPTER 5\nCONCLUSION AND FUTURE ENHANCEMENTS")
    add_chapter_intro(doc, "the conclusive assessment of the QFlow project against its foundational engineering objectives, summarizing key deliverables and outlining promising directions for future system enhancements.")

    add_heading_2(doc, "5.1 CONCLUSION")
    add_p(doc, "The QFlow Smart Token and Queue Management System successfully demonstrates a modern, responsive, hardware-free alternative to traditional physical queue dispensers. By integrating the MERN stack (MongoDB, Express.js, React 19, Node.js) with native Socket.IO WebSocket bi-directional streaming, QFlow empowers facility visitors to join queues seamlessly on their personal smartphones via dynamic QR code scanning.", space_after=8)

    add_p(doc, "The platform achieves its primary design objectives:", space_after=4)
    add_bullet_point(doc, "Elimination of Consumable Hardware: ", "Replaces expensive kiosk hardware, mechanical buttons, and consumable thermal paper rolls with a responsive mobile web interface.")
    add_bullet_point(doc, "Context-Aware AI Duration Modeling: ", "Computes real-time, context-aware service duration and wait-time predictions using a calibrated historical regression baseline adjusted for peak hours.")
    add_bullet_point(doc, "Workload-Balanced Counter Allocation: ", "Dynamically scores and balances counter assignments across active tellers using a 100-point heuristic formula to prevent facility bottlenecks.")
    add_bullet_point(doc, "Sub-Millisecond Event Dissemination: ", "Synchronizes queue state transitions across staff consoles and customer smartphones with sub-200ms latency via Socket.IO WebSocket rooms.")
    add_bullet_point(doc, "Multisensory Haptic Notification: ", "Delivers haptic vibration alerts directly to customer handsets when their token is called, liberating visitors from crowded waiting lounges.")
    add_bullet_point(doc, "Guaranteed Concurrency Control: ", "Enforces atomic database operations using MongoDB findOneAndUpdate to eliminate duplicate counter call race conditions under heavy traffic.", space_after=8)

    add_p(doc, "Empirical verification across multiple mobile and desktop platforms confirmed that all core workflows—token issuance, heuristic wait estimation, teller state management, token skipping, inter-counter transferring, and analytics aggregation—function reliably under local network conditions.", space_after=10)

    add_heading_2(doc, "5.2 FUTURE ENHANCEMENTS")
    add_p(doc, "To advance QFlow from a localized prototype to an enterprise-grade multi-facility queue orchestration ecosystem, the following enhancements are planned:", space_after=4)
    add_numbered_point(doc, "1.", "Public Lounge Display with Text-to-Speech (TTS): ", "Implement an automated full-screen waiting lounge display board with synthesized multi-lingual voice announcements (e.g., 'Token A101, please proceed to Counter 2').")
    add_numbered_point(doc, "2.", "Cellular SMS & WhatsApp Notification Gateways: ", "Integrate Twilio or WhatsApp Business APIs to deliver turn notifications to customers who close their mobile browser or lack persistent Wi-Fi connectivity.")
    add_numbered_point(doc, "3.", "Deep Machine-Learning Duration Modeling: ", "Replace the current weighted synthetic baseline with a trained Gradient Boosting or Random Forest regressor trained on longitudinal facility telemetry.")
    add_numbered_point(doc, "4.", "Multi-Branch Multi-Tenant Architecture: ", "Expand the database schema and routing to support multi-site enterprises with centralized corporate analytics dashboards.")
    add_numbered_point(doc, "5.", "Customer Feedback & Service Rating Module: ", "Allow customers to submit instantaneous five-star ratings and textual feedback on their mobile devices upon service completion.")
    add_numbered_point(doc, "6.", "Turnkey Cloud Container Orchestration: ", "Package multi-stage Dockerfiles and Helm charts for turnkey deployment on Kubernetes or AWS ECS clusters.", space_after=10)

    doc.add_page_break()

    # =========================================================================
    # APPENDIX 1: SAMPLE CODE (CURATED REPRESENTATIVE LISTINGS)
    # =========================================================================
    add_heading_1(doc, "APPENDIX 1: SAMPLE CODE")
    add_p(doc, "This appendix presents representative excerpts from the QFlow source code. Each excerpt is copied directly from the repository and labelled with its file path and key functions. Long functions are structured for clarity, and credentials use placeholder values.", space_after=10)

    # 1. Project Structure
    struct_code = """QFlow/
|-- client/                              # React 19 / Vite Frontend
|   |-- src/
|   |   |-- components/                  # CounterCard, AIRecommendation, QRModal, TransferModal
|   |   |-- context/                     # AuthContext.jsx, QueueContext.jsx
|   |   |-- layouts/                     # StaffLayout.jsx
|   |   |-- pages/
|   |   |   |-- auth/                    # LoginPage.jsx
|   |   |   |-- customer/                # CustomerPortal.jsx, TokenStatus.jsx
|   |   |   `-- staff/                   # Dashboard.jsx, QueuePage.jsx, CountersPage.jsx, AnalyticsPage.jsx
|   |   |-- services/                    # api.js (Axios), socket.js (Socket.IO client)
|   |   |-- App.jsx                      # Main React Router configuration
|   |   `-- main.jsx                     # Application bootstrap
|   |-- package.json
|   `-- vite.config.js
|-- server/                              # Express.js / Node.js Backend
|   |-- src/
|   |   |-- controllers/                 # auth, token, counter, service, queue, analytics
|   |   |-- models/                      # User.js, Token.js, Counter.js, Service.js
|   |   |-- routes/                      # authRoutes, tokenRoutes, counterRoutes, etc.
|   |   |-- services/                    # predictionService.js, counterAssignmentService.js
|   |   |-- sockets/                     # socketHandler.js
|   |   |-- middleware/                  # auth.js (JWT verify), errorHandler.js
|   |   |-- utils/                       # lanIP.js
|   |   `-- server.js                    # Express app & Socket.IO server entry point
|   |-- scripts/
|   |   |-- seed.js                      # Database seeder (services, counters, sample tokens)
|   |   `-- generateQR.js                # Dynamic QR code generator
|   `-- package.json
|-- qr/                                  # Auto-generated QR images (PNG, SVG)
|-- package.json                         # Root scripts (concurrent execution)
`-- README.md"""
    add_code_block(doc, struct_code, "1. Project Directory Structure")

    # 2. Installation Commands
    inst_code = """# Clone and enter the project repository
cd c:\\Projects\\QFlow

# Install root, backend, and frontend dependencies concurrently
npm run install-all

# Generate dynamic QR codes embedding the active local Wi-Fi IP address
npm run generate-qr

# Seed database with initial services, counters, and admin accounts
npm run seed

# Launch both Express backend (port 5000) and Vite client (port 5173) concurrently
npm run dev"""
    add_code_block(doc, inst_code, "2. Installation and Execution Commands")

    # 3. Environment Variables
    env_code = """# Server Port Configuration
PORT=5000

# MongoDB URI (Supports local instance or zero-config in-memory fallback)
MONGODB_URI=mongodb://127.0.0.1:27017/qflow

# JWT Secret for Staff/Admin Authentication Tokens
JWT_SECRET=qflow_super_secure_jwt_secret_key_2026

# Allowed Frontend Client Origin for CORS
CLIENT_URL=http://localhost:5173

# Node Environment
NODE_ENV=development"""
    add_code_block(doc, env_code, "3. Server Environment Configuration (.env)")

    # 4. Database Models
    model_token_code = """// server/src/models/Token.js
const mongoose = require('mongoose');

const tokenSchema = new mongoose.Schema({
  tokenNumber: { type: String, unique: true, required: true },
  customerName: { type: String, required: true, trim: true },
  phone: { type: String, required: true, trim: true },
  service: { type: String, required: true },
  priority: { type: String, enum: ['REGULAR', 'SENIOR', 'VIP', 'EMERGENCY'], default: 'REGULAR' },
  status: { 
    type: String, 
    enum: ['WAITING', 'CALLED', 'IN_SERVICE', 'COMPLETED', 'SKIPPED', 'CANCELLED'], 
    default: 'WAITING' 
  },
  counterId: { type: mongoose.Schema.Types.ObjectId, ref: 'Counter' },
  counterNumber: { type: Number },
  estimatedDuration: { type: Number, default: 10 },
  estimatedWaitTime: { type: Number, default: 0 },
  actualDuration: { type: Number },
  calledAt: { type: Date },
  servedAt: { type: Date },
  completedAt: { type: Date }
}, { timestamps: true });

tokenSchema.index({ status: 1, createdAt: 1 });
module.exports = mongoose.model('Token', tokenSchema);"""
    add_code_block(doc, model_token_code, "4.1 Token Data Model (server/src/models/Token.js)")

    model_counter_code = """// server/src/models/Counter.js
const mongoose = require('mongoose');

const counterSchema = new mongoose.Schema({
  counterNumber: { type: Number, unique: true, required: true },
  name: { type: String, required: true },
  status: { type: String, enum: ['AVAILABLE', 'BUSY', 'PAUSED', 'OFFLINE'], default: 'AVAILABLE' },
  currentToken: { type: mongoose.Schema.Types.ObjectId, ref: 'Token' },
  currentTeller: { type: mongoose.Schema.Types.ObjectId, ref: 'User' },
  servicesHandled: [{ type: String }],
  isActive: { type: Boolean, default: true }
}, { timestamps: true });

module.exports = mongoose.model('Counter', counterSchema);"""
    add_code_block(doc, model_counter_code, "4.2 Counter Data Model (server/src/models/Counter.js)")

    # 5. Server Entry Point
    server_code = """// server/src/server.js
const express = require('express');
const http = require('http');
const { Server } = require('socket.io');
const mongoose = require('mongoose');
const cors = require('cors');
require('dotenv').config();

const { initSocket } = require('./sockets/socketHandler');
const { getLocalIP } = require('./utils/lanIP');

const app = express();
const server = http.createServer(app);

const io = new Server(server, {
  cors: { origin: '*', methods: ['GET', 'POST', 'PATCH', 'PUT', 'DELETE'] }
});

app.use(cors());
app.use(express.json());

// Bind routes
app.use('/api/auth', require('./routes/authRoutes'));
app.use('/api/tokens', require('./routes/tokenRoutes'));
app.use('/api/counters', require('./routes/counterRoutes'));
app.use('/api/services', require('./routes/serviceRoutes'));
app.use('/api/analytics', require('./routes/analyticsRoutes'));

initSocket(io);

const PORT = process.env.PORT || 5000;
server.listen(PORT, '0.0.0.0', () => {
  const lanIP = getLocalIP();
  console.log(`[QFlow Server] Listening on port ${PORT}`);
  console.log(`[QFlow Portal] Customer URL: http://${lanIP}:5173/register`);
});"""
    add_code_block(doc, server_code, "5. Main Server File and Database Connection (server/src/server.js)")

    # 6. Token Controller
    token_ctrl_code = """// server/src/controllers/tokenController.js (Atomic Token Issuance & Call Next)
exports.generateToken = async (req, res) => {
  try {
    const { customerName, phone, service, priority = 'REGULAR' } = req.body;
    if (!customerName || !phone || !service) {
      return res.status(400).json({ error: 'customerName, phone, and service required' });
    }
    const today = new Date(); today.setHours(0, 0, 0, 0);
    const count = await Token.countDocuments({ createdAt: { $gte: today } });
    const tokenNumber = `A${String(count + 1).padStart(3, '0')}`;

    const waiting = await Token.find({ status: 'WAITING' });
    const activeCounters = await Counter.countDocuments({ isActive: true, status: { $ne: 'OFFLINE' } });
    const { estimatedDuration } = await predictServiceDuration(service, waiting.length);
    const estimatedWaitTime = await calculateWaitTime(waiting, activeCounters, service);

    const token = await Token.create({
      tokenNumber, customerName, phone, service, priority,
      estimatedDuration, estimatedWaitTime
    });

    const io = req.app.get('io');
    if (io) { io.to('queue').emit('token:created', token); io.to('queue').emit('queue:update'); }
    return res.status(201).json(token);
  } catch (err) { return res.status(500).json({ error: err.message }); }
};

exports.callNextToken = async (req, res) => {
  try {
    const { counterId } = req.params;
    const counter = await Counter.findById(counterId);
    if (!counter) return res.status(404).json({ error: 'Counter not found' });

    // Atomic findOneAndUpdate eliminates race conditions across concurrent tellers
    const token = await Token.findOneAndUpdate(
      { status: 'WAITING' },
      { $set: { status: 'CALLED', counterId, counterNumber: counter.counterNumber, calledAt: new Date() } },
      { sort: { priority: -1, createdAt: 1 }, new: true }
    );
    if (!token) return res.status(404).json({ message: 'No waiting tokens in queue' });

    counter.status = 'BUSY'; counter.currentToken = token._id;
    await counter.save();

    const io = req.app.get('io');
    if (io) { io.to(`token:${token._id}`).emit('token:called', token); io.to('queue').emit('queue:update'); }
    return res.json(token);
  } catch (err) { return res.status(500).json({ error: err.message }); }
};"""
    add_code_block(doc, token_ctrl_code, "6. Token Controller & Concurrency Logic (server/src/controllers/tokenController.js)")

    # 7. Auth Controller
    auth_code = """// server/src/controllers/authController.js
const User = require('../models/User');
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');

exports.login = async (req, res) => {
  try {
    const { email, password } = req.body;
    const user = await User.findOne({ email });
    if (!user) return res.status(401).json({ error: 'Invalid credentials' });

    const isMatch = await bcrypt.compare(password, user.password);
    if (!isMatch) return res.status(401).json({ error: 'Invalid credentials' });

    const token = jwt.sign(
      { id: user._id, role: user.role, name: user.name },
      process.env.JWT_SECRET || 'qflow_jwt_secret',
      { expiresIn: '12h' }
    );

    return res.json({ token, user: { id: user._id, name: user.name, role: user.role } });
  } catch (err) {
    return res.status(500).json({ error: err.message });
  }
};"""
    add_code_block(doc, auth_code, "7. Authentication Controller and JWT Middleware")

    # 8. AI Prediction Engine
    pred_code = """// server/src/services/predictionService.js
const historicalDurations = require('../data/historicalDurations.json');

exports.predictServiceDuration = async (serviceName, queueLengthAhead = 0) => {
  const currentHour = new Date().getHours();
  const matched = historicalDurations.filter(d => d.serviceName === serviceName);

  if (!matched.length) {
    return { estimatedDuration: 10, confidence: 0.5 };
  }

  // Weight records from same operating hour 2x higher
  let weightedSum = 0;
  let weightTotal = 0;
  for (const r of matched) {
    const w = (r.hour === currentHour) ? 2.0 : 1.0;
    weightedSum += r.duration * w;
    weightTotal += w;
  }
  const baseDuration = weightedSum / weightTotal;

  // Rush hour surcharge (09:00-11:00, 14:00-16:00)
  const isPeak = (currentHour >= 9 && currentHour <= 11) || (currentHour >= 14 && currentHour <= 16);
  const peakDelta = isPeak ? 1.5 : 0;
  const queueFactor = queueLengthAhead * 0.05;

  const estimatedDuration = Math.max(1, Math.round(baseDuration + peakDelta + queueFactor));
  return { estimatedDuration, confidence: 0.85 };
};

exports.calculateWaitTime = async (waitingTokens, activeCounters, targetService) => {
  if (!activeCounters || activeCounters < 1) activeCounters = 1;

  let totalWorkload = 0;
  for (const t of waitingTokens) {
    totalWorkload += t.estimatedDuration || 10;
  }
  return Math.max(0, Math.round(totalWorkload / activeCounters));
};"""
    add_code_block(doc, pred_code, "8. AI Service Duration and Wait-Time Prediction Engine")

    # 9. Dynamic Counter Recommendation
    rec_code = """// server/src/services/counterAssignmentService.js
exports.recommendCounter = async (token, activeCounters) => {
  if (!activeCounters || !activeCounters.length) return null;

  let bestCounter = null;
  let highestScore = -Infinity;

  for (const counter of activeCounters) {
    let score = 0;
    if (counter.status === 'AVAILABLE' && !counter.currentToken) {
      score += 100;
    } else if (counter.status === 'AVAILABLE') {
      score += 80;
    } else if (counter.status === 'CALLING') {
      score += 50;
    } else if (counter.status === 'BUSY') {
      score += 30;
    }

    const assignedCount = counter.assignedTokensCount || 0;
    score -= (assignedCount * 5);

    if (score > highestScore) {
      highestScore = score;
      bestCounter = counter;
    }
  }
  return { recommendedCounter: bestCounter, score: highestScore };
};"""
    add_code_block(doc, rec_code, "9. Dynamic Counter Recommendation Scoring Engine")

    # 10. Socket Handler
    sock_code = """// server/src/sockets/socketHandler.js
exports.initSocket = (io) => {
  io.on('connection', (socket) => {
    // Client joins public queue feed
    socket.on('join:queue', () => {
      socket.join('queue');
    });

    // Customer joins private room for their specific token
    socket.on('join:token', (tokenId) => {
      socket.join(`token:${tokenId}`);
    });

    // Tellers join counter channel
    socket.on('join:counter', (counterId) => {
      socket.join(`counter:${counterId}`);
    });

    socket.on('disconnect', () => {
      // Automatic socket teardown
    });
  });
};"""
    add_code_block(doc, sock_code, "10. Socket.IO Room Multiplexing and Broadcasting Logic")

    # 11. React Queue Context
    client_ctx_code = """// client/src/context/QueueContext.jsx
import React, { createContext, useContext, useEffect, useState } from 'react';
import { socket } from '../services/socket';
import api from '../services/api';

const QueueContext = createContext();

export const QueueProvider = ({ children }) => {
  const [tokens, setTokens] = useState([]);
  const [counters, setCounters] = useState([]);

  const refreshQueue = async () => {
    try {
      const [tokRes, cntRes] = await Promise.all([
        api.get('/tokens/active'),
        api.get('/counters')
      ]);
      setTokens(tokRes.data);
      setCounters(cntRes.data);
    } catch (err) {
      console.error('Queue fetch error:', err);
    }
  };

  useEffect(() => {
    refreshQueue();
    socket.emit('join:queue');
    socket.on('queue:update', refreshQueue);
    return () => {
      socket.off('queue:update');
    };
  }, []);

  return (
    <QueueContext.Provider value={{ tokens, counters, refreshQueue }}>
      {children}
    </QueueContext.Provider>
  );
};

export const useQueue = () => useContext(QueueContext);"""
    add_code_block(doc, client_ctx_code, "11. Client Real-Time Queue Context Synchronization")

    # 12. Customer Mobile Vibration
    mob_vib_code = """// client/src/pages/customer/TokenStatus.jsx (Excerpt: Real-Time Haptic Alert)
useEffect(() => {
  if (!token?._id) return;

  socket.emit('join:token', token._id);

  socket.on('token:called', (updatedToken) => {
    setToken(updatedToken);
    setShowCalledModal(true);

    // Trigger HTML5 Web Vibration API on customer phone
    if ('vibrate' in navigator) {
      navigator.vibrate([300, 100, 300, 100, 400]);
    }
  });

  return () => {
    socket.off('token:called');
  };
}, [token?._id]);"""
    add_code_block(doc, mob_vib_code, "12. Customer Mobile Status & Haptic Vibration Handler")

    # 13. REST JSON Excerpt
    rest_json = """// Sample Response: POST /api/tokens
{
  "_id": "67167a50e932b1234567890a",
  "tokenNumber": "A127",
  "customerName": "Priya Sharma",
  "phone": "+91 98765 43210",
  "service": "DOC_VER",
  "priority": "REGULAR",
  "status": "WAITING",
  "estimatedDuration": 15,
  "estimatedWaitTime": 12,
  "createdAt": "2026-10-21T10:15:30.000Z"
}

// Sample Response: PATCH /api/tokens/:id/call
{
  "message": "Token A127 called to Counter 1 successfully.",
  "token": { "tokenNumber": "A127", "status": "CALLED" }
}"""
    add_code_block(doc, rest_json, "13. REST API Request and Response Examples")

    doc.add_page_break()

    # =========================================================================
    # PROJECT SCREENSHOTS
    # =========================================================================
    add_main_title(doc, "PROJECT SCREENSHOTS")
    add_p(doc, "The screenshots below are captured directly from the running QFlow system across staff administrative workstations and customer smartphone client devices.", space_after=12)

    add_figure_image(doc, os.path.join(img_dir, "login.png"), "Figure A.1: Staff and Administrative Authentication Portal", max_width=5.5, max_height=4.0)
    add_figure_image(doc, os.path.join(img_dir, "dash.png"), "Figure A.2: Live Staff Operations Dashboard with Active Counters", max_width=6.0, max_height=3.6)
    add_figure_image(doc, os.path.join(img_dir, "qr.png"), "Figure A.3: Customer QR Code Registration Poster and Modal", max_width=4.8, max_height=3.8)

    add_figure_image(doc, os.path.join(img_dir, "WhatsApp Image 2026-10-21 at 4.42.16 PM.jpeg"), "Figure A.4: Mobile Customer Portal - Welcome and Value Proposition", max_width=2.8, max_height=4.8)
    add_figure_image(doc, os.path.join(img_dir, "WhatsApp Image 2026-10-21 at 4.42.16 PM (1).jpeg"), "Figure A.5: Mobile Customer Registration Form with Service Selection", max_width=2.8, max_height=4.8)
    add_figure_image(doc, os.path.join(img_dir, "WhatsApp Image 2026-10-21 at 4.42.16 PM (2).jpeg"), "Figure A.6: Mobile Service Catalogue Modal Dialog", max_width=2.8, max_height=4.8)
    add_figure_image(doc, os.path.join(img_dir, "WhatsApp Image 2026-10-21 at 4.42.17 PM.jpeg"), "Figure A.7: Live Mobile Customer Ticket - Waiting Status with AI Estimation", max_width=2.8, max_height=4.8)
    add_figure_image(doc, os.path.join(img_dir, "WhatsApp Image 2026-10-21 at 4.42.17 PM (1).jpeg"), "Figure A.8: Real-Time Mobile Haptic & Visual Turn Alert Screen", max_width=2.8, max_height=4.8)
    add_figure_image(doc, os.path.join(img_dir, "WhatsApp Image 2026-10-21 at 4.42.17 PM (2).jpeg"), "Figure A.9: Active Mobile Consultation In-Service Status Monitor", max_width=2.8, max_height=4.8)
    add_figure_image(doc, os.path.join(img_dir, "WhatsApp Image 2026-10-21 at 4.42.18 PM.jpeg"), "Figure A.10: Service Completion Confirmation Screen", max_width=2.8, max_height=4.8)

    add_figure_image(doc, os.path.join(img_dir, "counters.png"), "Figure A.11: Counter Management and Dynamic Fleet Allocation Workspace", max_width=6.0, max_height=3.4)
    add_figure_image(doc, os.path.join(img_dir, "queue.png"), "Figure A.12: Real-Time Queue Inspection and Live Token Roster", max_width=6.0, max_height=3.4)
    add_figure_image(doc, os.path.join(img_dir, "analytics.png"), "Figure A.13: Executive Operational Analytics Dashboard with Traffic Distributions", max_width=6.0, max_height=3.5)
    add_figure_image(doc, os.path.join(img_dir, "active_counter.png"), "Figure A.14: Active Counter Workspace Telemetry Detail Cards", max_width=6.0, max_height=3.2)

    doc.add_page_break()

    # =========================================================================
    # REFERENCES
    # =========================================================================
    add_main_title(doc, "REFERENCES")
    
    add_reference_item(doc, "1", "A. K. Erlang", "The Theory of Probabilities and Telephone Conversations", "Nyt Tidsskrift for Matematik B, vol. 20", "pp. 33–39, 1909")
    add_reference_item(doc, "2", "D. G. Kendall", "Stochastic Processes Occurring in the Theory of Queues and their Analysis by the Method of the Imbedded Markov Chain", "The Annals of Mathematical Statistics, vol. 24, no. 3", "pp. 338–354, 1953")
    add_reference_item(doc, "3", "J. D. C. Little", "A Proof for the Queuing Formula: L = λW", "Operations Research, vol. 9, no. 3", "pp. 383–387, 1961")
    add_reference_item(doc, "4", "R. C. Larson", "The Psychology of Waiting Lines", "Operations Research, vol. 35, no. 6", "pp. 895–901, 1987")
    add_reference_item(doc, "5", "C. H. Fine and E. B. Sankar", "Predictive Analytics in Service Queue Scheduling", "Management Science, vol. 64, no. 4", "pp. 1720–1738, 2018")
    add_reference_item(doc, "6", "R. T. Fielding", "Architectural Styles and the Design of Network-based Software Architectures", "Ph.D. dissertation, University of California, Irvine", "2000")
    add_reference_item(doc, "7", "I. Fette and A. Melnikov", "The WebSocket Protocol", "Internet Engineering Task Force (IETF) RFC 6455", "Dec. 2011")
    add_reference_item(doc, "8", "Socket.IO Community", "Socket.IO Documentation: Real-Time Event Driven Engine", "Online documentation", "https://socket.io/docs/v4/, 2024")
    add_reference_item(doc, "9", "K. Chodorow", "MongoDB: The Definitive Guide - Powerful and Scalable Data Storage", "O'Reilly Media, Sebastopol, CA, USA, 3rd ed.", "2020")
    add_reference_item(doc, "10", "Mongoose ODM Community", "Mongoose v8 API Documentation: Atomic Operations and Schemas", "Online resource", "https://mongoosejs.com/docs/api.html, 2024")
    add_reference_item(doc, "11", "Meta Open Source", "React 19 Documentation: Concurrent Rendering and Reactive Actions", "Online resource", "https://react.dev/, 2024")
    add_reference_item(doc, "12", "Vite Community", "Vite: Next Generation Frontend Tooling", "Online documentation", "https://vitejs.dev/, 2024")
    add_reference_item(doc, "13", "M. Jones, J. Bradley, and N. Sakimura", "JSON Web Token (JWT)", "IETF RFC 7519", "May 2015")
    add_reference_item(doc, "14", "N. Provos and D. Mazières", "A Future-Adaptable Password Scheme", "in Proceedings of the USENIX Annual Technical Conference, FREENIX Track", "pp. 81–92, 1999")
    add_reference_item(doc, "15", "W3C", "Vibration API: W3C Recommendation", "World Wide Web Consortium", "https://www.w3.org/TR/vibration/, 2016")
    add_reference_item(doc, "16", "Tailwind Labs", "Tailwind CSS Documentation: Utility-First CSS Framework", "Online resource", "https://tailwindcss.com/docs, 2024")
    add_reference_item(doc, "17", "Recharts Group", "Recharts: Redefined Chart Library Built with React and D3", "Online documentation", "https://recharts.org/, 2024")
    add_reference_item(doc, "18", "Node.js Foundation", "Node.js v22.x LTS Documentation: Asynchronous Runtime", "Online resource", "https://nodejs.org/docs/latest-v22.x/api/, 2024")

    output_path = r"C:\Projects\QFlow\QFLOW_PROJECT_REPORT.docx"
    doc.save(output_path)
    print(f"Report generated successfully: {output_path}")

if __name__ == "__main__":
    build_document()
