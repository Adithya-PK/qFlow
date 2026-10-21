with open(r'c:\Projects\QFlow\scripts\build_full_report_docx.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
i = 0
while i < len(lines):
    line = lines[i]
    if 'HEAD OF THE DEPARTMENT' in line and not line.strip().endswith(';'):
        new_lines.append('    r_c1_h = p_c1.add_run("HEAD OF THE DEPARTMENT\\nDr. T. Kalai Selvi\\n")\n')
        i += 3
        continue
    if 'Easwari Engineering College,' in line and i + 1 < len(lines) and 'Ramapuram' in lines[i+1]:
        new_lines.append('    r_c1_d = p_c1.add_run("Easwari Engineering College,\\nRamapuram, Chennai – 600089.")\n')
        i += 2
        continue
    if 'SUPERVISOR' in line and not line.strip().endswith(';'):
        new_lines.append('    r_c2_h = p_c2.add_run("SUPERVISOR\\nMs. D. S. K. Harshitha\\n")\n')
        i += 3
        continue
    if 'Internal Examiner' in line and i + 1 < len(lines) and 'Date:' in lines[i+1]:
        new_lines.append('    r_v1 = p_v1.add_run("Internal Examiner\\nDate:")\n')
        i += 2
        continue
    new_lines.append(line)
    i += 1

with open(r'c:\Projects\QFlow\scripts\build_full_report_docx.py', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print('Lines normalized successfully!')
