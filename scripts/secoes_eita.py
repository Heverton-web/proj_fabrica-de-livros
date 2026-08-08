#!/usr/bin/env python3
"""
V5 — Parser canonico do framework EITA-V2 e primitivas de extracao de cards.

Fonte unica das funcoes que ate a V4 viviam duplicadas em auditar-obra.py.
Consumido por: auditar-obra.py, extrair-passos-praticos.py, gerar-lead-magnet.py,
gerar-deck.py, validar-playbook.py.

Uso como biblioteca:
    from secoes_eita import (SECOES_EITA, sem_acento, dividir_secoes,
                             secao_por_nome, itens_de_lista, blocos_de_codigo,
                             comandos_executaveis, caminhos_de_arquivo,
                             subtitulos, primeiro_paragrafo, subsecao)
"""

import re
import unicodedata

SECOES_EITA = [
    (1, "Introdução"), (2, "Explica"), (3, "Ilustra"), (4, "Técnica"),
    (5, "Aplica"), (6, "Conclusão"), (7, "Referências"),
]

# Numero da secao por apelido curto (usado pelos extratores)
SECAO = {"introducao": 1, "explica": 2, "ilustra": 3, "tecnica": 4,
         "aplica": 5, "conclusao": 6, "referencias": 7}

RE_CODIGO = re.compile(r"^[ \t]*```.*?^[ \t]*```[ \t]*$", re.DOTALL | re.MULTILINE)
RE_BLOCO_LING = re.compile(r"^[ \t]*```[ \t]*([A-Za-z0-9_+-]*)[ \t]*\n(.*?)^[ \t]*```[ \t]*$",
                           re.DOTALL | re.MULTILINE)
RE_MERMAID = re.compile(r"^[ \t]*```[ \t]*mermaid", re.MULTILINE | re.IGNORECASE)

# Item de lista: "- x", "* x", "1. x", "- [ ] x"
RE_ITEM_LISTA = re.compile(r"^[ \t]*(?:[-*+]|\d{1,2}[\.\)])[ \t]+(?:\[[ xX]\][ \t]+)?(.+?)[ \t]*$",
                           re.MULTILINE)

RE_SUBTITULO = re.compile(r"^(#{3,4})[ \t]+(.+?)[ \t]*$", re.MULTILINE)

# Comando executavel no inicio de linha dentro de bloco de codigo
EXECUTAVEIS = ("python", "python3", "py", "pytest", "pip", "uv", "bash", "sh",
               "powershell", "pwsh", "git", "node", "npm", "npx", "pnpm", "yarn",
               "docker", "typst", "pandoc", "make", "cargo", "go", "curl", "./")
RE_COMANDO = re.compile(
    r"^[ \t]*(?:\$[ \t]+|>[ \t]+|PS[ \t]*>[ \t]*)?((?:" + "|".join(
        re.escape(e) for e in EXECUTAVEIS) + r")\b.*)$",
    re.MULTILINE)

# Caminho de arquivo em crase: contem "/" ou termina numa extensao conhecida
EXTENSOES = ("py", "md", "json", "typ", "yml", "yaml", "toml", "ps1", "sh", "js",
             "mjs", "ts", "tsx", "html", "css", "epub", "pdf", "png", "svg",
             "txt", "csv", "sql", "ini", "cfg", "env")
RE_PATH_CRASE = re.compile(
    r"`([^`\n]*?(?:/[^`\n]+|\.(?:" + "|".join(EXTENSOES) + r"))[^`\n]*?)`")

# Ruido comum que nao e caminho de arquivo
RE_NAO_PATH = re.compile(r"^(?:https?://|[<>{}\[\]|]|\s*$)")


def sem_acento(texto):
    texto = unicodedata.normalize("NFKD", texto)
    return "".join(c for c in texto if not unicodedata.combining(c))


def normalizar(texto):
    return sem_acento(texto or "").lower().strip()


