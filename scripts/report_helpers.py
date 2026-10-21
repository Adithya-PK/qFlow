import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from PIL import Image

def set_cell_background(cell, fill_hex):
    tcPr = cell._element.get_or_add_tcPr()
    for shd in tcPr.findall(qn('w:shd')):
        tcPr.remove(shd)
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), fill_hex)
    tcPr.append(shd)

def set_table_borders(table, color="000000", sz="4", val="single"):
    tblPr = table._element.xpath('w:tblPr')
    if tblPr:
        for b in tblPr[0].findall(qn('w:tblBorders')):
            tblPr[0].remove(b)
        borders = OxmlElement('w:tblBorders')
        for border_name in ['top', 'left', 'bottom', 'right', 'insideH', 'insideV']:
            b = OxmlElement(f'w:{border_name}')
            b.set(qn('w:val'), val)
            b.set(qn('w:sz'), sz)
            b.set(qn('w:space'), '0')
            b.set(qn('w:color'), color)
            borders.append(b)
        tblPr[0].append(borders)

def set_cell_margins(cell, top=70, bottom=70, left=100, right=100):
    tcPr = cell._element.get_or_add_tcPr()
    for tcMar in tcPr.findall(qn('w:tcMar')):
        tcPr.remove(tcMar)
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def add_p(doc, text="", font_name="Times New Roman", font_size=12, bold=False, italic=False, color=None, alignment=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0, space_after=6, line_spacing=1.5, tab_indent=True, keep_with_next=False):
    p = doc.add_paragraph()
    p.alignment = alignment
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = line_spacing
    p.paragraph_format.keep_with_next = keep_with_next
    if tab_indent:
        p.paragraph_format.first_line_indent = Inches(0.5)
    else:
        p.paragraph_format.first_line_indent = Inches(0)

    if text:
        run = p.add_run(text)
        run.font.name = font_name
        run.font.size = Pt(font_size)
        run.font.bold = bold
        run.font.italic = italic
        run.font.color.rgb = color if color else RGBColor(0, 0, 0)
    return p

def add_bullet_point(doc, bold_prefix="", text="", level=0, space_after=3, line_spacing=1.5):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_before = Pt(1)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = line_spacing
    indent_base = 0.5 + (level * 0.25)
    p.paragraph_format.left_indent = Inches(indent_base)
    p.paragraph_format.first_line_indent = Inches(-0.2)
    
    r_bullet = p.add_run("•  ")
    r_bullet.font.name = "Times New Roman"
    r_bullet.font.size = Pt(12)
    r_bullet.font.bold = True
    r_bullet.font.color.rgb = RGBColor(0, 0, 0)
    
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = "Times New Roman"
        r_pre.font.size = Pt(12)
        r_pre.font.bold = True
        r_pre.font.color.rgb = RGBColor(0, 0, 0)
        
    if text:
        r_txt = p.add_run(text)
        r_txt.font.name = "Times New Roman"
        r_txt.font.size = Pt(12)
        r_txt.font.color.rgb = RGBColor(0, 0, 0)
    return p

def add_numbered_point(doc, num_str, bold_prefix="", text="", space_after=3, line_spacing=1.5):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_before = Pt(1)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = line_spacing
    p.paragraph_format.left_indent = Inches(0.5)
    p.paragraph_format.first_line_indent = Inches(-0.25)
    
    r_num = p.add_run(num_str + "\t")
    r_num.font.name = "Times New Roman"
    r_num.font.size = Pt(12)
    r_num.font.bold = True
    r_num.font.color.rgb = RGBColor(0, 0, 0)
    
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = "Times New Roman"
        r_pre.font.size = Pt(12)
        r_pre.font.bold = True
        r_pre.font.color.rgb = RGBColor(0, 0, 0)
        
    if text:
        r_txt = p.add_run(text)
        r_txt.font.name = "Times New Roman"
        r_txt.font.size = Pt(12)
        r_txt.font.color.rgb = RGBColor(0, 0, 0)
    return p

def add_main_title(doc, text):
    # Main Title: 16 pt, bold, center-aligned
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(12)
    p.paragraph_format.line_spacing = 1.2
    p.paragraph_format.first_line_indent = Inches(0)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    r.font.name = "Times New Roman"
    r.font.size = Pt(16)
    r.font.bold = True
    r.font.color.rgb = RGBColor(0, 0, 0)
    return p

