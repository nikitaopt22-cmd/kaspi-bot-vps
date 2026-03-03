from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm

def build_a4_layout(input_pdfs, output_path, per_page=4, page_width_mm=210):
    c = canvas.Canvas(output_path, pagesize=A4)
    W, H = A4
    margin = 10 * mm
    y = H - margin
    count = 0
    for p in input_pdfs:
        c.setFont("Helvetica", 10)
        c.drawString(margin, y, f"Накладная: {p}")
        y -= 12
        count += 1
        if count >= per_page:
            c.showPage()
            y = H - margin
            count = 0
    if count != 0:
        c.showPage()
    c.save()
