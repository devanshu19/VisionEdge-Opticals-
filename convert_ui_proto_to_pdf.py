import os
import re
from fpdf import FPDF

class UI_PDF(FPDF):
    def header(self):
        if self.page_no() > 1:
            self.set_font('Arial', 'I', 9)
            self.set_text_color(100, 100, 100)
            self.cell(0, 10, 'Original UI Prototypes Specification - VisionEdge v1.0', 0, 0, 'R')
            self.ln(12)

    def footer(self):
        if self.page_no() > 1:
            self.set_y(-15)
            self.set_font('Arial', 'I', 9)
            self.set_text_color(100, 100, 100)
            self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def clean_text(text):
    text = text.replace('–', '-').replace('—', '-').replace('…', '...')
    text = text.replace('“', '"').replace('”', '"').replace('’', "'").replace('‘', "'")
    text = text.replace('≥', '>=').replace('≤', '<=').replace('→', '->')
    text = text.replace('\u2265', '>=').replace('\u2264', '<=').replace('\u2192', '->')
    return text.encode('latin-1', 'replace').decode('latin-1')

def generate_pdf():
    md_path = r'c:\projects\VisionEdge\VisionEdge_UI_Prototypes.md'
    pdf_path = r'c:\projects\VisionEdge\VisionEdge_UI_Prototypes.pdf'

    with open(md_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    pdf = UI_PDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    # --- COVER PAGE ---
    pdf.add_page()
    pdf.ln(40)
    pdf.set_font('Arial', 'B', 24)
    pdf.set_text_color(24, 76, 120) # Blue title
    pdf.cell(0, 15, clean_text('UI Prototypes Specification'), 0, 1, 'C')
    
    pdf.set_font('Arial', 'I', 14)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 10, clean_text('for'), 0, 1, 'C')
    pdf.ln(5)

    pdf.set_font('Arial', 'B', 18)
    pdf.set_text_color(30, 41, 59)
    pdf.multi_cell(0, 10, clean_text('VisionEdge: AI-Powered Optical Store Management & Virtual Try-On System'), 0, 'C')
    pdf.ln(40)

    pdf.set_font('Arial', '', 12)
    pdf.set_text_color(50, 50, 50)
    pdf.cell(0, 8, clean_text('Version 1.0'), 0, 1, 'C')
    pdf.cell(0, 8, clean_text('Design System: Bootstrap 5.3 + Custom CSS Variables + Dark/Light Mode'), 0, 1, 'C')
    pdf.cell(0, 8, clean_text('Interactions: MediaPipe Computer Vision, Canvas API, AOS, Swiper'), 0, 1, 'C')
    pdf.cell(0, 8, clean_text('Date: August 2026'), 0, 1, 'C')

    # --- BODY PAGES ---
    pdf.add_page()
    
    in_code_block = False

    for line in lines:
        line_str = clean_text(line.rstrip())
        
        if line_str.startswith('```'):
            in_code_block = not in_code_block
            if in_code_block:
                pdf.ln(2)
                pdf.set_font('Courier', '', 7.5)
                pdf.set_text_color(30, 41, 59)
            else:
                pdf.ln(3)
            continue

        if in_code_block:
            pdf.cell(0, 3.8, line_str, 0, 1, 'L')
            continue
        
        if line_str.startswith('# '):
            pdf.ln(6)
            pdf.set_font('Arial', 'B', 16)
            pdf.set_text_color(24, 76, 120)
            pdf.cell(0, 10, line_str[2:], 0, 1, 'L')
            pdf.ln(2)
        elif line_str.startswith('## '):
            pdf.ln(4)
            pdf.set_font('Arial', 'B', 14)
            pdf.set_text_color(30, 41, 59)
            pdf.cell(0, 8, line_str[3:], 0, 1, 'L')
            pdf.ln(2)
        elif line_str.startswith('### '):
            pdf.ln(3)
            pdf.set_font('Arial', 'B', 12)
            pdf.set_text_color(51, 65, 85)
            pdf.cell(0, 7, line_str[4:], 0, 1, 'L')
            pdf.ln(1)
        elif line_str.startswith('#### '):
            pdf.ln(2)
            pdf.set_font('Arial', 'BI', 11)
            pdf.set_text_color(71, 85, 105)
            pdf.cell(0, 6, line_str[5:], 0, 1, 'L')
        else:
            if line_str == '---' or line_str == '':
                pdf.ln(2)
                continue
            
            pdf.set_font('Arial', '', 10)
            pdf.set_text_color(50, 50, 50)
            
            cleaned_line = re.sub(r'\*\*(.*?)\*\*', r'\1', line_str)
            cleaned_line = re.sub(r'\*(.*?)\*', r'\1', cleaned_line)
            cleaned_line = re.sub(r'`(.*?)`', r'\1', cleaned_line)
            
            if cleaned_line.startswith('* ') or cleaned_line.startswith('- '):
                pdf.set_x(15)
                pdf.cell(5, 5, chr(149), 0, 0)
                pdf.multi_cell(0, 5, cleaned_line[2:])
            else:
                pdf.multi_cell(0, 5, cleaned_line)
            pdf.ln(1)

    pdf.output(pdf_path)
    print(f"Successfully generated UI Prototypes PDF at: {pdf_path}")

if __name__ == '__main__':
    generate_pdf()
