#!/usr/bin/env python3
"""Guarda do llms.txt (CI `llms.yml`). Não edita o `seo.py` (byte a byte igual nos 4 sites).

1. `llms.txt` bate com o que `tools/gerar_llms.py` gera de `tools/marca.json` (sem edição à mão).
2. Os valores de preço do llms.txt são EXATAMENTE os da tabela visível em `index.html` (#preco): o assistente de IA
   lê um, o visitante lê o outro, e os dois não podem divergir.
3. Frases proibidas: o facial não abre a porta do quarto, e a senha da fechadura não pode ser dada como pronta.
"""
import pathlib
import re
import subprocess
import sys

RAIZ = pathlib.Path(__file__).resolve().parent.parent
erros = []

r = subprocess.run([sys.executable, str(RAIZ / "tools" / "gerar_llms.py"), "--check"], capture_output=True, text=True)
if r.returncode:
    erros.append(r.stdout.strip() or "llms.txt difere do gerado")

llms = (RAIZ / "llms.txt").read_text(encoding="utf-8")
home = (RAIZ / "index.html").read_text(encoding="utf-8")
secao = re.search(r'<section id="preco".*?</section>', home, re.S)
if not secao:
    erros.append("index.html sem <section id=\"preco\"> — não dá para conferir o preço")
else:
    visivel = re.sub(r"<[^>]+>|&nbsp;", " ", secao.group(0))
    em_llms = set(re.findall(r"R\$\s?(\d+,\d{2})", llms))
    na_home = set(re.findall(r"R\$\s?(\d+,\d{2})", visivel))
    # exemplos de conta (19,60 / 39,20 / 97,20) e faixas (4,90 / 2,90 / 1,90) devem existir nos dois lados
    so_llms, so_home = em_llms - na_home, na_home - em_llms
    if so_llms:
        erros.append(f"preço só no llms.txt, não na home: {sorted(so_llms)}")
    if so_home:
        erros.append(f"preço só na home, não no llms.txt: {sorted(so_home)}")
    if not em_llms:
        erros.append("llms.txt sem nenhum preço")

for padrao, porque in [
    (r"(facial|reconhecimento facial|rosto)[^.\n]{0,60}(abre|libera)[^.\n]{0,30}(porta d[oa] (quarto|apartamento))", "o facial não abre a porta do quarto"),
    (r"(sistema|nós) envia(mos)? a senha da fechadura", "a senha da fechadura por WhatsApp ainda não existe"),
]:
    for linha in llms.splitlines():
        if re.search(padrao, linha, re.I) and "NÃO" not in linha and "não" not in linha:
            erros.append(f"llms.txt: {porque}: {linha[:90]}")

if erros:
    print("llms.txt REPROVADO:")
    for e in erros:
        print(" -", e)
    sys.exit(1)
print("llms.txt ok:", len(llms), "bytes; preços iguais aos da home:", sorted(em_llms))