def add_heading_1(doc, text, alignment=WD_ALIGN_PARAGRAPH.CENTER):
    # Main Headings (Chapter titles): 14 pt, bold, center-aligned
    p = doc.add_paragraph()
    p.alignment = alignment
    p.paragraph_format.space_before = Pt(16)
    p.paragraph_format.space_after = Pt(10)
    p.paragraph_format.line_spacing = 1.2
    p.paragraph_format.first_line_indent = Inches(0)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    r.font.name = "Times New Roman"
    r.font.size = Pt(14)
    r.font.bold = True
    r.font.color.rgb = RGBColor(0, 0, 0)
    return p

def add_heading_2(doc, text):
    # Subheadings: 12 pt, bold, left-aligned
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.2
    p.paragraph_format.first_line_indent = Inches(0)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)
    r.font.bold = True
    r.font.color.rgb = RGBColor(0, 0, 0)
    return p

def add_heading_3(doc, text):
    # Subheadings: 12 pt, bold, left-aligned
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.2
    p.paragraph_format.first_line_indent = Inches(0)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)
    r.font.bold = True
    r.font.color.rgb = RGBColor(0, 0, 0)
    return p

def add_chapter_intro(doc, topic_summary):
    # "This chapter deals with ..." starting with tab blankspace (0.5")
    return add_p(doc, f"This chapter deals with {topic_summary}", 
                 font_size=12, alignment=WD_ALIGN_PARAGRAPH.JUSTIFY, 
                 space_before=4, space_after=12, line_spacing=1.5, tab_indent=True)

def add_table_data(doc, title, headers, rows, col_widths=None):
    # Caption: 11pt bold, left-aligned, keep_with_next
    p_cap = doc.add_paragraph()
    p_cap.paragraph_format.space_before = Pt(12)
    p_cap.paragraph_format.space_after = Pt(4)
    p_cap.paragraph_format.keep_with_next = True
    p_cap.paragraph_format.first_line_indent = Inches(0)
    p_cap.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r = p_cap.add_run(title)
    r.font.name = "Times New Roman"
    r.font.size = Pt(11)
    r.font.bold = True
    r.font.color.rgb = RGBColor(0, 0, 0)

    num_cols = len(headers)
    # Target printable area: 6.25 inches = 9000 dxa
    if col_widths and len(col_widths) == num_cols:
        col_dxas = [int(w.inches * 1440) for w in col_widths]
        # Ensure exact 9000 dxa sum
        diff = 9000 - sum(col_dxas)
        col_dxas[-1] += diff
    else:
        each = int(9000 / num_cols)
        col_dxas = [each] * num_cols
        col_dxas[-1] = 9000 - sum(col_dxas[:-1])
    total_dxa = sum(col_dxas)

    table = doc.add_table(rows=len(rows) + 1, cols=num_cols)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False

    tblPr = table._element.xpath('w:tblPr')[0]

    # Explicit table width in dxa
    for child in tblPr.findall(qn('w:tblW')):
        tblPr.remove(child)
    tblW = OxmlElement('w:tblW')
    tblW.set(qn('w:w'), str(total_dxa))
    tblW.set(qn('w:type'), 'dxa')
    tblPr.append(tblW)

    # Fixed layout
    for child in tblPr.findall(qn('w:tblLayout')):
        tblPr.remove(child)
    tblLayout = OxmlElement('w:tblLayout')
    tblLayout.set(qn('w:type'), 'fixed')
    tblPr.append(tblLayout)

    # Uniform cell margins at table level
    for child in tblPr.findall(qn('w:tblCellMar')):
        tblPr.remove(child)
    tblCellMar = OxmlElement('w:tblCellMar')
    for m, val in [('top', '70'), ('bottom', '70'), ('left', '100'), ('right', '100')]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), val)
        node.set(qn('w:type'), 'dxa')
        tblCellMar.append(node)
    tblPr.append(tblCellMar)

    # Clean borders
    for child in tblPr.findall(qn('w:tblBorders')):
        tblPr.remove(child)
    tblBorders = OxmlElement('w:tblBorders')
    for b_name in ['top', 'left', 'bottom', 'right']:
        b = OxmlElement(f'w:{b_name}')
        b.set(qn('w:val'), 'single')
        b.set(qn('w:sz'), '6')
        b.set(qn('w:space'), '0')
        b.set(qn('w:color'), '000000')
        tblBorders.append(b)
    for b_name in ['insideH', 'insideV']:
        b = OxmlElement(f'w:{b_name}')
        b.set(qn('w:val'), 'single')
        b.set(qn('w:sz'), '4')
        b.set(qn('w:space'), '0')
        b.set(qn('w:color'), '000000')
        tblBorders.append(b)
    tblPr.append(tblBorders)

    # Construct w:tblGrid
    tblGrid = OxmlElement('w:tblGrid')
    for dxa in col_dxas:
        gc = OxmlElement('w:gridCol')
        gc.set(qn('w:w'), str(dxa))
        tblGrid.append(gc)
    table._element.append(tblGrid)

    # Populate rows and cells
    for row_idx, row in enumerate(table.rows):
        trPr = row._element.get_or_add_trPr()
        trPr.append(OxmlElement('w:cantSplit'))
        if row_idx == 0:
            trPr.append(OxmlElement('w:tblHeader'))

        for c_idx, cell in enumerate(row.cells):
            tcPr = cell._element.get_or_add_tcPr()
            for child in tcPr.findall(qn('w:tcW')):
                tcPr.remove(child)
            tcW = OxmlElement('w:tcW')
            tcW.set(qn('w:w'), str(col_dxas[c_idx]))
            tcW.set(qn('w:type'), 'dxa')
            tcPr.append(tcW)

            set_cell_background(cell, "FFFFFF")

            p = cell.paragraphs[0]
            p.paragraph_format.first_line_indent = Inches(0)
            p.paragraph_format.space_before = Pt(1.5)
            p.paragraph_format.space_after = Pt(1.5)
            p.paragraph_format.line_spacing = 1.15

            if row_idx == 0:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                cell.text = headers[c_idx]
                p = cell.paragraphs[0]
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                p.paragraph_format.first_line_indent = Inches(0)
                for run in p.runs:
                    run.font.name = "Times New Roman"
                    run.font.size = Pt(10)
                    run.font.bold = True
                    run.font.color.rgb = RGBColor(0, 0, 0)
            else:
                data_val = rows[row_idx - 1][c_idx]
                cell.text = str(data_val)
                p = cell.paragraphs[0]
                p.paragraph_format.first_line_indent = Inches(0)
                p.paragraph_format.space_before = Pt(1.5)
                p.paragraph_format.space_after = Pt(1.5)
                p.paragraph_format.line_spacing = 1.15
                if c_idx == 0 and num_cols > 2 and len(str(data_val)) < 15:
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                else:
                    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                for run in p.runs:
                    run.font.name = "Times New Roman"
                    run.font.size = Pt(10)
                    run.font.color.rgb = RGBColor(0, 0, 0)

    p_after = doc.add_paragraph()
    p_after.paragraph_format.space_before = Pt(0)
    p_after.paragraph_format.space_after = Pt(6)
    p_after.paragraph_format.first_line_indent = Inches(0)