def dividir_secoes(texto):
    """Retorna dict {numero_secao: {'titulo','corpo'}} conforme o template EITA-V2."""
    secoes = {}
    marcas = []
    for m in re.finditer(r"^##\s*(\d)[\.\)]?\s*(.+)$", texto, re.MULTILINE):
        marcas.append((int(m.group(1)), m.group(2).strip(), m.start(), m.end()))
    for i, (num, titulo, _ini, fim) in enumerate(marcas):
        prox = marcas[i + 1][2] if i + 1 < len(marcas) else len(texto)
        secoes[num] = {"titulo": titulo, "corpo": texto[fim:prox]}
    return secoes


def cabecalho_secao(numero, nome):
    """Regex tolerante para `## 1. Introdução` (aceita variacao de acento/caixa)."""
    alvo = sem_acento(nome).lower()[:6]
    return re.compile(rf"^##\s*{numero}[\.\)]?\s*(?P<t>.+)$", re.MULTILINE), alvo


def secao_por_nome(secoes, apelido):
    """secoes: saida de dividir_secoes(). apelido: 'tecnica', 'aplica', ...

    Confere o titulo alem do numero (capitulo com secao trocada nao passa)."""
    numero = SECAO.get(normalizar(apelido))
    if numero is None:
        return ""
    atual = secoes.get(numero)
    if atual is None:
        return ""
    nome_oficial = dict(SECOES_EITA)[numero]
    alvo = sem_acento(nome_oficial).lower()[:6]
    if alvo not in sem_acento(atual["titulo"]).lower():
        return ""
    return atual["corpo"]


def sem_codigo(texto):
    return RE_CODIGO.sub("", texto or "")


def itens_de_lista(texto, minimo_palavras=2, limite=None):
    """Itens de lista de 1o nivel, sem marcador, sem duplicata, na ordem original."""
    vistos, saida = set(), []
    for m in RE_ITEM_LISTA.finditer(sem_codigo(texto)):
        item = m.group(1).strip().strip("*_ ").rstrip(".")
        item = re.sub(r"\s+", " ", item)
        if len(item.split()) < minimo_palavras:
            continue
        chave = normalizar(item)[:80]
        if chave in vistos:
            continue
        vistos.add(chave)
        saida.append(item)
        if limite and len(saida) >= limite:
            break
    return saida


# Verbos que abrem uma instrucao acionavel em PT-BR. Usados para quebrar prosa
# imperativa em itens binarios quando o autor NAO escreveu o exercicio em lista
# ("Execute o prompt, verifique a entrega, faca o commit e responda...").
VERBOS_IMPERATIVOS = (
    "abra", "adicione", "ajuste", "anote", "aplique", "commite", "compare",
    "configure", "confira", "crie", "defina", "documente", "escolha", "escreva",
    "execute", "faca", "gere", "identifique", "implemente", "instale", "liste",
    "meca", "publique", "refatore", "registre", "remova", "responda", "revise",
    "rode", "salve", "teste", "valide", "verifique", "repita", "compile",
    "descreva", "explique", "justifique", "reescreva", "substitua", "marque",
)
RE_INICIO_IMPERATIVO = re.compile(
    r"^(?:" + "|".join(VERBOS_IMPERATIVOS) + r")\b", re.IGNORECASE)
RE_FIM_FRASE = re.compile(r"(?<=[\.\!\?;])\s+")
RE_SEPARADOR_CLAUSULA = re.compile(r",\s+|\s+e\s+(?=[a-zà-ÿ])")


def itens_binarios(texto, limite=None, minimo_palavras=3):
    """Itens verificaveis de um trecho: lista quando existe, prosa imperativa senao.

    O framework EITA nao obriga o "Exercicio Pratico" a ser uma lista — boa parte
    dos capitulos escreve uma frase encadeada. Sem esta quebra, o card sai com
    'Feito quando' vazio e o gate reprova por R-PBK-4 um capitulo que, na verdade,
    tem o exercicio escrito."""
    itens = itens_de_lista(texto, limite=limite)
    if itens:
        return itens

    saida, vistos = [], set()
    for frase in RE_FIM_FRASE.split(sem_codigo(texto or "")):
        frase = re.sub(r"\s+", " ", frase).strip()
        if not frase or frase.startswith(("#", ">", "|")):
            continue
        partes = RE_SEPARADOR_CLAUSULA.split(frase)
        for i, bruto in enumerate(partes):
            item = bruto.strip().strip("*_ ").rstrip(".;:,")
            if len(item.split()) < minimo_palavras:
                continue
            # 1a clausula da frase entra sempre; as seguintes so se forem ordens
            if i > 0 and not RE_INICIO_IMPERATIVO.match(sem_acento(item)):
                continue
            chave = normalizar(item)[:80]
            if chave in vistos:
                continue
            vistos.add(chave)
            saida.append(item[0].upper() + item[1:] if item else item)
            if limite and len(saida) >= limite:
                return saida
    return saida


