import os
import re
from fpdf import FPDF
from pathlib import Path

class ReportPDF(FPDF):
    def header(self):
        # Set font
        self.set_font('Malgun', '', 10)
        # Move to the right
        self.cell(0, 10, '글로벌 AI 콘텐츠 플랫폼 전략 리포트', 0, 0, 'R')
        self.ln(10)

    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Set font
        self.set_font('Malgun', '', 8)
        # Page number
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def parse_markdown_table(lines, start_index):
    table_data = []
    i = start_index
    while i < len(lines) and '|' in lines[i]:
        row = [cell.strip() for cell in lines[i].split('|') if cell.strip()]
        if row and not all(re.match(r'[-:| ]+', cell) for cell in row):
            table_data.append(row)
        i += 1
    return table_data, i

def create_improved_pdf(md_path, pdf_path):
    md_content = Path(md_path).read_text(encoding='utf-8')
    lines = md_content.splitlines()
    
    pdf = ReportPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Use Malgun Gothic
    font_path = r"C:\Windows\Fonts\malgun.ttf"
    pdf.add_font("Malgun", "", font_path)
    
    pdf.add_page()
    pdf.set_font("Malgun", size=11)
    
    col_width = pdf.epw # effective page width
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        if not line:
            pdf.ln(5)
            i += 1
            continue
            
        if line.startswith('## '):
            pdf.ln(5)
            pdf.set_font("Malgun", size=16)
            pdf.multi_cell(col_width, 12, line[3:], border=0, align='L')
            pdf.set_font("Malgun", size=11)
            i += 1
        elif line.startswith('### '):
            pdf.ln(3)
            pdf.set_font("Malgun", size=14)
            pdf.multi_cell(col_width, 10, line[4:], border=0, align='L')
            pdf.set_font("Malgun", size=11)
            i += 1
        elif line.startswith('#### '):
            pdf.set_font("Malgun", size=12)
            pdf.multi_cell(col_width, 8, line[5:], border=0, align='L')
            pdf.set_font("Malgun", size=11)
            i += 1
        elif line.startswith('|'):
            table_data, next_i = parse_markdown_table(lines, i)
            if table_data:
                pdf.ln(2)
                try:
                    with pdf.table(borders_layout="SINGLE_TOP_LINE", cell_fill_color=(240, 240, 240), cell_fill_mode="ROWS", text_align="LEFT") as table:
                        for row in table_data:
                            row_cells = table.row()
                            for cell in row:
                                row_cells.cell(cell)
                except:
                    # Fallback for weird table rows
                    for row in table_data:
                        pdf.write(7, " | ".join(row) + "\n")
                pdf.ln(2)
            i = next_i
        elif line.startswith('```'):
            i += 1
            code_lines = []
            while i < len(lines) and not lines[i].strip().startswith('```'):
                code_lines.append(lines[i])
                i += 1
            if code_lines:
                pdf.set_fill_color(245, 245, 245)
                pdf.set_font("Malgun", size=10)
                pdf.multi_cell(col_width, 6, "\n".join(code_lines), border=1, fill=True)
                pdf.set_font("Malgun", size=11)
            i += 1
        elif line.startswith('- '):
            pdf.write(7, "  • " + line[2:] + "\n")
            i += 1
        else:
            pdf.write(7, line + "\n")
            i += 1
            
    pdf.output(pdf_path)
    print(f"Improved PDF saved to: {pdf_path}")

if __name__ == "__main__":
    src = r"E:\Mywork\AI\AI컨텐츠제작\글로벌 AI 콘텐츠 플랫폼 마케팅 및 미국 상장 전략.md"
    dst = r"C:\Users\JayPark1004\.openclaw\workspace\US_Beauty_Strategy_Final.pdf"
    create_improved_pdf(src, dst)
