with open(r'c:\Projects\QFlow\scripts\build_full_report_docx.py', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('r_c2_d = p_c2.add_run("Easwari Engineering College,', 'r_c1_d = p_c1.add_run("Easwari Engineering College,', 1)

with open(r'c:\Projects\QFlow\scripts\build_full_report_docx.py', 'w', encoding='utf-8') as f:
    f.write(text)

print('Fixed successfully!')