def blocos_de_codigo(texto, ignorar_mermaid=True):
    """[{'linguagem': str, 'codigo': str}] na ordem de aparicao."""
    saida = []
    for m in RE_BLOCO_LING.finditer(texto or ""):
        ling = (m.group(1) or "").lower()
        if ignorar_mermaid and ling == "mermaid":
            continue
        codigo = m.group(2).rstrip()
        if codigo.strip():
            saida.append({"linguagem": ling or "text", "codigo": codigo})
    return saida


def comandos_executaveis(texto, limite=None):
    """Linhas de comando dentro de blocos de codigo (bash/ps/python -m ...)."""
    vistos, saida = set(), []
    for bloco in blocos_de_codigo(texto):
        for m in RE_COMANDO.finditer(bloco["codigo"]):
            cmd = m.group(1).strip()
            if cmd.endswith("\\") or len(cmd) > 240:
                continue
            chave = normalizar(cmd)
            if chave in vistos:
                continue
            vistos.add(chave)
            saida.append(cmd)
            if limite and len(saida) >= limite:
                return saida
    return saida


def caminhos_de_arquivo(texto, limite=None):
    """Paths citados em crase na secao (viram as 'entregas' do card)."""
    vistos, saida = set(), []
    for m in RE_PATH_CRASE.finditer(texto or ""):
        alvo = m.group(1).strip()
        if RE_NAO_PATH.match(alvo) or " " in alvo or len(alvo) > 120:
            continue
        chave = alvo.lower()
        if chave in vistos:
            continue
        vistos.add(chave)
        saida.append(alvo)
        if limite and len(saida) >= limite:
            break
    return saida


def subtitulos(texto):
    """[(nivel, titulo)] dos ### / #### da secao."""
    return [(len(m.group(1)), m.group(2).strip())
            for m in RE_SUBTITULO.finditer(texto or "")]


def subsecao(texto, *apelidos):
    """Corpo do primeiro ### cujo titulo contenha um dos apelidos (sem acento/caixa)."""
    if not texto:
        return ""
    marcas = list(RE_SUBTITULO.finditer(texto))
    alvos = [normalizar(a) for a in apelidos]
    for i, m in enumerate(marcas):
        titulo = normalizar(m.group(2))
        if any(a in titulo for a in alvos):
            fim = marcas[i + 1].start() if i + 1 < len(marcas) else len(texto)
            return texto[m.end():fim]
    return ""


def primeiro_paragrafo(texto, max_chars=400):
    """Primeiro paragrafo de prosa (ignora codigo, titulos, listas e citacoes)."""
    limpo = sem_codigo(texto or "")
    for bruto in re.split(r"\n\s*\n", limpo):
        p = bruto.strip()
        if not p or p.startswith(("#", ">", "|", "-", "*", "!", "1.")):
            continue
        p = re.sub(r"\s+", " ", p)
        p = re.sub(r"\[\d{1,3}\]", "", p).strip()
        if len(p.split()) < 8:
            continue
        return p[:max_chars].rsplit(" ", 1)[0] + ("…" if len(p) > max_chars else "")
    return ""


def titulo_do_capitulo(texto, padrao=""):
    """Texto do primeiro `# Titulo` do arquivo, sem numeracao residual."""
    m = re.search(r"^#[ \t]+(.+?)[ \t]*$", texto or "", re.MULTILINE)
    if not m:
        return padrao
    # Remove "Capítulo 3", "3." e o travessão/hífen separador que costuma segui-los
    return re.sub(r"^(?:Cap[íi]tulo\s*)?\d+\s*[\.\):\-–—]?\s*[\-–—]?\s*", "",
                  m.group(1).strip())
