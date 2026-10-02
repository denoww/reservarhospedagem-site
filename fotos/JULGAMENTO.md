# Julgamento das fotos (02/10/2026)

Gerador: AWS Bedrock us-west-2 — Stable Image **Ultra** (hero, rosto) e **Core** (demais). OpenAI e Gemini
estavam sem crédito/cota. 3 candidatos por vaga, julgados olhando a imagem. Rubrica (0-10): vende? traz lead?
conversa com a copy? parece foto (mãos, olhos, dentes)? texto/tela alucinados? cara de stock? pessoas brancas europeias?
Candidatos ficam em `fotos/candidatos/` (gitignored). Os escolhidos estão em `assets/`.

| vaga | cand. | nota | motivo |
|---|---|---|---|
| hero | 1 | 6,5 | teal mais fiel à marca, mas a chave tem gravação que parece texto e o sujeito saiu à esquerda |
| hero | **2** | **8** | **escolhida**: mulher europeia, mão e chave limpas, sem texto; fundo teal-claro (mais frio que o #0F766E) |
| hero | 3 | 5 | fundo branco, fora do tom da marca |
| rosto | **1** | **8** | **escolhida**: hóspede sorri para o leitor discreto na parede; conceito claro, sem tela legível |
| rosto | 2 | 6 | não olha o leitor, parede ciano estourada |
| rosto | 3 | 7,5 | bom, mas olha para a câmera, não para o leitor |
| limpeza | 1 | 5,5 | camareira sentada lendo um papel: não é limpeza |
| limpeza | **2** | **8** | **escolhida**: dobra toalhas, mãos corretas, manta teal |
| limpeza | 3 | 6 | pose, sem tarefa |
| condominio | 1 | 6,5 | mão com relógio no botão, enquadramento apertado |
| condominio | **2** | **7** | **escolhida**: retrato sólido; não segura chaves como pedido |
| condominio | 3 | 7 | bom, mão com pingente estranho |
| pousada | 1 | 7 | boa, cozinha ao fundo |
| pousada | **2** | **7,5** | **escolhida**: sorriso natural, ambiente de pousada; fundo não ficou âmbar |
| pousada | 3 | 7 | relógio e luz ao fundo competem |
| hotel | 1 | 6,5 | braços cruzados, rígido |
| hotel | **2** | **7,5** | **escolhida**: recepcionista, mãos cruzadas plausíveis, lobby ao fundo |
| hotel | 3 | 7 | bom, pose frontal dura |

Nenhuma vaga ficou abaixo de 7 na escolhida, então não houve segunda rodada.
Limites conhecidos: o Ultra devolve 1344x768 (não 2016); os fundos de estúdio saíram mais frios/claros que o
#0F766E; pousada e hotel ganharam ambiente em vez de fundo âmbar/verde-ardósia.
Custo real: 6 chamadas Ultra (US$ 0,84) + 12 Core (US$ 0,48) = **US$ 1,32** (`fotos/CUSTO.log`).
