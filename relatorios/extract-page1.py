import fitz  # PyMuPDF
doc = fitz.open("relatorios/18-08-2026-analise-fabrica-agentica.pdf")
page = doc[0]
pix = page.get_pixmap(dpi=150)
pix.save("relatorios/page1_preview.png")
print(f"Salvo: relatorios/page1_preview.png ({pix.width}x{pix.height}px, {pix.width*pix.height/1e6:.1f}MP)")
doc.close()