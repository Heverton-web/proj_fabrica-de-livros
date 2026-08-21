#!/usr/bin/env python3
"""Gera capa moderna para o relatório de análise, usando Pillow."""

from PIL import Image, ImageDraw, ImageFont
import os
import sys
from pathlib import Path

# Configuração da capa — padrão visual da Fábrica Agêntica
LARGURA = 1600
ALTURA = 2263
COR_FUNDO = (7, 9, 15, 255)       # #07090f
COR_ACCENT = (88, 166, 255, 255)  # #58a6ff
COR_ACCENT_DARK = (55, 195, 214, 255)  # #37c3d6
COR_PRIMAria = (124, 58, 237, 255)  # #7c3aed
COR_TEXTO_BRANCO = (240, 246, 252, 255)
COR_TEXTO_GRAY = (139, 148, 158, 255)

# Ancorado na raiz do projeto (nunca na CWD) — evita criar `relatorios/`
# solto onde quer que o script seja invocado (ex.: de dentro de output/<hub>/).
DIR_RELATORIOS = str(Path(__file__).resolve().parent.parent / "relatorios")
os.makedirs(f"{DIR_RELATORIOS}/imagens", exist_ok=True)

# Criar imagem base
img = Image.new('RGBA', (LARGURA, ALTURA), COR_FUNDO)
draw = ImageDraw.Draw(img)

# Gradiente de fundo sutil
for i in range(ALTURA):
    t = i / ALTURA
    r = int(7 + (10 - 7) * t)
    g = int(9 + (12 - 9) * t)
    b = int(15 + (20 - 15) * t)
    draw.line([(0, i), (LARGURA, i)], fill=(r, g, b, 255))

# Grid perspectivo
grid_color = (168, 85, 247, int(255 * 0.06))
for x in range(0, LARGURA, 80):
    draw.line([(x, 0), (x, ALTURA)], fill=grid_color, width=1)
for y in range(0, ALTURA, 80):
    draw.line([(0, y), (LARGURA, y)], fill=grid_color, width=1)

# Glow radial no centro-superior
glow = Image.new('RGBA', (LARGURA, ALTURA), (0, 0, 0, 0))
glow_draw = ImageDraw.Draw(glow)
for i in range(50, 0, -1):
    alpha = int(255 * 0.18 * (1 - i / 50))
    radius = max(10, 700 - i * 12)
    cx = LARGURA // 2
    cy = 200
    glow_draw.ellipse(
        [cx - radius, cy - radius, cx + radius, cy + radius],
        fill=(168, 85, 247, alpha)
    )
img = Image.alpha_composite(img, glow)
draw = ImageDraw.Draw(img)

# Glow sutil no rodapé
glow_bottom = Image.new('RGBA', (LARGURA, ALTURA), (0, 0, 0, 0))
glow_b_draw = ImageDraw.Draw(glow_bottom)
for i in range(30, 0, -1):
    alpha = int(255 * 0.12 * (1 - i / 30))
    radius = max(10, 500 - i * 15)
    cx = LARGURA // 2
    cy = ALTURA - 400
    glow_b_draw.ellipse(
        [cx - radius, cy - radius, cx + radius, cy + radius],
        fill=(99, 102, 241, alpha)
    )
img = Image.alpha_composite(img, glow_bottom)
draw = ImageDraw.Draw(img)

# Barras de accent
draw.rectangle([0, 0, LARGURA, 6], fill=COR_ACCENT_DARK)
draw.rectangle([0, ALTURA - 4, LARGURA, ALTURA], fill=COR_ACCENT_DARK)
draw.rectangle([0, 6, 3, ALTURA - 4], fill=COR_ACCENT_DARK)

# Fontes
FONT_DIR = "C:/Windows/Fonts"

def _carregar(nome, tamanho):
    caminho = os.path.join(FONT_DIR, nome)
    if os.path.exists(caminho):
        return ImageFont.truetype(caminho, tamanho)
    return ImageFont.load_default()

font_title = _carregar("arialbd.ttf", 80)
font_subtitle = _carregar("arial.ttf", 32)
font_badge = _carregar("arialbd.ttf", 28)
font_author = _carregar("arialbd.ttf", 40)
font_author_role = _carregar("arial.ttf", 20)
font_category = _carregar("arialbd.ttf", 18)
font_stats_num = _carregar("arialbd.ttf", 36)
font_stats_label = _carregar("arial.ttf", 14)
font_logo = _carregar("Consolas.ttf", 32)
font_small = _carregar("arial.ttf", 14)

MARGEM_LEFT = 100
MARGEM_RIGHT = 100
MARGEM_TOP = 60
MARGEM_BOTTOM = 60

# --- HEADER ---
header_y = MARGEM_TOP
draw.rectangle(
    [MARGEM_LEFT, header_y, MARGEM_LEFT + 68, header_y + 68],
    outline=(168, 85, 247, int(255 * 0.6)), width=2,
    fill=(168, 85, 247, int(255 * 0.08))
)
draw.text((MARGEM_LEFT + 20, header_y + 12), ">_", fill=COR_ACCENT_DARK, font=font_logo)

editora_x = MARGEM_LEFT + 90
draw.text((editora_x, header_y + 8), "EDITORA AGÊNTICA", fill=(201, 209, 217, 255), font=font_category)
draw.text((editora_x, header_y + 30), "// publishing.ai_driven", fill=(168, 85, 247, int(255 * 0.7)), font=font_small)

