import os
import re
from fpdf import FPDF

class Seq_PDF(FPDF):
    def header(self):
        if self.page_no() > 1:
            self.set_font('Arial', 'I', 9)
            self.set_text_color(100, 100, 100)
            self.cell(0, 10, 'Sequence Diagram Specification - VisionEdge v1.0', 0, 0, 'R')
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
    md_path = r'c:\projects\VisionEdge\VisionEdge_Sequence_Diagram_Doc.md'
    pdf_path = r'c:\projects\VisionEdge\VisionEdge_Sequence_Diagram_Doc.pdf'

    with open(md_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    pdf = Seq_PDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    # --- COVER PAGE ---
    pdf.add_page()
    pdf.ln(40)
    pdf.set_font('Arial', 'B', 24)
    pdf.set_text_color(24, 76, 120) # Blue title
    pdf.cell(0, 15, clean_text('Sequence Diagram Specification'), 0, 1, 'C')
    
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
    pdf.cell(0, 8, clean_text('File Created: visionedge_sequence_diagram.drawio'), 0, 1, 'C')
    pdf.cell(0, 8, clean_text('Theme: White Background, Black Typography (#000000)'), 0, 1, 'C')
    pdf.cell(0, 8, clean_text('Date: August 2026'), 0, 1, 'C')

    # --- BODY PAGES ---
    pdf.add_page()
    
    in_table = False
    table_data = []
    in_code_block = False

    for line in lines:
        line_str = clean_text(line.strip())
        
        if line_str.startswith('```'):
            in_code_block = not in_code_block
            continue

        if in_code_block:
            pdf.set_font('Courier', '', 8)
            pdf.set_text_color(30, 41, 59)
            pdf.multi_cell(0, 4, line_str)
            continue
        
        if line_str.startswith('# '):
            if in_table:
                render_table(pdf, table_data)
                in_table = False
                table_data = []
            pdf.ln(6)
            pdf.set_font('Arial', 'B', 16)
            pdf.set_text_color(24, 76, 120)
            pdf.cell(0, 10, line_str[2:], 0, 1, 'L')
            pdf.ln(2)
        elif line_str.startswith('## '):
            if in_table:
                render_table(pdf, table_data)
                in_table = False
                table_data = []
            pdf.ln(4)
            pdf.set_font('Arial', 'B', 14)
            pdf.set_text_color(30, 41, 59)
            pdf.cell(0, 8, line_str[3:], 0, 1, 'L')
            pdf.ln(2)
        elif line_str.startswith('### '):
            if in_table:
                render_table(pdf, table_data)
                in_table = False
                table_data = []
            pdf.ln(3)
            pdf.set_font('Arial', 'B', 12)
            pdf.set_text_color(51, 65, 85)
            pdf.cell(0, 7, line_str[4:], 0, 1, 'L')
            pdf.ln(1)
        elif line_str.startswith('|'):
            in_table = True
            cells = [c.strip() for c in line_str.split('|')[1:-1]]
            if not all(set(c).issubset({'-', ':', ' '}) for c in cells):
                table_data.append(cells)
        else:
            if in_table:
                render_table(pdf, table_data)
                in_table = False
                table_data = []

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

    if in_table:
        render_table(pdf, table_data)

    pdf.output(pdf_path)
    print(f"Successfully generated Sequence Diagram PDF at: {pdf_path}")

def render_table(pdf, table_data):
    if not table_data:
        return
    
    pdf.ln(2)
    num_cols = len(table_data[0])
    page_width = 180
    
    if num_cols == 5:
        col_widths = [15, 30, 35, 50, 50]
    elif num_cols == 3:
        col_widths = [35, 45, 100]
    elif num_cols == 2:
        col_widths = [45, 135]
    else:
        col_widths = [page_width / num_cols] * num_cols

    # Header Row
    pdf.set_font('Arial', 'B', 8.5)
    pdf.set_fill_color(24, 76, 120)
    pdf.set_text_color(255, 255, 255)
    
    headers = table_data[0]
    for i, h in enumerate(headers):
        w = col_widths[i] if i < len(col_widths) else col_widths[-1]
        h_clean = re.sub(r'\*\*(.*?)\*\*', r'\1', h)
        pdf.cell(w, 6, h_clean, 1, 0, 'C', fill=True)
    pdf.ln()

    # Data Rows
    pdf.set_font('Arial', '', 7.5)
    pdf.set_text_color(40, 40, 40)
    pdf.set_fill_color(245, 247, 250)

    for row_idx, row in enumerate(table_data[1:]):
        fill = (row_idx % 2 == 1)
        lines_needed = 1
        for i, cell in enumerate(row):
            w = col_widths[i] if i < len(col_widths) else col_widths[-1]
            cell_clean = re.sub(r'\*\*(.*?)\*\*', r'\1', cell)
            cell_clean = re.sub(r'`(.*?)`', r'\1', cell_clean)
            lines = pdf.get_string_width(cell_clean) / (w - 2)
            lines_needed = max(lines_needed, int(lines) + 1)
        
        row_height = max(5.5, lines_needed * 4)
        
        if pdf.get_y() + row_height > 270:
            pdf.add_page()
            pdf.set_font('Arial', 'B', 8.5)
            pdf.set_fill_color(24, 76, 120)
            pdf.set_text_color(255, 255, 255)
            for i, h in enumerate(headers):
                w = col_widths[i] if i < len(col_widths) else col_widths[-1]
                h_clean = re.sub(r'\*\*(.*?)\*\*', r'\1', h)
                pdf.cell(w, 6, h_clean, 1, 0, 'C', fill=True)
            pdf.ln()
            pdf.set_font('Arial', '', 7.5)
            pdf.set_text_color(40, 40, 40)

        x_start = pdf.get_x()
        y_start = pdf.get_y()

        for i, cell in enumerate(row):
            w = col_widths[i] if i < len(col_widths) else col_widths[-1]
            cell_clean = re.sub(r'\*\*(.*?)\*\*', r'\1', cell)
            cell_clean = re.sub(r'`(.*?)`', r'\1', cell_clean)
            
            pdf.set_xy(x_start + sum(col_widths[:i]), y_start)
            pdf.multi_cell(w, 4, cell_clean, border=1, align='L', fill=fill)
        
        pdf.set_xy(x_start, y_start + row_height)

    pdf.ln(3)

if __name__ == '__main__':
    generate_pdf()
