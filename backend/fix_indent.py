import os

filepath = r"C:\projects\VisionEdge\backend\routes\auth_routes.py"
with open(filepath, "r") as f:
    lines = f.readlines()

new_lines = []
in_func = False

for line in lines:
    if line.startswith("def "):
        in_func = True
        new_lines.append(line)
    elif line.startswith("# =================================================="):
        in_func = False
        new_lines.append(line)
    elif line.startswith("@"):
        in_func = False
        new_lines.append(line)
    else:
        if in_func and line != "\n":
            new_lines.append("    " + line)
        else:
            new_lines.append(line)

with open(filepath, "w") as f:
    f.writelines(new_lines)
print("Indentation fixed.")
