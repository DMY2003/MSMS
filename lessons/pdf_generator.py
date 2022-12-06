import time
from reportlab.lib.pagesizes import A5, landscape
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from lessons.models import Invoice
from reportlab.platypus.paragraph import stringWidth


def generate_invoice_PDF(invoice_id, student, teacher, instrument, lesson_date, price, base_in=canvas):
    """
    Generate invoice PDF

    @param:
    student = [id, first name, last name, email]
    teacher = [first name, last name]
    """
    # Details
    invoice_ref_id = str(student[0]) + "-" + str(invoice_id)
    date = time.strftime("%d/%m/%Y")

    # PDF generation
    padding = 1.5 * cm
    height, width = A5
    base = base_in.Canvas(student[1] + "_" +
                          student[2] + "_Invoice_" +
                          invoice_ref_id + ".pdf", pagesize=landscape(A5))

    base.setFont('Helvetica-Bold', 18)
    base.drawRightString(width - padding, 380 - 50, "INVOICE")
    base.drawString(padding, 380 - 50, "MSMS")
    base.setFont('Helvetica', 14)
    base.drawString(padding, 360 - 50, "billing@msms.org")
    base.drawRightString(width - padding - stringWidth(date, "Helvetica", 14), 360 - 50, "Date:  ")
    base.drawRightString(width - padding, 360 - 50, date)
    base.drawRightString(width - padding - stringWidth(invoice_ref_id, "Helvetica", 14), 340 - 50, "Invoice ID:   ")
    base.drawRightString(width - padding, 340 - 50, invoice_ref_id)
    base.setLineWidth(.5)
    base.line(padding - 5, 330 - 50, width - padding + 5, 330 - 50)

    base.setFont('Helvetica-Bold', 14)
    base.drawString(padding, 310 - 50, "Billed To:")
    base.setFont('Helvetica', 12)
    base.drawString(padding, 295 - 50, student[1] + " " + student[2])
    base.drawString(padding, 280 - 50, student[3])
    base.setLineWidth(.5)
    base.line(padding - 5, 265 - 50, width - padding + 5, 265 - 50)

    base.setFont('Helvetica-Bold', 14)
    base.drawString(padding, 245 - 50, "Description:")
    base.drawRightString(width - padding, 245 - 50, "Ammount")
    base.setLineWidth(.5)
    base.line(padding - 5, 230 - 50, width - padding + 5, 230 - 50)

    base.setFont('Helvetica', 12)
    base.drawString(padding, 200 - 50, "1x " + instrument + " lesson on")
    base.drawString(padding, 185 - 50, str(lesson_date))
    base.drawString(padding, 170 - 50, "with " + teacher[0] + " " + teacher[1])
    base.drawRightString(width - padding - (stringWidth(str("Amount"), "Helvetica", 12) / 2), 185 - 50,
                         "£" + str(price))

    base.save()
