#!/usr/bin/env python3
"""
Gera capa de análise com identidade visual única.
Cor predominante: #1e3a5c (navy analítico) com destaque em #f0b429 (âmbar surpresa).
NADA de texto cortado. Legibilidade sine qua non.
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
import os, math

# ═══════════════════════════════════════════════════════════════════════════
# CONFIGURAÇÃO DA IDENTIDADE VISUAL
# ═══════════════════════════════════════════════════════════════════════════

LARGURA = 1600
ALTURA = 2263

# Cor predominante (evidente em todas as faixas, gradientes, destaques)
COR_PREDOMINANTE = (30, 58, 92, 255)      # #1e3a5c — navy analítico
COR_PREDOMINANTE_ESCURO = (18, 38, 68, 255)   # #122644 — variante mais escura
COR_PREDOMINANTE_CLARO = (48, 88, 132, 255)  # #305884 — variante mais clara

# Cor de destaque para a 1 palavra do título (SURPRESA: âmbar, não o habitual ciano)
COR_DESTAQUE = (240, 180, 43, 255)        # #f0b429 — âmbar/aquão

# Fundo
COR_FUNDO = (10, 14, 26, 255)              # #0a0e1a — quase preto, frio

# Textos
COR_BRANCO = (240, 246, 252, 255)          # #f0f6fc
COR_CIAN = (55, 195, 214, 255)             # #37c3d6 — mantido como secundário
COR_GRAY = (139, 148, 158, 255)            # #8b949e
COR_GRAY_CLARO = (175, 185, 195, 255)      # #afb9c3

# Badges
COR_BADGE_ROXO = (124, 58, 237, 255)      # #7c3aed
COR_BADGE_OUTLINE = (30, 58, 92, 255)     # borda dos badges secundários

# ═══════════════════════════════════════════════════════════════════════════
# CRIAÇÃO DA IMAGEM
# ═══════════════════════════════════════════════════════════════════════════

img = Image.new('RGBA', (LARGURA, ALTURA), COR_FUNDO)
draw = ImageDraw.Draw(img)

# ─── 1. FUNDO COM PADRÃO ANALÍTICO (nada de grid genérico) ─────────────
# Padrão: linhas de "dado" entrelaçadas — sugere análise, conectividade

# Grid fino de fundo
grid_color = (30, 58, 92, 15)  # muito sutil
for x in range(0, LARGURA, 40):
    draw.line([(x, 0), (x, ALTURA)], fill=grid_color, width=1)
for y in range(0, ALTURA, 40):
    draw.line([(0, y), (LARGURA, y)], fill=grid_color, width=1)

# Padrão analítico: cruzes de "dado" sutil no fundo
cruz_color = (30, 58, 92, 8)
for cx in range(200, LARGURA - 200, 180):
    for cy in range(200, ALTURA - 200, 180):
        cross_size = 30
        draw.line([(cx - cross_size, cy), (cx + cross_size, cy)], fill=cruz_color, width=1)
        draw.line([(cx, cy - cross_size), (cx, cy + cross_size)], fill=cruz_color, width=1)
        # pequeno círculo no centro
        draw.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=cruz_color)

# Glow analítico no centro (como um "spotlight de dados")
glow = Image.new('RGBA', (LARGURA, ALTURA), (0, 0, 0, 0))
glow_draw = ImageDraw.Draw(glow)
for i in range(80, 0, -1):
    alpha = int(255 * 0.06 * (1 - i / 80))
    radius = max(20, 500 - i * 4)
    cx, cy = LARGURA // 2, ALTURA // 2 - 100
    glow_draw.ellipse([cx - radius, cy - radius, cx + radius, cy + radius],
                      fill=(30, 58, 92, alpha))
img = Image.alpha_composite(img, glow)
draw = ImageDraw.Draw(img)

# ─── 2. FAIXAS DE COR PREDOMINANTE ─────────────────────────────────────
# Superior
draw.rectangle([0, 0, LARGURA, 8], fill=COR_PREDOMINANTE)
# Inferior  
draw.rectangle([0, ALTURA - 8, LARGURA, ALTURA], fill=COR_PREDOMINANTE)
# Lateral esquerda
draw.rectangle([0, 8, 4, ALTURA - 8], fill=COR_PREDOMINANTE)
# Lateral direita
draw.rectangle([LARGURA - 4, 8, LARGURA, ALTURA - 8], fill=COR_PREDOMINANTE)

# Gradiente sutil na faixa superior (de escuro para predominante)
for i in range(8):
    t = i / 8
    r = int(COR_PREDOMINANTE_ESCURO[0] + (COR_PREDOMINANTE[0] - COR_PREDOMINANTE_ESCURO[0]) * t)
    g = int(COR_PREDOMINANTE_ESCURO[1] + (COR_PREDOMINANTE[1] - COR_PREDOMINANTE_ESCURO[1]) * t)
    b = int(COR_PREDOMINANTE_ESCURO[2] + (COR_PREDOMINANTE[2] - COR_PREDOMINANTE_ESCURO[2]) * t)
    draw.line([(0, i), (LARGURA, i)], fill=(r, g, b, 255), width=1)

# Gradiente sutil na faixa inferior
for i in range(8):
    t = i / 8
    r = int(COR_PREDOMINANTE[0] + (COR_PREDOMINANTE_ESCURO[0] - COR_PREDOMINANTE[0]) * t)
    g = int(COR_PREDOMINANTE[1] + (COR_PREDOMINANTE_ESCURO[1] - COR_PREDOMINANTE[1]) * t)
    b = int(COR_PREDOMINANTE[2] + (COR_PREDOMINANTE_ESCURO[2] - COR_PREDOMINANTE[2]) * t)
    draw.line([(0, ALTURA - 8 + i), (LARGURA, ALTURA - 8 + i)], fill=(r, g, b, 255), width=1)

# ─── 3. CODE DECORATIVO DE FUNDO ────────────────────────────────────────
code_text = """import analise
from fabrica import *

