"""Builds qr/art-NN.png and qr/print-labels-A4.pdf from the data in index.html.
Run from the repo root:  python3 tools/make_labels.py
Needs: node, pip install "qrcode[pil]" reportlab
"""
import json, subprocess, os, re
import qrcode
from qrcode.constants import ERROR_CORRECT_Q
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

BASE = "https://kanaan-dvlps.github.io/art-exhibition/"
html = open("index.html", encoding="utf-8").read()
data = html[html.index("// ===== EDIT HERE"):html.index("// ===== END EDIT")]
js = data + "\nconsole.log(JSON.stringify({EXHIBITION, WORKS}));"
d = json.loads(subprocess.check_output(["node", "-e", js]))
EX, WORKS = d["EXHIBITION"], d["WORKS"]

os.makedirs("qr", exist_ok=True)
pngs = []
for i in range(len(WORKS)):
    q = qrcode.QRCode(error_correction=ERROR_CORRECT_Q, box_size=20, border=4)
    q.add_data(f"{BASE}#art-{i+1:02d}"); q.make(fit=True)
    p = f"qr/art-{i+1:02d}.png"; q.make_image().convert("1").save(p, optimize=True); pngs.append(p)

def kr(n): return f"{n:,}".replace(",", " ") + " kr"
def fit(c, text, font, size, maxw):
    while c.stringWidth(text, font, size) > maxw and size > 6: size -= 0.25
    return size

INK, MUTED, ACCENT, RULE = (0.086, 0.094, 0.114), (0.36, 0.38, 0.42), (0.12, 0.25, 0.72), (0.8, 0.8, 0.78)
c = canvas.Canvas("qr/print-labels-A4.pdf", pagesize=A4); W, H = A4
lw, lh = 95*mm, 68*mm; mx, my = (W - 2*lw)/2, (H - 4*lh)/2
for i, w in enumerate(WORKS):
    k = i % 8
    if i and k == 0: c.showPage()
    x = mx + (k % 2)*lw; y = H - my - (k//2 + 1)*lh
    c.setStrokeColorRGB(*RULE); c.setLineWidth(.3); c.setDash(1, 3); c.rect(x, y, lw, lh); c.setDash()
    p = 6*mm; qs = 34*mm; qx = x + lw - p - qs + 2.5*mm
    tx = x + p; top = y + lh - p; textw = qx - tx - 1*mm
    c.setFillColorRGB(*MUTED); c.setFont("Helvetica-Bold", 6.2)
    c.drawString(tx, top - 2*mm, f"{EX['sv']['name'].upper()}  ·  {EX['en']['name'].upper()}")
    c.setStrokeColorRGB(*INK); c.setLineWidth(.8); c.line(tx, top - 4*mm, x + lw - p, top - 4*mm)
    c.drawImage(ImageReader(pngs[i]), qx, top - 6*mm - qs, qs, qs)
    c.setFillColorRGB(*ACCENT); c.setFont("Helvetica-Bold", 22); c.drawString(tx, top - 13.5*mm, f"{i+1:02d}")
    en, sv = w["en"]["title"], w["sv"]["title"]
    c.setFillColorRGB(*INK)
    s = fit(c, en, "Helvetica-Bold", 11, textw); c.setFont("Helvetica-Bold", s); c.drawString(tx, top - 20.5*mm, en)
    s = fit(c, sv, "Helvetica", 10, textw); c.setFont("Helvetica", s); c.drawString(tx, top - 25.5*mm, sv)
    c.setFillColorRGB(*MUTED); c.setFont("Helvetica", 8.5); c.drawString(tx, top - 31.5*mm, f"{w['artist']}, {w['year']}")
    med = f"{w['en']['medium']} / {w['sv']['medium']}"
    s = fit(c, med, "Helvetica", 7.5, textw); c.setFont("Helvetica", s); c.drawString(tx, top - 35.5*mm, med)
    c.setFont("Helvetica", 7.5); c.drawString(tx, top - 39.5*mm, w["size"])
    # bottom band: price left, call to action right
    by = y + p
    c.setStrokeColorRGB(*RULE); c.setLineWidth(.4); c.line(tx, by + 9*mm, x + lw - p, by + 9*mm)
    c.setFillColorRGB(*INK) if w["price"] is not None else c.setFillColorRGB(0.64, 0.15, 0.11)
    c.setFont("Helvetica-Bold", 11); c.drawString(tx, by + 2.5*mm, kr(w["price"]) if w["price"] is not None else "Såld / Sold")
    c.setFillColorRGB(*INK); c.setFont("Helvetica-Bold", 7.5); c.drawRightString(x + lw - p, by + 4.6*mm, "Scan for the story →")
    c.setFont("Helvetica", 7.5); c.drawRightString(x + lw - p, by + 1*mm, "Skanna för berättelsen →")
c.save()
print(f"{len(WORKS)} labels, {len(pngs)} QR codes")
