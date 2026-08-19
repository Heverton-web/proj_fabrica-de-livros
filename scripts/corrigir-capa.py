#!/usr/bin/env python3
"""Correção da capa: adiciona gradiente de texto no título e gradiente no badge.
Correção pontual — não regenera tudo."""

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
import os

# Configuração
IMG_PATH = "relatorios/imagens/capa-livro-analise-agentica.png"
SAIDA_PATH = "relatorios/imagens/capa-livro-analise-agentica.png"

img = Image.open(IMG_PATH).convert("RGBA")
draw = ImageDraw.Draw(img)

# Paleta
COR_ROXO = (124, 58, 237)       # #7c3aed
COR_CIAN = (55, 195, 214)       # #37c3d6
COR_BRANCO = (240, 246, 252)    # #f0f6fc

# ─── 1. CRIAR GRADIENTE PARA O BADGE ────────────────────────────────────

# Criar imagem de gradiente 135° roxo→cian
def criar_gradiente_radial(largura, altura, cor_inicio, cor_fim, angulo=135):
    """Cria gradiente em L corner (roxo) para R corner (cian) com angulo 135°"""
    arr = np.zeros((altura, largura, 4), dtype=np.uint8)
    
    # Calcular direção do gradiente (135° = x positivo, y positivo)
    rad = np.radians(angulo)
    dx = np.cos(rad)
    dy = np.sin(rad)
    
    for y in range(altura):
        for x in range(largura):
            t = (x * dx + y * dy) / (largura * abs(dx) + altura * abs(dy))
            t = max(0, min(1, t))
            
            r = int(cor_inicio[0] + (cor_fim[0] - cor_inicio[0]) * t)
            g = int(cor_inicio[1] + (cor_fim[1] - cor_inicio[1]) * t)
            b = int(cor_inicio[2] + (cor_fim[2] - cor_inicio[2]) * t)
            arr[y, x] = [r, g, b, 255]
    
    return Image.fromarray(arr, 'RGBA')

# Criar gradiente do badge
badge_grad = criar_gradiente_radial(280, 50, COR_ROXO, COR_CIAN, 135)

# Criar badge com texto em cima
badge_img = Image.new('RGBA', (280, 50), (0, 0, 0, 0))
badge_draw = ImageDraw.Draw(badge_img)

# Desenhar gradiente do badge
badge_img.paste(badge_grad, (0, 0), badge_grad)

# Adicionar texto "◆  NÍVEL TÉCNICO"
font_badge = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 22)
badge_text = "◆  NÍVEL TÉCNICO"
badge_bbox = badge_draw.textbbox((0, 0), badge_text, font=font_badge)
badge_w = badge_bbox[2] - badge_bbox[0]
badge_h = badge_bbox[3] - badge_bbox[1]

# Posicionar badge text centralizado
badge_x = (280 - badge_w) // 2
badge_y = (50 - badge_h) // 2

# Desenhar texto em branco
badge_draw.text((badge_x, badge_y), badge_text, fill=COR_BRANCO, font=font_badge)

# Adicionar drop shadow ao badge (simulado com borda externa)
badge_with_shadow = Image.new('RGBA', (300, 70), (0, 0, 0, 0))
badge_with_shadow.paste(badge_img, (10, 10), badge_img)

# Adicionar borda externa escura (simula o shadow)
shadow_draw = ImageDraw.Draw(badge_with_shadow)
shadow_draw.rectangle([0, 0, 300, 70], outline=(0, 0, 0, 50), width=5)

# Colocar badge na imagem principal (posição original do badge)
# O badge original está em (cat_x, badge_y) = (100, ~690)
# Vamos colocar o badge corrigido na mesma posição
origem_x = 100
origem_y = 690

# Remover badge antigo (desenhar sobre ele com preto)
draw.rectangle([origem_x, origem_y, origem_x + 280, origem_y + 50], fill=(7, 9, 15, 255))

# Colocar novo badge com gradiente
img.paste(badge_img, (origem_x, origem_y), badge_img)

print("[OK] Badge com gradiente adicionado")


# ─── 2. CRIAR GRADIENTE DE TEXTO PARA "FÁBRICA AGÊNTICA" ─────────────────

# Criar overlay de gradiente para texto
def criar_gradiente_texto(largura, altura, cor_inicio, cor_fim):
    """Cria gradiente horizontal para texto"""
    arr = np.zeros((altura, largura, 4), dtype=np.uint8)
    for x in range(largura):
        t = x / largura
        r = int(cor_inicio[0] + (cor_fim[0] - cor_inicio[0]) * t)
        g = int(cor_inicio[1] + (cor_fim[1] - cor_inicio[1]) * t)
        b = int(cor_inicio[2] + (cor_fim[2] - cor_inicio[2]) * t)
        for y in range(altura):
            arr[y, x] = [r, g, b, 255]
    return Image.fromarray(arr, 'RGBA')

# Pegar posição "FÁBRICA AGÊNTICA" na imagem
# O texto está em (cat_x, cat_y + 140) = (100, ~780)
# Usaremos essa região
text_x = 100
text_y = 780
text_w = 500  # largura estimada do texto
text_h = 80   # altura estimada

# Criar máscara do texto (vermelho para identificar onde está o texto)
mask = Image.new('L', (text_w, text_h), 0)
mask_draw = ImageDraw.Draw(mask)

# Desenhar texto na máscara (em branco)
font_title = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 80)
texto_titulo = "FÁBRICA AGÊNTICA"
text_bbox = mask_draw.textbbox((0, 0), texto_titulo, font=font_title)
tw = text_bbox[2] - text_bbox[0]
th = text_bbox[3] - text_bbox[1]

# Centralizar texto na máscara
tx = (text_w - tw) // 2
ty = (text_h - th) // 2
mask_draw.text((tx, ty), texto_titulo, fill=255, font=font_title)

# Aplicar blur leve na máscara
mask = mask.filter(ImageFilter.GaussianBlur(1))

# Criar gradiente de texto
texto_grad = criar_gradiente_texto(text_w, text_h, COR_CIAN, (100, 220, 240))

# Aplicar gradiente na imagem usando a máscara
img_np = np.array(img)
mask_np = np.array(mask) / 255.0

# Extrair região da imagem
regiao = img_np[text_y:text_y + text_h, text_x:text_x + text_w]

# Aplicar gradiente com alpha
alpha = mask_np[:, :, np.newaxis]
regiao_cor = np.array(texto_grad) * alpha
regiao_original = regiao * (1 - alpha)

# Combinar
regiao_nova = (regiao_original + regiao_cor).astype(np.uint8)
img_np[text_y:text_y + text_h, text_x:text_x + text_w] = regiao_nova

img = Image.fromarray(img_np, 'RGBA')

print("[OK] Gradiente de texto em 'FÁBRICA AGÊNTICA' adicionado")


# ─── 3. SALVAR ────────────────────────────────────────────────────────────

img.save(SAIDA_PATH, 'PNG', optimize=True)
print(f"[OK] Capa corrigida salva: {SAIDA_PATH}")
print(f"  Dimensões: {img.size[0]}x{img.size[1]} px")
