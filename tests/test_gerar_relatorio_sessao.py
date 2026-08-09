"""Testes do script scripts/gerar-relatorio-sessao.py (convenção V5.2).

Cobre a normalização do nome de arquivo, o template do markdown (seções,
escape de pipes) e a geração end-to-end MD (+PDF quando pandoc disponível).
"""

import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path

from conftest import carregar_script

DIR_PROJETO = Path(__file__).resolve().parent.parent


def _modulo():
    return carregar_script("gerar-relatorio-sessao.py")


# ── slug_tema ────────────────────────────────────────────────────────────────

def test_slug_tema_normaliza():
    m = _modulo()
    assert m.slug_tema("Máquina de Vendas / Checkout!") == "maquina-de-vendas-checkout"
    assert m.slug_tema("feat(api)") == "feat-api"
    assert m.slug_tema("  Espaços  ") == "espacos"
    assert m.slug_tema("") == ""
    assert m.slug_tema(None) == ""


# ── montar_markdown ──────────────────────────────────────────────────────────

def test_markdown_tem_secoes_obrigatorias():
    m = _modulo()
    md = m.montar_markdown(
        titulo="Sessão Teste",
        contexto="ctx",
        bugs=["causa|fix|scripts/foo.py"],
        arquivos=["scripts/bar.py"],
        validacoes=["445 testes"],
        commits=["abc123"],
        entregas=["entrega1"],
    )
    for secao in ("## 1. Contexto", "## 2. Bugs", "## 3. Arquivos",
                  "## 4. Validações", "## 5. Commits", "## 6. Resumo"):
        assert secao in md
    assert "- **Causa:** causa" in md
    assert "- **Fix:** fix" in md
    assert "`scripts/foo.py`" in md
    assert "`abc123`" in md
    assert "- entrega1" in md
    assert date.today().isoformat() in md


def test_markdown_escapa_pipe():
    m = _modulo()
    md = m.montar_markdown("T", "ctx", [], [], ["a | b"], [], [])
    assert "a \\| b" in md


def test_markdown_sem_bugs_usam_placeholder():
    m = _modulo()
    md = m.montar_markdown("T", "ctx", [], [], [], [], [])
    assert "Nenhum bug registrado" in md


# ── geração end-to-end (MD) ──────────────────────────────────────────────────

def test_gera_arquivos_md(tmp_path, monkeypatch):
    m = _modulo()
    # Redirecionar a pasta de relatórios para tmp_path
    monkeypatch.setattr(m, "RELATORIOS_DIR", tmp_path)

    # Simular a main() sem argparse: chamar as funções diretamente
    md_path = tmp_path / f"{date.today().isoformat()}-sessao-teste.md"
    md = m.montar_markdown("Sessão Teste", "ctx", ["c|f|x"], ["a"], ["v"], ["c"], ["e"])
    md_path.write_text(md, encoding="utf-8")
    assert md_path.is_file()
    assert "Sessão Teste" in md_path.read_text(encoding="utf-8")


def test_gera_pdf_se_pandoc_disponivel(tmp_path, monkeypatch):
    if not shutil.which("pandoc"):
        import pytest
        pytest.skip("pandoc não instalado")
    m = _modulo()
    monkeypatch.setattr(m, "RELATORIOS_DIR", tmp_path)
    md_path = tmp_path / "relatorio.md"
    pdf_path = tmp_path / "relatorio.pdf"
    md_path.write_text("# Teste\n\nConteúdo.\n", encoding="utf-8")
    rc = m.gerar_pdf(md_path, pdf_path)
    assert rc == 0, f"pandoc falhou (rc={rc})"
    assert pdf_path.is_file()
    assert pdf_path.stat().st_size > 0