edition_tag = "v1.0 · 2026"
bbox = draw.textbbox((0, 0), edition_tag, font=font_small)
edition_w = bbox[2] - bbox[0]
edition_x = LARGURA - MARGEM_RIGHT - edition_w - 20
draw.rectangle(
    [edition_x - 14, header_y + 8, edition_x + edition_w + 14, header_y + 36],
    outline=(168, 85, 247, int(255 * 0.25)),
    fill=(168, 85, 247, int(255 * 0.05))
)
draw.text((edition_x, header_y + 12), edition_tag, fill=(168, 85, 247, int(255 * 0.6)), font=font_small)

draw.line(
    [(MARGEM_LEFT, header_y + 74), (LARGURA - MARGEM_RIGHT, header_y + 74)],
    fill=(168, 85, 247, int(255 * 0.18)), width=1
)

# --- CORPO CENTRAL ---
body_top = header_y + 90
body_bottom = ALTURA - MARGEM_BOTTOM - 120

# Categoria
cat_x = MARGEM_LEFT
cat_y = body_top + 20
draw.text((cat_x, cat_y), "ANÁLISE DE SISTEMAS", fill=COR_ACCENT_DARK, font=font_category)
draw.line([(cat_x, cat_y + 32), (cat_x + 28, cat_y + 32)], fill=COR_ACCENT_DARK, width=2)

# Título
draw.text((cat_x, cat_y + 50), "Análise da", fill=COR_TEXTO_BRANCO, font=font_title)
draw.text((cat_x, cat_y + 140), "Fábrica Agêntica", fill=COR_ACCENT_DARK, font=font_title)

# Subtítulo
subtitle_y = cat_y + 230
draw.text(
    (cat_x, subtitle_y),
    "Arquitetura Limpa | Código Limpo | Segurança | UI/UX",
    fill=COR_TEXTO_GRAY, font=font_subtitle
)

# Badges
badge_y = subtitle_y + 60
draw.rounded_rectangle(
    [cat_x, badge_y, cat_x + 280, badge_y + 50], radius=8,
    fill=(124, 58, 237, 255)
)
draw.text((cat_x + 20, badge_y + 10), "◆  NÍVEL TÉCNICO", fill=(255, 255, 255, 255), font=font_badge)

badge2_x = cat_x + 300
draw.rounded_rectangle(
    [badge2_x, badge_y, badge2_x + 200, badge_y + 50], radius=8,
    outline=(168, 85, 247, int(255 * 0.4)),
    fill=(168, 85, 247, int(255 * 0.06))
)
draw.text((badge2_x + 12, badge_y + 12), "20 capítulos", fill=COR_ACCENT_DARK, font=font_small)

badge3_x = badge2_x + 220
draw.rounded_rectangle(
    [badge3_x, badge_y, badge3_x + 180, badge_y + 50], radius=8,
    outline=(168, 85, 247, int(255 * 0.4)),
    fill=(168, 85, 247, int(255 * 0.06))
)
draw.text((badge3_x + 12, badge_y + 12), "projetos práticos", fill=COR_ACCENT_DARK, font=font_small)

# Divisor
div_y = badge_y + 70
draw.line([(cat_x, div_y), (cat_x + 500, div_y)], fill=(168, 85, 247, int(255 * 0.1)), width=1)
for i, dot_x in enumerate([cat_x + 520, cat_x + 535, cat_x + 550]):
    alpha = int(255 * (0.8 - i * 0.3))
    draw.ellipse([dot_x, div_y - 3, dot_x + 6, div_y + 3], fill=(55, 195, 214, alpha))

# --- RODAPÉ ---
footer_top = ALTURA - MARGEM_BOTTOM - 120
footer_y = footer_top + 30
draw.line(
    [(MARGEM_LEFT, footer_top), (LARGURA - MARGEM_RIGHT, footer_top)],
    fill=(168, 85, 247, int(255 * 0.15)), width=1
)

draw.text((cat_x, footer_y), "AUTOR", fill=(168, 85, 247, int(255 * 0.6)), font=font_category)
draw.text((cat_x, footer_y + 20), "Heverton Eduardo Peres", fill=(230, 237, 243, 255), font=font_author)
draw.text((cat_x, footer_y + 65), "Especialista em Marketing e", fill=(110, 118, 129, 255), font=font_author_role)
draw.text((cat_x, footer_y + 85), "Desenvolvimento de Soluções", fill=(110, 118, 129, 255), font=font_author_role)

# Stats laterais
stats_x = LARGURA - MARGEM_RIGHT - 250
draw.text((stats_x, footer_y), "20", fill=COR_ACCENT_DARK, font=font_stats_num)
draw.text((stats_x, footer_y + 40), "CAPÍTULOS", fill=(72, 79, 88, 255), font=font_stats_label)

stats_x2 = stats_x + 100
draw.text((stats_x2, footer_y), "70+", fill=COR_ACCENT_DARK, font=font_stats_num)
draw.text((stats_x2, footer_y + 40), "PÁGINAS", fill=(72, 79, 88, 255), font=font_stats_label)

stats_x3 = stats_x2 + 100
draw.text((stats_x3, footer_y), "∞", fill=COR_ACCENT_DARK, font=font_stats_num)
draw.text((stats_x3, footer_y + 40), "PROJETOS", fill=(72, 79, 88, 255), font=font_stats_label)

# Salvar
caminho_saida = f"{DIR_RELATORIOS}/imagens/capa-livro-analise-agentica.png"
img.save(caminho_saida, 'PNG', optimize=True)
print(f"[OK] Capa gerada: {caminho_saida}")
print(f"  Dimensões: {LARGURA}x{ALTURA} px")

img_check = Image.open(caminho_saida)
print(f"  Verificado: {img_check.size[0]}x{img_check.size[1]} px ({img_check.size[0] / img_check.size[1]:.2f})")
