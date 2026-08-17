import re, sys
for n in range(1, 9):
    f = f"output/git-github-submodules/livros/git-github-submodules/capitulos/cap_{n}.md"
    try:
        t = open(f, encoding="utf-8").read()
    except FileNotFoundError:
        print(f"cap_{n}: AUSENTE")
        continue
    body = re.sub(r"```.*?```", "", t, flags=re.S)
    cited = set(int(x) for x in re.findall(r"\[(\d{1,2})\](?!\()", body))
    listed = set(int(x) for x in re.findall(r"^\- \[(\d{1,2})\]", t, re.M))
    orphans = cited - listed
    unused = listed - cited
    print(f"cap_{n}: {len(t)} chars | refs: {len(listed)} | citadas: {sorted(cited)} | orfas: {sorted(orphans)} | nao-citadas: {sorted(unused)}")
