"""Entrance poster: one QR that opens the home page (all works).
Run from the repo root:  python3 tools/make_poster.py
"""
import qrcode
from qrcode.constants import ERROR_CORRECT_Q
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

URL = "https://kanaan-dvlps.github.io/art-exhibition/"
q = qrcode.QRCode(error_correction=ERROR_CORRECT_Q, box_size=24, border=2); q.add_data(URL); q.make(fit=True)
q.make_image().convert("1").save("qr/entrance.png", optimize=True)

INK, MUTED, ACCENT = (0.082, 0.086, 0.075), (0.33, 0.35, 0.31), (0.18, 0.36, 0.27)
W, H = A4; c = canvas.Canvas("qr/entrance-poster-A4.pdf", pagesize=A4); cx = W / 2
c.setFillColorRGB(0.969, 0.969, 0.957); c.rect(0, 0, W, H, stroke=0, fill=1)
c.setFillColorRGB(*MUTED); c.setFont("Helvetica-Bold", 11)
c.drawCentredString(cx, H - 30*mm, "MAHSHAD PARSI NEZHAD  ·  2026")
c.setFillColorRGB(*INK); c.setFont("Times-Roman", 84); c.drawCentredString(cx, H - 62*mm, "First Life")
c.setFillColorRGB(*MUTED); c.setFont("Helvetica", 15)
c.drawCentredString(cx, H - 76*mm, "Welcome  ·  Välkommen")
qs = 120*mm; qy = H - 88*mm - qs
c.setFillColorRGB(1, 1, 1); c.roundRect(cx - qs/2 - 8*mm, qy - 8*mm, qs + 16*mm, qs + 16*mm, 6*mm, stroke=0, fill=1)
c.drawImage(ImageReader("qr/entrance.png"), cx - qs/2, qy, qs, qs)
c.setFillColorRGB(*ACCENT); c.setFont("Helvetica-Bold", 22)
c.drawCentredString(cx, qy - 24*mm, "Scan to explore all works")
c.setFont("Helvetica", 20); c.drawCentredString(cx, qy - 33*mm, "Skanna för att utforska alla verk")
c.setFillColorRGB(*MUTED); c.setFont("Helvetica", 11)
c.drawCentredString(cx, qy - 45*mm, "Use your phone camera. No app needed.  ·  Använd mobilkameran. Ingen app behövs.")
c.drawCentredString(cx, 16*mm, URL.replace("https://", ""))
c.save(); print("poster ok")