def add_borderless_table(doc, headers, rows, col_widths=None, bold_ch_only=True):
    num_cols = len(headers)
    if col_widths and len(col_widths) == num_cols:
        col_dxas = [int(w.inches * 1440) for w in col_widths]
        diff = 9000 - sum(col_dxas)
        col_dxas[-1] += diff
    else:
        each = int(9000 / num_cols)
        col_dxas = [each] * num_cols
        col_dxas[-1] = 9000 - sum(col_dxas[:-1])
    total_dxa = sum(col_dxas)

    table = doc.add_table(rows=len(rows) + 1, cols=num_cols)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False

    tblPr = table._element.xpath('w:tblPr')[0]
    for child in tblPr.findall(qn('w:tblW')):
        tblPr.remove(child)
    tblW = OxmlElement('w:tblW')
    tblW.set(qn('w:w'), str(total_dxa))
    tblW.set(qn('w:type'), 'dxa')
    tblPr.append(tblW)

    for child in tblPr.findall(qn('w:tblLayout')):
        tblPr.remove(child)
    tblLayout = OxmlElement('w:tblLayout')
    tblLayout.set(qn('w:type'), 'fixed')
    tblPr.append(tblLayout)

    for child in tblPr.findall(qn('w:tblCellMar')):
        tblPr.remove(child)
    tblCellMar = OxmlElement('w:tblCellMar')
    for m, val in [('top', '40'), ('bottom', '40'), ('left', '60'), ('right', '60')]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), val)
        node.set(qn('w:type'), 'dxa')
        tblCellMar.append(node)
    tblPr.append(tblCellMar)

    set_table_borders(table, color="FFFFFF", sz="0", val="none")

    tblGrid = OxmlElement('w:tblGrid')
    for dxa in col_dxas:
        gc = OxmlElement('w:gridCol')
        gc.set(qn('w:w'), str(dxa))
        tblGrid.append(gc)
    table._element.append(tblGrid)

    for row_idx, row in enumerate(table.rows):
        trPr = row._element.get_or_add_trPr()
        trPr.append(OxmlElement('w:cantSplit'))
        if row_idx == 0:
            trPr.append(OxmlElement('w:tblHeader'))

    # Header Row
    for i, h in enumerate(headers):
        cell = table.rows[0].cells[i]
        tcPr = cell._element.get_or_add_tcPr()
        for child in tcPr.findall(qn('w:tcW')):
            tcPr.remove(child)
        tcW = OxmlElement('w:tcW')
        tcW.set(qn('w:w'), str(col_dxas[i]))
        tcW.set(qn('w:type'), 'dxa')
        tcPr.append(tcW)

        cell.text = h
        set_cell_background(cell, "FFFFFF")
        p = cell.paragraphs[0]
        p.paragraph_format.first_line_indent = Inches(0)
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        if i == 0:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        elif i == 1:
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        else:
            p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        for run in p.runs:
            run.font.name = "Times New Roman"
            run.font.size = Pt(11)
            run.font.bold = True
            run.font.color.rgb = RGBColor(0, 0, 0)

    # Data Rows
    for r_idx, row_data in enumerate(rows):
        row_cells = table.rows[r_idx + 1].cells
        ch_val, tit_val, pg_val = row_data[0], row_data[1], row_data[2]
        
        is_bold = False
        if bold_ch_only:
            if ch_val != "" or tit_val in [
                "ABSTRACT", "ACKNOWLEDGEMENT", "LIST OF TABLES", "LIST OF FIGURES", 
                "REFERENCES", "APPENDIX 1: SAMPLE CODE", "PROJECT SCREENSHOTS", 
                "APPENDIX: SOURCE CODE", "SCREENSHOTS OF THE PROJECT"
            ]:
                is_bold = True
        
        for c_idx, val in enumerate(row_data):
            cell = row_cells[c_idx]
            tcPr = cell._element.get_or_add_tcPr()
            for child in tcPr.findall(qn('w:tcW')):
                tcPr.remove(child)
            tcW = OxmlElement('w:tcW')
            tcW.set(qn('w:w'), str(col_dxas[c_idx]))
            tcW.set(qn('w:type'), 'dxa')
            tcPr.append(tcW)

            cell.text = str(val)
            set_cell_background(cell, "FFFFFF")
            p = cell.paragraphs[0]
            p.paragraph_format.first_line_indent = Inches(0)
            p.paragraph_format.space_before = Pt(1)
            p.paragraph_format.space_after = Pt(1)
            p.paragraph_format.line_spacing = 1.05
            if c_idx == 0:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            elif c_idx == 1:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            for run in p.runs:
                run.font.name = "Times New Roman"
                run.font.size = Pt(10.5)
                run.font.bold = is_bold
                run.font.color.rgb = RGBColor(0, 0, 0)

    p_after = doc.add_paragraph()
    p_after.paragraph_format.space_before = Pt(0)
    p_after.paragraph_format.space_after = Pt(6)
    p_after.paragraph_format.first_line_indent = Inches(0)

