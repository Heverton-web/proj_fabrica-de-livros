"""Testes da rota /api/checkout da Máquina de Vendas (template + gerador).

A rota vive em `templates/maquina/frontend/app/api/checkout/route.ts` e é
copiada pelo `criar-maquina-vendas.py` para toda máquina nova (requisito R11
da SPEC_MAQUINA_VENDAS.md). Estes testes validam o CONTRATO da rota:

1. A rota existe no template E na máquina gerada;
2. A validação zod está presente (nome >= 2, e-mail válido, produto default);
3. O registro no backend existe (POST /api/leads/ + BACKEND_URL com fallback);
4. A resposta tem redirect_url /obrigado e valor com placeholder {{PRECO_CORE}};
5. O checkout page envia JSON via fetch (não form urlencoded) com nome/e-mail;
6. O .env.example expõe BACKEND_URL / NEXT_PUBLIC_BACKEND_URL;
7. O gerador substitui os placeholders (sem resíduos "{{").
"""

import re
from pathlib import Path

import pytest

from conftest import carregar_script

DIR_PROJETO = Path(__file__).resolve().parent.parent
DIR_TEMPLATE = DIR_PROJETO / "templates" / "maquina"
ROTA_CHECKOUT = DIR_TEMPLATE / "frontend" / "app" / "api" / "checkout" / "route.ts"
PAGINA_CHECKOUT = DIR_TEMPLATE / "frontend" / "app" / "checkout" / "page.tsx"
ENV_EXEMPLO = DIR_TEMPLATE / ".env.example"


# ── 1. Existência ────────────────────────────────────────────────────────────

def test_rota_checkout_existe_no_template():
    assert ROTA_CHECKOUT.is_file(), (
        "Rota /api/checkout ausente no template — o checkout/page.tsx posta nela "
        "e toda máquina nova nasceria com 404 (SPEC_MAQUINA_VENDAS R11)"
    )


def test_pagina_checkout_existe_no_template():
    assert PAGINA_CHECKOUT.is_file()


# ── 2. Validação zod ─────────────────────────────────────────────────────────

@pytest.fixture(scope="module")
def rota_texto():
    return ROTA_CHECKOUT.read_text(encoding="utf-8")


def test_zod_valida_nome_minimo(rota_texto):
    assert re.search(r'z\.\s*string\s*\(\)\s*\.min\s*\(2', rota_texto), (
        "zod deve exigir nome com mínimo de 2 caracteres")


def test_zod_valida_email(rota_texto):
    assert re.search(r'z\.\s*string\s*\(\)\s*\.email\s*\(', rota_texto), (
        "zod deve validar o formato do e-mail")


def test_zod_produto_default_placeholder(rota_texto):
    assert re.search(r'\.default\s*\("{{SLUG}}"\)', rota_texto), (
        "produto deve ter default {{SLUG}} substituído pelo gerador")


def test_zod_nome_e_email_obrigatorios(rota_texto):
    assert re.search(r'nome:\s*z\.\s*string\s*\(\)\s*\.min\s*\(2', rota_texto)
    assert re.search(r'email:\s*z\.\s*string\s*\(\)\s*\.email\s*\(', rota_texto)


# ── 3. Registro no backend ───────────────────────────────────────────────────

def test_rota_registra_lead_no_backend(rota_texto):
    assert "/api/leads/" in rota_texto, (
        "a rota de checkout deve registrar o lead no backend FastAPI")


def test_rota_usa_backend_url_com_fallback(rota_texto):
    assert "BACKEND_URL" in rota_texto
    assert "NEXT_PUBLIC_BACKEND_URL" in rota_texto
    assert "http://127.0.0.1:8000" in rota_texto


def test_rota_diferencia_json_invalido_de_erro_interno(rota_texto):
    """A rota deve responder 400 para JSON malformado e 500 para erro interno."""
    assert "instanceof SyntaxError" in rota_texto
    assert "status: isJsonParse ? 400 : 500" in rota_texto
    assert "Payload inválido" in rota_texto


