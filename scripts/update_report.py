import re
import os

report_path = r"c:\Projects\QFlow\scripts\build_full_report_docx.py"
with open(report_path, "r", encoding="utf-8") as f:
    text = f.read()

# 1. Update the certificate section
cert_pattern = re.compile(
    r"    # =========================================================================\s*"
    r"    # 2\. BONAFIDE CERTIFICATE.*?setup_footer\(s2\)",
    re.DOTALL
)

new_cert_block = """    # =========================================================================
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
    r_c1_h = p_c1.add_run("HEAD OF THE DEPARTMENT\\nDr. T. Kalai Selvi\\n")
    r_c1_h.font.name = "Times New Roman"; r_c1_h.font.size = Pt(11); r_c1_h.font.bold = True
    r_c1_d = p_c1.add_run("Easwari Engineering College,\\nRamapuram, Chennai – 600089.")
    r_c1_d.font.name = "Times New Roman"; r_c1_d.font.size = Pt(10.5)

    c2 = t_cert.rows[0].cells[1]
    tcPr2 = c2._element.get_or_add_tcPr()
    for child in tcPr2.findall(qn('w:tcW')): tcPr2.remove(child)
    tcW2 = OxmlElement('w:tcW'); tcW2.set(qn('w:w'), '4500'); tcW2.set(qn('w:type'), 'dxa'); tcPr2.append(tcW2)
    p_c2 = c2.paragraphs[0]
    p_c2.paragraph_format.first_line_indent = Inches(0)
    p_c2.paragraph_format.line_spacing = 1.25
    p_c2.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r_c2_h = p_c2.add_run("SUPERVISOR\\nMs. D. S. K. Harshitha\\n")
    r_c2_h.font.name = "Times New Roman"; r_c2_h.font.size = Pt(11); r_c2_h.font.bold = True
    r_c2_d = p_c2.add_run("Easwari Engineering College,\\nRamapuram, Chennai – 600089.")
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
    r_v1 = p_v1.add_run("Internal Examiner\\nDate:")
    r_v1.font.name = "Times New Roman"
    r_v1.font.size = Pt(11)
    r_v1.font.bold = True
    r_v1.font.color.rgb = RGBColor(0, 0, 0)

    doc.add_page_break()"""

assert cert_pattern.search(text) is not None, "Cert pattern not found in text"
text = cert_pattern.sub(new_cert_block, text)

# 2. Update Table of Contents, List of Tables, List of Figures column widths and TOC list
text = text.replace(
    'add_borderless_table(doc, ["CHAPTER NO.", "TITLE", "PAGE No."], toc_data, col_widths=[Inches(1.3), Inches(4.3), Inches(0.9)], bold_ch_only=True)',
    'add_borderless_table(doc, ["CHAPTER NO.", "TITLE", "PAGE No."], toc_data, col_widths=[Inches(1.30), Inches(4.15), Inches(0.80)], bold_ch_only=True)'
)
text = text.replace(
    'add_borderless_table(doc, ["TABLE NO.", "TABLE TITLE", "PAGE No."], tables_list, col_widths=[Inches(1.3), Inches(4.3), Inches(0.9)], bold_ch_only=False)',
    'add_borderless_table(doc, ["TABLE NO.", "TABLE TITLE", "PAGE No."], tables_list, col_widths=[Inches(1.30), Inches(4.15), Inches(0.80)], bold_ch_only=False)'
)
text = text.replace(
    'add_borderless_table(doc, ["FIGURE NO.", "FIGURE TITLE", "PAGE No."], figures_list, col_widths=[Inches(1.3), Inches(4.3), Inches(0.9)], bold_ch_only=False)',
    'add_borderless_table(doc, ["FIGURE NO.", "FIGURE TITLE", "PAGE No."], figures_list, col_widths=[Inches(1.30), Inches(4.15), Inches(0.80)], bold_ch_only=False)'
)

# 3. Update all table column widths to sum to exactly 6.25 inches
text = text.replace(
    '[Inches(1.5), Inches(1.2), Inches(1.1), Inches(1.0), Inches(1.1), Inches(1.1)]',
    '[Inches(1.15), Inches(1.05), Inches(1.05), Inches(1.00), Inches(1.00), Inches(1.00)]'
)
text = text.replace(
    '[Inches(2.5), Inches(4.0)]',
    '[Inches(2.25), Inches(4.00)]'
)
text = text.replace(
    '[Inches(1.0), Inches(1.8), Inches(3.7)]',
    '[Inches(0.95), Inches(1.70), Inches(3.60)]'
)
text = text.replace(
    '[Inches(1.2), Inches(1.5), Inches(1.5), Inches(2.3)]',
    '[Inches(1.15), Inches(1.40), Inches(1.40), Inches(2.30)]'
)
text = text.replace(
    '[Inches(1.2), Inches(1.7), Inches(1.7), Inches(1.9)]',
    '[Inches(1.15), Inches(1.60), Inches(1.60), Inches(1.90)]'
)
text = text.replace(
    '[Inches(0.9), Inches(1.4), Inches(1.1), Inches(1.5), Inches(1.6)]',
    '[Inches(0.85), Inches(1.35), Inches(1.05), Inches(1.45), Inches(1.55)]'
)
text = text.replace(
    '[Inches(1.0), Inches(1.8), Inches(1.1), Inches(2.6)]',
    '[Inches(0.85), Inches(1.85), Inches(1.10), Inches(2.45)]'
)
text = text.replace(
    '[Inches(2.2), Inches(4.3)]',
    '[Inches(2.15), Inches(4.10)]'
)
text = text.replace(
    '[Inches(1.8), Inches(2.2), Inches(2.5)]',
    '[Inches(1.75), Inches(2.10), Inches(2.40)]'
)
text = text.replace(
    '[Inches(1.1), Inches(1.4), Inches(1.0), Inches(1.1), Inches(1.9)]',
    '[Inches(1.05), Inches(1.35), Inches(0.95), Inches(1.05), Inches(1.85)]'
)
text = text.replace(
    '[Inches(1.1), Inches(2.2), Inches(1.5), Inches(1.7)]',
    '[Inches(1.05), Inches(2.10), Inches(1.45), Inches(1.65)]'
)
text = text.replace(
    '[Inches(0.8), Inches(1.2), Inches(1.4), Inches(1.4), Inches(1.4), Inches(0.5)]',
    '[Inches(0.75), Inches(1.10), Inches(1.30), Inches(1.30), Inches(1.30), Inches(0.50)]'
)
text = text.replace(
    '[Inches(0.5), Inches(1.8), Inches(2.0), Inches(2.2)]',
    '[Inches(0.50), Inches(1.75), Inches(1.90), Inches(2.10)]'
)

with open(report_path, "w", encoding="utf-8") as f:
    f.write(text)

print("build_full_report_docx.py updated successfully!")
