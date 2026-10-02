# Livreto do reservarhospedagem — playbook

Peça funda de vendas, servida em `/livreto/` com PDF espelho em `/livreto.pdf`. Portado do
`acompanhaobra-site` (leia o `livreto/CLAUDE.md` de lá: as 4 travas do `@media print` quebram
em silêncio).

## A regra de ouro

> **Edite `content.py` e dê push. NÃO edite `livreto/index.html` (gerado).**

O CI (`.github/workflows/livreto.yml`) regenera o HTML, gera o PDF por Chromium headless, **abre o
PDF e mede** página em branco e commita o espelho (`livreto/index.html`, `livreto.pdf`,
`livreto/.espelho.sha`). O passo de commit usa `git status --porcelain`, porque `git diff --quiet`
não enxerga arquivo untracked (PDF do primeiro run ficaria fora do repo e `/livreto.pdf` daria 404).

## Onde editar

| Quero mudar | Arquivo |
|---|---|
| Texto dos cards, boards, "o que não faz", tiles | `content.py` |
| Capítulos, hero, CTA, SEO, nav | `build.py` → `build()` |
| Cenas dos storyboards (SVG line-art) | `build.py` → `SCENES` |
| Cores e CSS de tela e impressão | `build.py` → `CSS` |

## As 4 travas do `@media print`

1. `.rev{opacity:1}` — sem isto o PDF sai **EM BRANCO**.
2. `print-color-adjust:exact` — sem isto hero e CTA saem sem cor.
3. `break-inside:avoid` só nas unidades atômicas (card, painel). Nunca por capítulo.
4. `@page{size:A4}` — sem isto o Chrome imprime em Letter.

## Conteúdo: só o que roda

Fonte: `app/services/hospedagem/ROADMAP_site_reservas_hospedagem.md` (ERP, Ondas 0–2) e o roadmap
operacional em `portaria/`. O cabeçalho do `content.py` lista o que NÃO pode ser dito, e o guard
`.github/scripts/seo.py` reprova o push que prometer: sincronização com Airbnb/Booking/iCal,
channel manager, pagamento online no site, vitrine de vários condomínios, concorrente pelo nome,
"ninguém tem", prova social. A frase honesta **nega** ("não há sincronização…").

## Pendências

- **Fotos** (passo 4c): o livreto nasceu sem foto (hero é uma faixa de noites em CSS). Quando houver
  fotos geradas e julgadas, use `foto()`/`mrow()` do `build.py` — confira que `assets/x.jpg` existe;
  `seo.py` reprova referência a arquivo ausente. Todo arquivo novo em `assets/` refaz o PDF.
- Selos `piloto` (site de reservas e acerto) saem quando mais de um cliente operar.