def test_rota_devolve_redirect_obrigado(rota_texto):
    assert 'redirect_url: "/obrigado"' in rota_texto


def test_rota_devolve_valor_placeholder(rota_texto):
    assert "valor: {{PRECO_CORE}}" in rota_texto, (
        "o valor deve usar {{PRECO_CORE}} substituído pelo gerador")


def test_rota_payment_link_webhook(rota_texto):
    assert "payment_link" in rota_texto
    assert "/api/webhooks/lead" in rota_texto


# ── 4. Página de checkout envia JSON via fetch ───────────────────────────────

@pytest.fixture(scope="module")
def pagina_texto():
    return PAGINA_CHECKOUT.read_text(encoding="utf-8")


def test_checkout_page_usa_fetch_json(pagina_texto):
    assert '"use client"' in pagina_texto, (
        "checkout page precisa ser client component para usar fetch")
    assert 'fetch("/api/checkout"' in pagina_texto, (
        "checkout page deve enviar via fetch, não form urlencoded — form HTML "
        "puro quebraria no request.json da rota")
    assert '"Content-Type": "application/json"' in pagina_texto


def test_checkout_page_tem_campos_nome_email(pagina_texto):
    assert 'name="nome"' in pagina_texto
    assert 'name="email"' in pagina_texto
    assert 'type="email"' in pagina_texto
    assert "required" in pagina_texto


def test_checkout_page_redireciona_obrigado(pagina_texto):
    assert 'window.location.href = "/obrigado"' in pagina_texto


# ── 5. .env.example ──────────────────────────────────────────────────────────

def test_env_exemplo_tem_backend_url():
    env = ENV_EXEMPLO.read_text(encoding="utf-8")
    assert "BACKEND_URL=" in env
    assert "NEXT_PUBLIC_BACKEND_URL=" in env


# ── 6. Gerador produz máquina com a rota e placeholders resolvidos ───────────

def test_gerador_tem_reconfigure_utf8():
    """Regra 11 do AGENTS.md: scripts com emojis precisam de UTF-8 no Windows."""
    gerador = carregar_script("criar-maquina-vendas.py")
    fonte = Path(gerador.__file__).read_text(encoding="utf-8")
    assert "reconfigure(encoding=\"utf-8\")" in fonte


def test_gerador_cria_rota_com_placeholders_resolvidos(tmp_path, monkeypatch):
    """Gera uma máquina real em diretório temporário e valida a rota final."""
    gerador = carregar_script("criar-maquina-vendas.py")

    # Redirecionar a saída para tmp_path (não tocar marketing/maquinas real)
    monkeypatch.setattr(gerador, "OUTPUT_BASE", tmp_path)
    monkeypatch.setattr(gerador, "OBRA_BASE", tmp_path / "obras")

    slug = "obra-checkout-teste"
    destino = tmp_path / slug
    gerador.criar_maquina(slug, tipo="completo")

    rota_gerada = destino / "frontend" / "app" / "api" / "checkout" / "route.ts"
    assert rota_gerada.is_file(), "a rota /api/checkout deve ser copiada para a máquina"

    texto = rota_gerada.read_text(encoding="utf-8")
    assert "{{" not in texto, f"placeholders não resolvidos na rota gerada:\n{texto}"
    assert slug in texto, "produto default deve conter o slug da máquina"
    assert "97" in texto, "{{PRECO_CORE}} deve virar 97"
    assert "http://127.0.0.1:8000" in texto

    # .env.example copiado e com BACKEND_URL
    env_gerado = destino / ".env.example"
    assert env_gerado.is_file()
    assert "BACKEND_URL=" in env_gerado.read_text(encoding="utf-8")

    # Manifesto gerado (contrato mínimo de saída)
    assert (destino / "manifesto.json").is_file()

    # Página de checkout copiada com fetch
    pagina_gerada = destino / "frontend" / "app" / "checkout" / "page.tsx"
    assert pagina_gerada.is_file()
    assert 'fetch("/api/checkout"' in pagina_gerada.read_text(encoding="utf-8")
