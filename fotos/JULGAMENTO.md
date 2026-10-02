# Julgamento das fotos (02/10/2026)

Gerador: AWS Bedrock us-west-2 — Stable Image **Ultra** (hero, rosto) e **Core** (demais). OpenAI e Gemini
estavam sem crédito/cota. 3 candidatos por vaga, julgados olhando a imagem. Rubrica (0-10): vende? traz lead?
conversa com a copy? parece foto (mãos, olhos, dentes)? texto/tela alucinados? cara de stock? pessoas brancas europeias?
Candidatos ficam em `fotos/candidatos/` (gitignored). Os escolhidos estão em `assets/`.

| vaga | cand. | nota | motivo |
|---|---|---|---|
| hero | 1 | 6,5 | teal mais fiel à marca, mas a chave tem gravação que parece texto e o sujeito saiu à esquerda |
| hero | 2 | 8 | (substituída em 02/10 a pedido do Rodrigo: fundo simples demais) — mulher europeia, mão e chave limpas, sem texto; fundo teal-claro (mais frio que o #0F766E) |
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


## Hero — 2ª rodada (02/10/2026, pedido do Rodrigo: 'fundo mais elaborado e sofisticado')

Mesma anfitriã, cenário de hotel boutique (lobby/suíte com latão, boiserie, luz quente). 3 candidatos no Ultra (US$ 0,42).

| vaga | cand. | nota | motivo |
|---|---|---|---|
| hero | 4 | 6 | corredor com portas de madeira escura; a chave tem gravação que lembra texto; fundo pouco sofisticado |
| hero | 5 | 6,5 | ambiente elegante (nichos com LED, arco), mas a mão ficou com o dedo apontando para baixo da chave, deformada |
| hero | **6** | **8** | **escolhida**: suíte de hotel com abajur de latão, boiserie e arco; rosto natural, mão e chave limpas, sem texto. Menos teal que a 1ª rodada, fica no neutro quente |

## Seção "Check-in sem recepção" — foto de destaque (02/10/2026, pedido do Rodrigo: 'capriche na chamada e na foto')

Vaga nova, 4:5, Ultra. 1ª rodada (3 cand.): cenário teal sofisticado, mas o hóspede de costas, sem rosto nem leitor — **reprovadas as três** (nota 4). 2ª rodada (US$ 0,42 perdidos por um prompt que não trocou; refeita): 

| cand. | nota | motivo |
|---|---|---|
| **c1** | **7,5** | **escolhida**: parede teal com boiserie, o hóspede olha para o leitor facial (equipamento plausível, câmera visível); micro-texto ilegível sob o leitor |
| c2 | 6,5 | retrato mais forte, mas o 'leitor' parece celular com interface alucinada; olha para a câmera, não para a porta |
| c3 | 7 | leitor com texto no topo; perfil bom |

### Foto da seção do facial — 3ª rodada (02/10/2026, pedido: 'o equipamento não parece Hikvision/Intelbras; precisa de destaque; quase 100% tela')

Gastos desta rodada: ~US$ 2,3 (4 Ultra só do leitor + 4 Ultra 'dois-shots' + 4 inpaint). Aprendizados:
- Citar a marca no prompt faz o modelo **escrever a marca** no aparelho (apareceu 'Hikvision' quase legível) — não citar.
- No 'dois-shots' (hóspede + leitor) o modelo **ignora o leitor** e desenha só a pessoa (4 de 4).
- Inpaint (`us.stability.stable-image-inpaint-v1:0`, precisa do perfil de inferência `us.`) redesenhou o leitor maior, mas saíram tablets genéricos/vazios e o rosto do hóspede mudou; reprovados.
- **Escolhida: `rosto_leitor_3`** (só o equipamento, parede teal, rosto na tela, câmera no topo, módulo de leitura). Apaguei por pós-edição o micro-texto de marca falsa. Limitação: não tem o hóspede em cena e o aparelho tem o módulo inferior (não é 100% tela).

### Foto do facial — 4ª rodada (02/10/2026): ENTRADA DO PRÉDIO + terminal moderno (referência: DS-K1T673 do print do Rodrigo)

Custo da rodada ≈ US$ 2,3 (4 control-structure a US$ 0,07 + 8 Ultra a US$ 0,14; log em `CUSTO.log`). Aprendizados:
- **Control-structure** (`us.stability.stable-image-control-structure-v1:0`) com o terminal da referência colado num canvas grande gerou **entradas de prédio ótimas, mas ignorou o aparelho e o hóspede** (aparelho pequeno demais para guiar). Depois passou a falhar com `INVALID_PAYMENT_INSTRUMENT` (assinatura AWS Marketplace do modelo, problema de cobrança da conta); Core/Ultra seguem funcionando.
- Pedir só o terminal (Ultra, prompt descritivo SEM marca) funciona: `terminal_u4` ficou parecido com a referência (3/4, silhueta no arco azul, câmeras no topo, botão em anel). Pedir a cena de entrada + terminal junto (`entrada_t1..3`) funciona sem hóspede: `entrada_t2` é a melhor cena.
- **Escolhida (composição)**: cena `entrada_t2` (nota 7,5: entrada de prédio, porta de vidro, hall aceso) + aparelho do `terminal_u4` (nota 7: desenho da referência) colado no lugar do aparelho original, com sombra, e micro-texto da barra apagado. Notas dos descartados: `entrada_t1` 6 (coluna alta, texto), `entrada_t3` 5 (aparelho pequeno, tela com foto de rua), `terminal_u1` 4 (texto alucinado), `terminal_u2` 5,5 (módulo de digital), `terminal_u3` 5.
- **Limitações**: sem hóspede em cena (3 tentativas de incluir pessoa+aparelho na mesma geração fizeram o modelo ignorar o aparelho); o relógio da tela mostra '100'; a foto é composição, não imagem única.

### Foto do facial — 5ª rodada (02/10/2026): aparelho 20% menor e tela chamativa

Pedido: 'diminua em 20% o equipamento e melhore a foto da tela — o atual é da foto original, queremos algo mais chamativo'.
- Aparelho reduzido de 477 px para 382 px de altura (×0,80), reconstruído **de frente** (o original estava em 3/4 e a cena é frontal): vidro alinhado, moldura prata simétrica, base com grade de alto-falante desenhada.
- **Tela redesenhada** (`tools/compor_entrada.py`, `tela_ui`): gradiente violeta→azul vívido, retrato de um homem europeu (`tela_retrato_2`, Core, US$ 0,04) em moldura neon ciano→magenta com cantos verdes, selo verde 'Acesso liberado', 'Bem-vindo!', relógio. Texto desenhado por nós, legível e em português.
- Parede limpa estendendo uma faixa limpa da pedra (listras horizontais); 1ª tentativa deixou a borda do aparelho antigo transparecer (margem estreita) — corrigido alargando o remendo; halo violeta suavizado.
- Custo: US$ 0,08 (2 retratos). A composição é local e reproduzível: `python3 tools/compor_entrada.py`.
- Limitações: continua sem o hóspede em cena; o rosto na tela é um retrato gerado (não identifica ninguém).
