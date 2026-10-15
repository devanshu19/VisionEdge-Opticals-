import os
import glob

directory = r"C:\projects\VisionEdge\frontend\admin"

html_files = glob.glob(os.path.join(directory, "*.html"))

for file in html_files:
    if "login.html" in file or "index.html" in file:
        continue
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if '<script src="assets/js/auth.js"></script>' not in content:
        content = content.replace('<script src="assets/js/app.js"></script>', '<script src="assets/js/auth.js"></script>\n    <script src="assets/js/app.js"></script>')
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {file}")