def add_figure_image(doc, img_path, caption, max_width=5.8, max_height=4.2):
    if not os.path.exists(img_path):
        print(f"Warning: image {img_path} not found!")
        return

    im = Image.open(img_path)
    w, h = im.size
    aspect = w / h

    target_w = Inches(max_width)
    target_h = Inches(max_width / aspect)
    if target_h > Inches(max_height):
        target_h = Inches(max_height)
        target_w = Inches(max_height * aspect)

    p_img = doc.add_paragraph()
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img.paragraph_format.space_before = Pt(8)
    p_img.paragraph_format.space_after = Pt(3)
    p_img.paragraph_format.first_line_indent = Inches(0)
    p_img.paragraph_format.keep_with_next = True
    run_img = p_img.add_run()
    run_img.add_picture(img_path, width=target_w, height=target_h)

    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap.paragraph_format.space_before = Pt(2)
    p_cap.paragraph_format.space_after = Pt(10)
    p_cap.paragraph_format.first_line_indent = Inches(0)
    p_cap.paragraph_format.keep_with_next = False
    r_cap = p_cap.add_run(caption)
    r_cap.font.name = "Times New Roman"
    r_cap.font.size = Pt(10.5)
    r_cap.font.bold = True
    r_cap.font.color.rgb = RGBColor(0, 0, 0)

