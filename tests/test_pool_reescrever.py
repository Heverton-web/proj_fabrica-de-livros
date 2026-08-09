"""Testes do pool-capitulos --reescrever (V5.2, F1).

Cobre: backup do capítulo em revisao/backups/<ts>/, flag `reescrever` no estado
fazendo `montar_visao` tratar o capítulo como pendente mesmo com arquivo
entregue, e `--registrar --sucesso` limpando a flag e restaurando o fluxo.
"""

import sys

from conftest import carregar_script, CAPITULO_EITA

SLUG = "livros/obra-teste"


def _capitao_entregue():
    """CAPITULO_EITA do conftest tem 1408 chars; o pool exige corpo >= 3000."""
    return CAPITULO_EITA + "\n\n" + "Corpo complementar para passar do limite do pool. " * 60


def _pool():
    return carregar_script("pool-capitulos.py")


def _rodar(pool, *args, monkeypatch):
    monkeypatch.setattr(sys, "argv", ["pool-capitulos.py", SLUG, *args])
    return pool.main()


def _estado(pool):
    return pool.carregar_estado(SLUG)


def _backups(pool, livro_falso):
    dir_backups = livro_falso["dir_livro"] / "revisao" / "backups"
    return sorted(dir_backups.glob("*/cap_*.md")) if dir_backups.exists() else []


class TestReescrever:
    def test_marca_pendente_e_faz_backup(self, livro_falso, redirecionar_output,
                                        monkeypatch):
        pool = _pool()
        redirecionar_output(pool, livro_falso["raiz"])
        (livro_falso["dir_livro"] / "capitulos" / "cap_01.md").write_text(
            _capitao_entregue(), encoding="utf-8")

        assert _rodar(pool, "--reescrever", "1", monkeypatch=monkeypatch) == 0

        backups = _backups(pool, livro_falso)
        assert len(backups) == 1, f"esperado 1 backup, achou {len(backups)}"
        assert backups[0].name == "cap_01.md"
        original = (livro_falso["dir_livro"] / "capitulos" / "cap_01.md")
        assert backups[0].read_text(encoding="utf-8") == \
            original.read_text(encoding="utf-8")

        reg = _estado(pool)["capitulos"]["1"]
        assert reg["reescrever"] is True
        assert reg["estado"] == "pendente"
        assert reg["tentativas"] == 0

    def test_montar_visao_respeita_flag(self, livro_falso, redirecionar_output,
                                        monkeypatch):
        pool = _pool()
        redirecionar_output(pool, livro_falso["raiz"])
        # cap_02 vira entregue (EITA completo) para isolar o efeito da flag
        (livro_falso["dir_livro"] / "capitulos" / "cap_02.md").write_text(
            _capitao_entregue(), encoding="utf-8")

        _rodar(pool, "--reescrever", "1", monkeypatch=monkeypatch)
        visao = pool.montar_visao(SLUG, 4)

        por_num = {c["capitulo"]: c for c in visao}
        assert por_num["1"]["estado"] == "pendente"
        assert "reescrita" in por_num["1"]["motivo"]
        assert por_num["2"]["estado"] == "concluido_autonomo"

    def test_registrar_sucesso_limpa_flag(self, livro_falso, redirecionar_output,
                                          monkeypatch):
        pool = _pool()
        redirecionar_output(pool, livro_falso["raiz"])

        _rodar(pool, "--reescrever", "1", monkeypatch=monkeypatch)
        assert _estado(pool)["capitulos"]["1"]["reescrever"] is True

        assert _rodar(pool, "--registrar", "1", "--sucesso",
                      monkeypatch=monkeypatch) == 0
        reg = _estado(pool)["capitulos"]["1"]
        assert "reescrever" not in reg
        assert reg["estado"] == "concluido_autonomo"

        # fluxo normal restaurado: visao volta a considerar entregue
        # (cap_01 do conftest tem corpo curto; registrado concluido, a visao
        # revalida pelo arquivo — para passar, o cap precisa de 3000+ chars)
        (livro_falso["dir_livro"] / "capitulos" / "cap_01.md").write_text(
            _capitao_entregue(), encoding="utf-8")
        visao = pool.montar_visao(SLUG, 4)
        por_num = {c["capitulo"]: c for c in visao}
        assert por_num["1"]["estado"] == "concluido_autonomo"

    def test_cap_sem_arquivo_avisa_e_nao_faz_backup(self, livro_falso,
                                                    redirecionar_output,
                                                    monkeypatch, capsys):
        pool = _pool()
        redirecionar_output(pool, livro_falso["raiz"])

        assert _rodar(pool, "--reescrever", "99", monkeypatch=monkeypatch) == 0
        saida = capsys.readouterr().out
        assert "sem arquivo em disco" in saida
        assert _backups(pool, livro_falso) == []
        assert _estado(pool)["capitulos"]["99"]["reescrever"] is True

    def test_backup_em_ts_unico_por_execucao(self, livro_falso, redirecionar_output,
                                             monkeypatch):
        pool = _pool()
        redirecionar_output(pool, livro_falso["raiz"])

        _rodar(pool, "--reescrever", "1", monkeypatch=monkeypatch)
        _rodar(pool, "--reescrever", "2", monkeypatch=monkeypatch)

        backups = _backups(pool, livro_falso)
        assert len(backups) == 2
        nomes = {b.name for b in backups}
        assert nomes == {"cap_01.md", "cap_02.md"}
        # timestamps de backup preservam o arquivo original
        for b in backups:
            assert b.read_text(encoding="utf-8").startswith("# Capítulo")
