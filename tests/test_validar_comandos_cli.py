#!/usr/bin/env python3
"""Testes para validar_comandos_cli.py"""

import re
import pytest


# Testes de regex diretamente (sem dependência de import do módulo)

class TestRegexCliCheck:
    """Testa extração de marcações cli-check."""

    def test_regex_extrai_cli_check(self):
        """Regex extrai cli-check corretamente."""
        RE_CLI_CHECK = re.compile(r'<!--\s*cli-check:\s*fonte=([A-C]);\s*confere=(true|false)\s*-->')

        texto = "<!-- cli-check: fonte=B; confere=true -->"
        m = RE_CLI_CHECK.search(texto)
        assert m is not None
        assert m.group(1) == "B"
        assert m.group(2) == "true"

    def test_regex_extrai_false(self):
        """Regex extrai confere=false corretamente."""
        RE_CLI_CHECK = re.compile(r'<!--\s*cli-check:\s*fonte=([A-C]);\s*confere=(true|false)\s*-->')

        texto = "<!-- cli-check: fonte=C; confere=false -->"
        m = RE_CLI_CHECK.search(texto)
        assert m is not None
        assert m.group(1) == "C"
        assert m.group(2) == "false"

    def test_regex_extrai_bloco_codigo(self):
        """Regex extrai blocos de código bash."""
        RE_BLOCO = re.compile(r'```(?:bash|sh|python|js|typescript|powershell)?\s*\n(.*?)\n```', re.DOTALL)

        texto = """```bash
pipx install something
```"""
        m = RE_BLOCO.search(texto)
        assert m is not None
        assert "pipx install" in m.group(1)


class TestValidarCapituloMock:
    """Testa validacao de capitulo com fixtures."""

    def test_capitulo_com_comando_confirmado(self, tmp_path):
        """Capítulo com comando marcado confere=true passa."""
        cap = tmp_path / "cap_1.md"
        cap.write_text("""
## 1. Introducao

Instale a ferramenta:

```bash
pip install asyncio
```
<!-- cli-check: fonte=A; confere=true -->

Pronto!
""", encoding="utf-8")

        cmd_ok, cmd_sem, cmd_fab, erro = VCC.validar_capitulo(cap, 1)
        assert erro is None
        assert len(cmd_ok) == 1
        assert cmd_ok[0]["confere"] is True
        assert len(cmd_fab) == 0

    def test_capitulo_com_comando_fabricado(self, tmp_path):
        """Capítulo com comando marcado confere=false reprova."""
        cap = tmp_path / "cap_2.md"
        cap.write_text("""
```python
fake_command --nao-existe
```
<!-- cli-check: fonte=C; confere=false -->
""", encoding="utf-8")

        cmd_ok, cmd_sem, cmd_fab, erro = VCC.validar_capitulo(cap, 2)
        assert erro is None
        assert len(cmd_fab) == 1
        assert cmd_fab[0]["confere"] is False

    def test_capitulo_com_comando_nao_marcado(self, tmp_path):
        """Capítulo com comando sem marcação não reprova."""
        cap = tmp_path / "cap_3.md"
        cap.write_text("""
```sh
ls -la
```
""", encoding="utf-8")

        cmd_ok, cmd_sem, cmd_fab, erro = VCC.validar_capitulo(cap, 3)
        assert erro is None
        assert len(cmd_sem) == 1
        assert len(cmd_fab) == 0


class TestValidarObra:
    """Testa validacao de obra completa."""

    def test_obra_sem_categoria_tecnica_passa(self, tmp_path):
        """Obra com categoria_tecnica=false pula o gate."""
        # Setup: criar estrutura mínima
        dir_obra = tmp_path / "test_obra"
        dir_caps = dir_obra / "capitulos"
        dir_caps.mkdir(parents=True)
        (dir_caps / "cap_1.md").write_text("# Cap 1", encoding="utf-8")

        veredicto, resultado = VCC.validar_obra("test", categoria_tecnica=False)
        assert veredicto == "OK"
        assert resultado["motivo"] == "categoria_tecnica=false"

    def test_obra_com_comando_fabricado_reprova(self, tmp_path, monkeypatch):
        """Obra com comando fabricado reprovado em --estrito."""
        # Monkeypatch TO.dir_obra para retornar tmp_path
        import tipos_obra as TO
        monkeypatch.setattr(TO, "DIR_OUTPUT", tmp_path.parent)
        monkeypatch.setattr(TO, "DIR_PROJETO", tmp_path.parent)

        dir_obra = tmp_path / "obra_teste"
        dir_caps = dir_obra / "capitulos"
        dir_caps.mkdir(parents=True)

        (dir_caps / "cap_1.md").write_text("""
```bash
fake-command --invalid
```
<!-- cli-check: fonte=B; confere=false -->
""", encoding="utf-8")

        veredicto, resultado = VCC.validar_obra("obra_teste", categoria_tecnica=True, relatorio_dir=dir_obra / "validacao")
        assert veredicto == "REPROVADO"
        assert resultado["resumo_geral"]["fabricado"] == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