def add_algorithm_box(doc, algo_title, inputs, outputs, steps):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    set_table_borders(tbl, color="000000", sz="6", val="single")
    
    tblPr = tbl._element.xpath('w:tblPr')[0]
    for child in tblPr.findall(qn('w:tblW')):
        tblPr.remove(child)
    tblW = OxmlElement('w:tblW')
    tblW.set(qn('w:w'), '9000')
    tblW.set(qn('w:type'), 'dxa')
    tblPr.append(tblW)

    tblGrid = OxmlElement('w:tblGrid')
    gc = OxmlElement('w:gridCol')
    gc.set(qn('w:w'), '9000')
    tblGrid.append(gc)
    tbl._element.append(tblGrid)

    trPr = tbl.rows[0]._element.get_or_add_trPr()
    trPr.append(OxmlElement('w:cantSplit'))
    
    cell = tbl.rows[0].cells[0]
    tcPr = cell._element.get_or_add_tcPr()
    for child in tcPr.findall(qn('w:tcW')):
        tcPr.remove(child)
    tcW = OxmlElement('w:tcW')
    tcW.set(qn('w:w'), '9000')
    tcW.set(qn('w:type'), 'dxa')
    tcPr.append(tcW)

    set_cell_background(cell, "FFFFFF")
    set_cell_margins(cell, top=80, bottom=80, left=120, right=120)

    p_t = cell.paragraphs[0]
    p_t.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_t.paragraph_format.space_before = Pt(2)
    p_t.paragraph_format.space_after = Pt(4)
    p_t.paragraph_format.first_line_indent = Inches(0)
    p_t.paragraph_format.keep_with_next = True
    r_t = p_t.add_run(algo_title)
    r_t.font.name = "Times New Roman"
    r_t.font.size = Pt(11)
    r_t.font.bold = True
    r_t.font.color.rgb = RGBColor(0, 0, 0)

    p_io = cell.add_paragraph()
    p_io.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_io.paragraph_format.space_before = Pt(2)
    p_io.paragraph_format.space_after = Pt(4)
    p_io.paragraph_format.line_spacing = 1.15
    p_io.paragraph_format.first_line_indent = Inches(0)
    
    r_in = p_io.add_run("Input:  ")
    r_in.font.name = "Times New Roman"
    r_in.font.size = Pt(10)
    r_in.font.bold = True
    r_in.font.color.rgb = RGBColor(0, 0, 0)
    
    r_in_val = p_io.add_run(inputs + "\n")
    r_in_val.font.name = "Times New Roman"
    r_in_val.font.size = Pt(10)
    r_in_val.font.color.rgb = RGBColor(0, 0, 0)

    r_out = p_io.add_run("Output: ")
    r_out.font.name = "Times New Roman"
    r_out.font.size = Pt(10)
    r_out.font.bold = True
    r_out.font.color.rgb = RGBColor(0, 0, 0)
    
    r_out_val = p_io.add_run(outputs)
    r_out_val.font.name = "Times New Roman"
    r_out_val.font.size = Pt(10)
    r_out_val.font.color.rgb = RGBColor(0, 0, 0)

    for s_num, s_title, s_desc, s_formula in steps:
        p_step = cell.add_paragraph()
        p_step.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p_step.paragraph_format.space_before = Pt(3)
        p_step.paragraph_format.space_after = Pt(1)
        p_step.paragraph_format.line_spacing = 1.15
        p_step.paragraph_format.left_indent = Inches(0.25)
        p_step.paragraph_format.first_line_indent = Inches(-0.25)

        r_n = p_step.add_run(f"Step {s_num}: ")
        r_n.font.name = "Times New Roman"
        r_n.font.size = Pt(10)
        r_n.font.bold = True
        r_n.font.color.rgb = RGBColor(0, 0, 0)

        r_st = p_step.add_run(s_title + " — ")
        r_st.font.name = "Times New Roman"
        r_st.font.size = Pt(10)
        r_st.font.bold = True
        r_st.font.color.rgb = RGBColor(0, 0, 0)

        r_sd = p_step.add_run(s_desc)
        r_sd.font.name = "Times New Roman"
        r_sd.font.size = Pt(10)
        r_sd.font.color.rgb = RGBColor(0, 0, 0)

        if s_formula:
            p_form = cell.add_paragraph()
            p_form.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p_form.paragraph_format.left_indent = Inches(0.40)
            p_form.paragraph_format.first_line_indent = Inches(0)
            p_form.paragraph_format.space_before = Pt(1)
            p_form.paragraph_format.space_after = Pt(3)
            r_f = p_form.add_run(s_formula)
            r_f.font.name = "Consolas"
            r_f.font.size = Pt(9.5)
            r_f.font.bold = True
            r_f.font.color.rgb = RGBColor(0, 0, 0)

    p_end = doc.add_paragraph()
    p_end.paragraph_format.space_before = Pt(0)
    p_end.paragraph_format.space_after = Pt(6)
    p_end.paragraph_format.first_line_indent = Inches(0)

