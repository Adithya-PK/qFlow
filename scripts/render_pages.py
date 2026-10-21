import fitz # PyMuPDF
import os

pdf_path = r"c:\Projects\QFlow\QFLOW_PROJECT_REPORT.pdf"
doc = fitz.open(pdf_path)
print(f"Total pages in PDF: {len(doc)}")

out_dir = r"c:\Projects\QFlow\rendered_check"
os.makedirs(out_dir, exist_ok=True)

# Render pages: 2 (Bonafide), 3 (Viva-Voce), 9 (Chapter 1), and find Table 4.1
pages_to_render = [1, 2, 8] # 0-indexed: 1 = page 2, 2 = page 3, 8 = page 9

# Find page with Table 4.1
for idx, page in enumerate(doc):
    txt = page.get_text()
    if "Table 4.1" in txt or "REST API Endpoints" in txt:
        pages_to_render.append(idx)
        print(f"Found Table 4.1 on page {idx+1}")
        break

for page_idx in pages_to_render:
    page = doc[page_idx]
    pix = page.get_pixmap(dpi=150)
    out_file = os.path.join(out_dir, f"page_{page_idx+1}.png")
    pix.save(out_file)
    print(f"Rendered page {page_idx+1} to {out_file}")
