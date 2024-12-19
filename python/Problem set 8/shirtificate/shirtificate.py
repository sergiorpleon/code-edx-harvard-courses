import sys
from fpdf import FPDF


def main():
    name = input("Name: ")

    pdf = FPDF(orientation="portrait", format="A4")
    pdf.set_page_background((252,255,255))

    pdf.add_page(same=True)

    pdf.set_margin(20)
    pdf.image('shirtificate.png', y=30, dims=(500,500))

    pdf.set_font('helvetica', 'B', 22.0)
    pdf.set_text_color( 255, 255, 255)
    text = F"{name} took CS50"
    pdf.cell(align='C', h=120, w=0, text=text, border=0)

    pdf.output("shirtificate.pdf")


if __name__ == "__main__":
    main()