def add_code_block(doc, code_text, caption=""):
    # Plain black and white text, Consolas 10pt, left-aligned with proper indentation
    if caption:
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p_cap.paragraph_format.space_before = Pt(10)
        p_cap.paragraph_format.space_after = Pt(2)
        p_cap.paragraph_format.keep_with_next = True
        p_cap.paragraph_format.first_line_indent = Inches(0)
        r_cap = p_cap.add_run(caption)
        r_cap.font.name = "Times New Roman"
        r_cap.font.size = Pt(11)
        r_cap.font.bold = True
        r_cap.font.color.rgb = RGBColor(0, 0, 0)

    p_code = doc.add_paragraph()
    p_code.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_code.paragraph_format.space_before = Pt(2)
    p_code.paragraph_format.space_after = Pt(8)
    p_code.paragraph_format.line_spacing = 1.15
    p_code.paragraph_format.first_line_indent = Inches(0)
    p_code.paragraph_format.left_indent = Inches(0.2)
    run = p_code.add_run(code_text.strip())
    run.font.name = "Consolas"
    run.font.size = Pt(9.5)
    run.font.color.rgb = RGBColor(0, 0, 0)

def add_reference_item(doc, ref_num, authors, title, publication, extra=""):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.line_spacing = 1.3
    p.paragraph_format.left_indent = Inches(0.35)
    p.paragraph_format.first_line_indent = Inches(-0.35)

    r_num = p.add_run(f"[{ref_num}]\t")
    r_num.font.name = "Times New Roman"
    r_num.font.size = Pt(11)
    r_num.font.bold = True
    r_num.font.color.rgb = RGBColor(0, 0, 0)

    r_auth = p.add_run(authors + ", ")
    r_auth.font.name = "Times New Roman"
    r_auth.font.size = Pt(11)
    r_auth.font.color.rgb = RGBColor(0, 0, 0)

    r_tit = p.add_run(f'"{title}," ')
    r_tit.font.name = "Times New Roman"
    r_tit.font.size = Pt(11)
    r_tit.font.italic = True
    r_tit.font.color.rgb = RGBColor(0, 0, 0)

    r_pub = p.add_run(publication)
    r_pub.font.name = "Times New Roman"
    r_pub.font.size = Pt(11)
    r_pub.font.color.rgb = RGBColor(0, 0, 0)

    if extra:
        r_ex = p.add_run(", " + extra)
        r_ex.font.name = "Times New Roman"
        r_ex.font.size = Pt(11)
        r_ex.font.color.rgb = RGBColor(0, 0, 0)
    p.add_run(".")

def setup_footer(section):
    footer = section.footer
    footer.is_linked_to_previous = False
    p = footer.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.first_line_indent = Inches(0)
    run = p.add_run()
    run.font.name = "Times New Roman"
    run.font.size = Pt(11)
    run.font.color.rgb = RGBColor(0, 0, 0)

    fld1 = OxmlElement('w:fldChar')
    fld1.set(qn('w:fldCharType'), 'begin')
    instr = OxmlElement('w:instrText')
    instr.set(qn('xml:space'), 'preserve')
    instr.text = ' PAGE '
    fld2 = OxmlElement('w:fldChar')
    fld2.set(qn('w:fldCharType'), 'separate')
    fld3 = OxmlElement('w:fldChar')
    fld3.set(qn('w:fldCharType'), 'end')

    run._r.append(fld1)
    run._r.append(instr)
    run._r.append(fld2)
    run._r.append(fld3)

def setup_section_numbering(section, start_num=None, is_roman=False):
    sectPr = section._sectPr
    for child in sectPr.findall(qn('w:pgNumType')):
        sectPr.remove(child)
    pgNumType = OxmlElement('w:pgNumType')
    if is_roman:
        pgNumType.set(qn('w:fmt'), 'lowerRoman')
    else:
        pgNumType.set(qn('w:fmt'), 'decimal')
    if start_num is not None:
        pgNumType.set(qn('w:start'), str(start_num))
    sectPr.append(pgNumType)
