"""Testes dos helpers genericos de versionamento (R17) de tipos_obra.py."""

import tipos_obra as TO


class TestProximaVersaoArquivada:
    def test_primeira_versao_e_v1(self, tmp_path):
        assert TO.proxima_versao_arquivada(tmp_path / "versoes", "campanhas") == 1

    def test_incrementa_a_maior_existente(self, tmp_path):
        dir_versoes = tmp_path / "versoes"
        dir_versoes.mkdir()
        (dir_versoes / "campanhas-v1").mkdir()
        (dir_versoes / "campanhas-v3").mkdir()
        assert TO.proxima_versao_arquivada(dir_versoes, "campanhas") == 4

    def test_prefixos_diferentes_nao_se_misturam(self, tmp_path):
        dir_versoes = tmp_path / "versoes"
        dir_versoes.mkdir()
        (dir_versoes / "maquina-v5").mkdir()
        assert TO.proxima_versao_arquivada(dir_versoes, "campanhas") == 1


class TestArquivarParaVersoes:
    def test_move_a_pasta_de_origem(self, tmp_path):
        origem = tmp_path / "campanhas"
        origem.mkdir()
        (origem / "campanha.json").write_text("{}", encoding="utf-8")

        destino = TO.arquivar_para_versoes(origem, tmp_path / "versoes", "campanhas")

        assert destino == tmp_path / "versoes" / "campanhas-v1"
        assert not origem.exists()
        assert (destino / "campanha.json").is_file()

    def test_chamadas_sucessivas_incrementam(self, tmp_path):
        dir_versoes = tmp_path / "versoes"
        for _ in range(2):
            origem = tmp_path / "campanhas"
            origem.mkdir()
            TO.arquivar_para_versoes(origem, dir_versoes, "campanhas")

        assert (dir_versoes / "campanhas-v1").is_dir()
        assert (dir_versoes / "campanhas-v2").is_dir()

    def test_sem_origem_devolve_none(self, tmp_path):
        resultado = TO.arquivar_para_versoes(
            tmp_path / "nao-existe", tmp_path / "versoes", "campanhas")
        assert resultado is None
