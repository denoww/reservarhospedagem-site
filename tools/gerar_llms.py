#!/usr/bin/env python3
"""Gera `llms.txt` a partir de `tools/marca.json` (fonte única). Só biblioteca padrão.

  python3 tools/gerar_llms.py          # escreve llms.txt na raiz
  python3 tools/gerar_llms.py --check  # não escreve; sai 1 se o llms.txt difere do gerado

POR QUE: o llms.txt escrito à mão derivou em menos de 24 h nos outros sites (ROADMAP_multi_produto §7.6).
Aqui o texto sai SEMPRE da mesma fonte, e `tools/conferir_llms.py` roda no CI.
"""
import json
import pathlib
import sys

RAIZ = pathlib.Path(__file__).resolve().parent.parent
FONTE = RAIZ / "tools" / "marca.json"
SAIDA = RAIZ / "llms.txt"


def lista(itens):
    return "\n".join(f"- {i}" for i in itens)


def gerar(m):
    p = m["preco"]
    partes = [
        f"# {m['nome']}",
        f"> {m['tagline']}",
        f"{m['familia']}",
        f"## Para quem é\n{m['para_quem']}\n\nEstado: {m['estado']}",
        f"## O que o produto faz\n{lista(m['faz'])}",
        f"## Como o hóspede entra\n{lista(m['acesso'])}",
        f"## Preço\n{p['modelo']}\n{lista(p['faixas'])}\n\n{p['unidade_ativa']}\n{p['exemplos']}\n\n{p['nota']}",
        f"## O que o produto NÃO faz\n{lista(m['nao_faz'])}",
        f"## Dados pessoais\n{m['lgpd']}",
        f"## Links\n- Site: {m['site']}\n- Login: {m['login']}\n- Blog: {m['blog']}\n- Livreto: {m['livreto']}",
        "---\nGerado de `tools/marca.json` por `tools/gerar_llms.py`. NÃO edite à mão: mude a fonte e gere de novo.",
    ]
    return "\n\n".join(partes) + "\n"


if __name__ == "__main__":
    texto = gerar(json.loads(FONTE.read_text(encoding="utf-8")))
    if "--check" in sys.argv:
        atual = SAIDA.read_text(encoding="utf-8") if SAIDA.exists() else ""
        if atual != texto:
            print("llms.txt difere do gerado por tools/marca.json — rode `python3 tools/gerar_llms.py`")
            sys.exit(1)
        print("llms.txt bate com tools/marca.json")
    else:
        SAIDA.write_text(texto, encoding="utf-8")
        print(f"escrito {SAIDA} ({len(texto)} bytes)")
