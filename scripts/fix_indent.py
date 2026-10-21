report_path = r"c:\Projects\QFlow\scripts\build_full_report_docx.py"
with open(report_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if line.startswith("toc_data = ["):
        new_lines.append("    " + line)
    elif line.startswith("tables_list = ["):
        new_lines.append("    " + line)
    elif line.startswith("figures_list = ["):
        new_lines.append("    " + line)
    else:
        new_lines.append(line)

with open(report_path, "w", encoding="utf-8") as f:
    f.writelines(new_lines)

print("Indentation fixed successfully!")