class Auditor:
    def __init__(self, obra):
        self.obra = obra
        self.dim = 4  # arquitetura, codigo, seguranca, uix
    
    def executar(self):
        resultados = []
        for dim in self.dimensions:
            r = self.analisar(dim)
            resultados.append(r)
        return self.sintetizar(resultados)

auditor = Auditor(fabrica_agentica)
print(auditor.executar())"""

# Fundo do código
code_layer = Image.new('RGBA', (LARGURA, ALTURA), (0, 0, 0, 0))
code_draw = ImageDraw.Draw(code_layer)
code_draw.text((60, 50), code_text, fill=(30, 58, 92, 20), font=ImageFont.truetype(
    "C:/Windows/Fonts/Consolas.ttf", 16))
# Área do código com blur
code_layer = code_layer.filter(ImageFilter.GaussianBlur(2))
img = Image.alpha_composite(img, code_layer)
draw = ImageDraw.Draw(img)

# ─── 4. TIPOGRAFIA ──────────────────────────────────────────────────────
FONT_DIR = "C:/Windows/Fonts"

def get_font(nome, tamanho):
    caminho = os.path.join(FONT_DIR, nome)
    if os.path.exists(caminho):
        return ImageFont.truetype(caminho, tamanho)
    raise FileNotFoundError(f"Fonte não encontrada: {caminho}")

try:
    font_logo = get_font("Consolas.ttf", 28)
    font_editora_name = get_font("arialbd.ttf", 16)
    font_editora_tag = get_font("arial.ttf", 12)
    font_version = get_font("arial.ttf", 13)
    font_category = get_font("arialbd.ttf", 14)
    font_title_main = get_font("arialbd.ttf", 82)   # palavra em destaque
    font_title_neutral = get_font("arial.ttf", 72)   # palavras neutras
    font_subtitle = get_font("arial.ttf", 30)
    font_badge_main = get_font("arialbd.ttf", 22)
    font_badge_secondary = get_font("arial.ttf", 18)
    font_author_label = get_font("arialbd.ttf", 12)
    font_author_name = get_font("arialbd.ttf", 38)
    font_author_role = get_font("arial.ttf", 18)
    font_stat_number = get_font("arialbd.ttf", 34)
    font_stat_label = get_font("arial.ttf", 14)
    font_section_title = get_font("arialbd.ttf", 48)
except Exception as e:
    print(f"Erro ao carregar fontes: {e}")
    raise

# Função para medir texto
def text_size(texto, fonte):
    bbox = draw.textbbox((0, 0), texto, font=fonte)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]

def draw_text_center(draw, texto, fonte, x, y, fill, shadow=True):
    """Desenha texto centralizado horizontalmente com opção de sombra."""
    tw, th = text_size(texto, fonte)
    cx = x - tw // 2
    cy = y - th // 2
    
    if shadow:
        draw.text((cx + 2, cy + 2), texto, fill=(0, 0, 0, 100), font=fonte)
    draw.text((cx, cy), texto, fill=fill, font=fonte)
    return tw, th

# ─── 5. HEADER: LOGO + EDITORA + VERSAO ────────────────────────────────
MARGEM_LEFT = 80
MARGEM_RIGHT = 80

# Logo da editora — quadrado com borda na cor predominante
logo_x = MARGEM_LEFT
logo_y = 40
logo_size = 64
draw.rounded_rectangle(
    [logo_x, logo_y, logo_x + logo_size, logo_y + logo_size],
    radius=12,
    outline=COR_PREDOMINANTE + (180,),  # borda semi-transparente
    width=2,
    fill=COR_PREDOMINANTE + (20,)       # fundo muito sutil
)
# Símbolo ">_" em Console/Mono
draw.text((logo_x + 16, logo_y + 12), ">_", fill=COR_DESTAQUE, font=font_logo)

# Nome da editora
editora_x = logo_x + logo_size + 20
editora_nome_y = logo_y + 10
draw.text((editora_x, editora_nome_y), "EDITORA AGÊNTICA", fill=COR_BRANCO, font=font_editora_name)
draw.text((editora_x, editora_nome_y + 22), "// publicando.saber", fill=COR_CIAN, font=font_editora_tag)

# Badge versão/ano — canto superior direito
version_text = "v1.0 · 2026"
vw, vh = text_size(version_text, font_version)
version_x = LARGURA - MARGEM_RIGHT - vw - 14
version_y = 42
# Caixa com borda na cor predominante
draw.rounded_rectangle(
    [version_x - 10, version_y - 4, version_x + vw + 10, version_y + vh + 4],
    radius=6,
    outline=COR_PREDOMINANTE + (120,),
    width=1,
    fill=COR_PREDOMINANTE + (15,)
)
draw.text((version_x, version_y), version_text, fill=COR_GRAY_CLARO, font=font_version)

# Linha separadora do header
header_bottom = logo_y + logo_size + 16
draw.line(
    [(MARGEM_LEFT, header_bottom), (LARGURA - MARGEM_RIGHT, header_bottom)],
    fill=COR_PREDOMINANTE + (60,),
    width=1
)

# ─── 6. CATEGORIA ────────────────────────────────────────────────────────
body_top = header_bottom + 30
cat_x = MARGEM_LEFT
cat_y = body_top
draw.text((cat_x, cat_y), "ANÁLISE DE SISTEMAS", fill=COR_DESTAQUE, font=font_category)
# Linha decorativa sob a categoria
draw.line([(cat_x, cat_y + 24), (cat_x + 30, cat_y + 24)], fill=COR_DESTAQUE, width=2)

# ─── 7. TÍTULO COM APENAS 1 PALAVRA NA COR PRINCIPAL ────────────────────
# "Análise da" (neutro) + "FÁBRICA" (cor predominante/destaque) + "Agêntica" (neutro)
# Para surpreender: "FÁBRICA" em âmbar (#f0b429)

titulo_y = cat_y + 40

# Medir cada parte para posicionamento preciso
neutral_part1 = "Análise da"
highlight_word = "FÁBRICA"
neutral_part2 = "Agêntica"

tw1, th1 = text_size(neutral_part1, font_title_neutral)
tw2, th2 = text_size(highlight_word, font_title_main)
tw3, th3 = text_size(neutral_part2, font_title_neutral)

# Verificar se há risco de corte — se o título não cabe, reduzir tamanho
while tw1 + tw2 + tw3 > LARGURA - 2 * MARGEM_LEFT:
    font_title_neutral = get_font("arial.ttf", font_title_neutral.size - 4)
    font_title_main = get_font("arialbd.ttf", font_title_main.size - 4)
    tw1, th1 = text_size(neutral_part1, font_title_neutral)
    tw2, th2 = text_size(highlight_word, font_title_main)
    tw3, th3 = text_size(neutral_part2, font_title_neutral)

# Verificar altura total
total_title_h = max(th1, th2, th3)
if total_title_h > 120:
    # Reduzir tudo proporcionalmente
    factor = 120 / total_title_h
    font_title_neutral = get_font("arial.ttf", int(font_title_neutral.size * factor))
    font_title_main = get_font("arialbd.ttf", int(font_title_main.size * factor))
    tw1, th1 = text_size(neutral_part1, font_title_neutral)
    tw2, th2 = text_size(highlight_word, font_title_main)
    tw3, th3 = text_size(neutral_part2, font_title_neutral)

# Posicionar cada parte
total_width = tw1 + tw2 + tw3
start_x = MARGEM_LEFT
ty = titulo_y + (max(th1, th2, th3) - th1) // 2  # centralizar verticalmente

# Parte 1: "Análise da" — branco
draw.text((start_x, titulo_y), neutral_part1, fill=COR_BRANCO, font=font_title_neutral)
start_x += tw1

# Parte 2: "FÁBRICA" — COR DESTAQUE (âmbar) — o destaque visual
# Adicionar glow sutil ao redor desta palavra
draw.text((start_x + 3, titulo_y + 3), highlight_word, fill=(0, 0, 0, 80), font=font_title_main)
draw.text((start_x, titulo_y), highlight_word, fill=COR_DESTAQUE, font=font_title_main)
start_x += tw2

# Parte 3: "Agêntica" — branco
ty2 = titulo_y + (max(th1, th2, th3) - th3) // 2
draw.text((start_x, ty2), neutral_part2, fill=COR_BRANCO, font=font_title_neutral)

# Linha decorativa sob o título
line_y = titulo_y + total_title_h + 12
draw.line(
    [(MARGEM_LEFT, line_y), (start_x + tw3, line_y)],
    fill=COR_PREDOMINANTE + (100,),
    width=1
)

# ─── 8. SUBTITULO ────────────────────────────────────────────────────────
subtitle_y = line_y + 18
draw.text(
    (MARGEM_LEFT, subtitle_y),
    "Arquitetura Limpa | Código Limpo | Segurança | UI/UX",
    fill=COR_GRAY,
    font=font_subtitle
)

# ─── 9. BADGES (3: senioridade, capítulos reais, foco) ──────────────────
badge_y = subtitle_y + 50

# Badges layout
badge_gap = 16
all_badges_width = 0
badge_data = [
    ("NÍVEL TÉCNICO", "badge_main", COR_BADGE_ROXO, COR_BRANCO),
    ("6 SEÇÕES", "badge_secondary", None, COR_CIAN),
    ("ANÁLISE INTEGRAL", "badge_secondary", None, COR_CIAN),
]

# Primeiro pass: medir todos para layout
badge_widths = []
for texto, _, _, _ in badge_data:
    w, h = text_size(texto, font_badge_secondary if "secondary" in _ else font_badge_main)
    # Adicionar padding
    padding = 20 if "main" in _ else 16
    badge_widths.append((w + 2 * padding, h + 2 * padding, texto, _))

total_badges_w = sum(b[0] for b in badge_widths) + badge_gap * (len(badge_widths) - 1)
start_badge_x = MARGEM_LEFT

# Desenhar badges
for i, (bw, bh, texto, tipo) in enumerate(badge_widths):
    bx = start_badge_x + sum(bw_b for bw_b, _, _, _ in badge_widths[:i]) + badge_gap * i
    
    if tipo == "badge_main":
        # Badge principal: gradiente roxo→cian com ◆
        badge_img = Image.new('RGBA', (bw, bh), (0, 0, 0, 0))
        badge_draw = ImageDraw.Draw(badge_img)
        
        # Gradiente 135° roxo → cian
        for px in range(bw):
            for py in range(bh):
                t = (px / bw + py / bh) / 2  # diagonal 135°
                t = max(0, min(1, t))
                r = int(COR_BADGE_ROXO[0] + (COR_CIAN[0] - COR_BADGE_ROXO[0]) * t)
                g = int(COR_BADGE_ROXO[1] + (COR_CIAN[1] - COR_BADGE_ROXO[1]) * t)
                b = int(COR_BADGE_ROXO[2] + (COR_CIAN[2] - COR_BADGE_ROXO[2]) * t)
                badge_draw.point((px, py), fill=(r, g, b, 255))
        
        # Borda arredondada
        badge_draw.rounded_rectangle([0, 0, bw, bh], radius=8, outline=None, fill=None)
        
        # Texto "◆  NÍVEL TÉCNICO"
        badge_draw.text((12, bh // 2 - 11), "◆  " + texto, fill=COR_BRANCO, font=font_badge_main)
        
        # Drop shadow (borda externa escura)
        shadow = Image.new('RGBA', (bw + 8, bh + 8), (0, 0, 0, 0))
        shadow_draw = ImageDraw.Draw(shadow)
        shadow_draw.rounded_rectangle([4, 4, bw + 4, bh + 4], radius=8, fill=(0, 0, 0, 40))
        shadow = shadow.filter(ImageFilter.GaussianBlur(3))
        
        # Composição final
        badge_final = Image.new('RGBA', (bw + 8, bh + 8), (0, 0, 0, 0))
        badge_final.paste(shadow, (0, 0), shadow)
        badge_final.paste(badge_img, (4, 4), badge_img)
        
        img.paste(badge_final, (bx - 4, badge_y - 4), badge_final)
    else:
        # Badge secundário: outline apenas
        draw.rounded_rectangle(
            [bx, badge_y, bx + bw, badge_y + bh],
            radius=8,
            outline=COR_BADGE_OUTLINE + (150,),
            width=1,
            fill=COR_PREDOMINANTE + (12,)
        )
        draw.text((bx + 10, badge_y + bh // 2 - 9), texto, fill=COR_CIAN, font=font_badge_secondary)

# ─── 10. DIVISOR ─────────────────────────────────────────────────────────
div_y = badge_y + 50 + 12
draw.line([(MARGEM_LEFT, div_y), (MARGEM_LEFT + 400, div_y)], fill=COR_PREDOMINANTE + (60,), width=1)
for i, dot_x in enumerate([MARGEM_LEFT + 410, MARGEM_LEFT + 422, MARGEM_LEFT + 434]):
    alpha = int(150 * (1 - i * 0.25))
    draw.ellipse([dot_x, div_y - 2, dot_x + 4, div_y + 2], fill=(55, 195, 214, alpha))

# ─── 11. RODAPÉ: AUTOR + QUALIFICAÇÃO ────────────────────────────────────
footer_top = ALTURA - 140
footer_y = footer_top

draw.line(
    [(MARGEM_LEFT, footer_top), (LARGURA - MARGEM_RIGHT, footer_top)],
    fill=COR_PREDOMINANTE + (60,),
    width=1
)

# Autor
author_x = MARGEM_LEFT
author_y = footer_y + 16
draw.text((author_x, author_y), "AUTOR", fill=COR_CIAN, font=font_author_label)
draw.text((author_x, author_y + 18), "Heverton Eduardo Peres", fill=COR_BRANCO, font=font_author_name)
draw.text((author_x, author_y + 62), "Especialista em Marketing e Desenvolvimento de Soluções",
          fill=COR_GRAY, font=font_author_role)

# ─── 12. 3 INFOS (capítulos reais, páginas reais, foco) ─────────────────
stats_x = LARGURA - MARGEM_RIGHT - 280
stats_data = [
    ("6", "SEÇÕES"),
    ("17", "PÁGINAS"),
    ("4", "DIMENSÕES"),
]

for i, (numero, label) in enumerate(stats_data):
    sx = stats_x + i * 85
    
    # Número grande
    draw.text((sx, footer_y + 16), numero, fill=COR_DESTAQUE, font=font_stat_number)
    # Label
    draw.text((sx, footer_y + 56), label, fill=COR_GRAY, font=font_stat_label)
    
    # Divisor entre stats (exceto último)
    if i < len(stats_data) - 1:
        div_x = sx + 60
        draw.line([(div_x, footer_y + 16), (div_x, footer_y + 80)], fill=COR_PREDOMINANTE + (40,), width=1)

# ─── 13. VERIFICAÇÃO FINAL: NADA CORTADO ────────────────────────────────
# Validar que nada ultrapassa os limites
def check_bounds(cx, cy, texto, fonte, margin_left=MARGEM_LEFT, margin_right=MARGEM_RIGHT, margin_top=0, margin_bottom=ALTURA):
    tw, th = text_size(texto, fonte)
    if cx + tw > LARGURA - margin_right:
        return False, f"TEXTO CORTADO horizontalmente: {texto[:30]}... em ({cx},{cy}), largura {tw} ultrapassa limite"
    if cy - th < margin_top:
        return False, f"TEXTO CORTADO no topo: {texto[:30]}... em ({cx},{cy}), altura {th} ultrapassa"
    if cy > margin_bottom:
        return False, f"TEXTO CORTADO no fundo: {texto[:30]}... em ({cx},{cy})"
    return True, "OK"

# Verificações
verificacoes = []

# Verificar título
titulo_ok, msg = check_bounds(MARGEM_LEFT, titulo_y, neutral_part1 + highlight_word + neutral_part2, font_title_main)
verificacoes.append(("Título 'Análise da FÁBRICA Agêntica'", titulo_ok, msg))

# Verificar subtitle
sub_ok, msg = check_bounds(MARGEM_LEFT, subtitle_y, "Arquitetura Limpa | Código Limpo | Segurança | UI/UX", font_subtitle)
verificacoes.append(("Subtítulo", sub_ok, msg))

# Verificar badges
for i, (bw, bh, texto, tipo) in enumerate(badge_widths):
    bx = MARGEM_LEFT + sum(bw_b for bw_b, _, _, _ in badge_widths[:i]) + badge_gap * i
    badge_ok, msg = check_bounds(bx, badge_y, texto, font_badge_main if tipo == "badge_main" else font_badge_secondary)
    verificacoes.append((f"Badge {i+1}: {texto}", badge_ok, msg))

# Verificar rodapé
footer_ok, msg = check_bounds(MARGEM_LEFT, author_y + 80, "Especialista em Marketing e Desenvolvimento de Soluções", font_author_role)
verificacoes.append(("Rodapé autor", footer_ok, msg))

# Verificar stats
for numero, label in stats_data:
    sx = LARGURA - MARGEM_RIGHT - 280
    stats_ok, msg = check_bounds(sx, footer_y + 80, label, font_stat_label)
    verificacoes.append((f"Stat: {label}", stats_ok, msg))

print("╔══════════════════════════════════════════════════════════╗")
print("║            VERIFICAÇÃO DE LEGIBILIDADE                  ║")
print("╠══════════════════════════════════════════════════════════╣")
for nome, ok, msg in verificacoes:
    status = "✅ OK" if ok else "❌ CORTADO"
    print(f"║  {nome:<40} {status:<10}║")
    if not ok:
        print(f"║  → {msg:<51}║")
print("╚══════════════════════════════════════════════════════════╝")

# ═══════════════════════════════════════════════════════════════════════════
# SALVAR
# ═══════════════════════════════════════════════════════════════════════════

saida_path = "relatorios/imagens/capa-livro-analise-agentica.png"
os.makedirs(os.path.dirname(saida_path), exist_ok=True)
img.save(saida_path, 'PNG', optimize=True)

print(f"\n[OK] Capa salva: {saida_path}")
print(f"  Dimensões: {img.size[0]}x{img.size[1]} px")
print(f"  Proporção: {img.size[0]/img.size[1]:.2f} (padrão A4 ~0.71)")

# Resumo da identidade visual
print(f"\n╔══════════════════════════════════════════════════════════╗")
print("║         IDENTIDADE VISUAL DA CAPA                       ║")
print("╠══════════════════════════════════════════════════════════╣")
print(f"║  Cor predominante: #1e3a5c (navy analítico)           ║")
print(f"║  Faixas: superior, inferior, laterais esquerda/direita ║")
print(f"║  Gradiente faixas: variante escura → clara            ║")
print(f"║  1 palavra do título: FÁBRICA em #f0b429 (âmbar)      ║")
print(f"║  Badges: NÍVEL TÉCNICO | 6 SEÇÕES | ANÁLISE INTEGRAL   ║")
print(f"║  Stats: 6 SEÇÕES | 17 PÁGINAS | 4 DIMENSÕES           ║")
print(f"║  Surpresa: âmber no lugar de ciano para destaque       ║")
print(f"║  Padrão fundo: cruzes de dado + glow analítico         ║")
print(f"╚══════════════════════════════════════════════════════════╝")
