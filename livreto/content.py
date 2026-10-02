# -*- coding: utf-8 -*-
"""Conteúdo do livreto do reservarhospedagem — 95% das mudanças acontecem AQUI.

VOCÊ SÓ PRECISA EDITAR ESTE ARQUIVO. O HTML e o PDF se regeneram sozinhos no CI
(.github/workflows/livreto.yml) assim que você der push — o PDF é um ESPELHO
automático. O CI abre o PDF e barra o build se alguma página sair EM BRANCO.

Fonte da verdade do que pode ser dito, nesta ordem:
  1. `app/services/hospedagem/ROADMAP_site_reservas_hospedagem.md` no repo do ERP
     (denoww/seucondominio) — Ondas 0–2 em produção. Nada entra aqui sem estar lá.
  2. `app/services/portaria/ROADMAP_meus_visitantes_como_hospedes.md` — a camada
     operacional (estadia, porta, quadro, limpeza).

⛔ REGRAS DE COPY — o que NÃO pode ser prometido (o guard `.github/scripts/seo.py`
   reprova o push que escrever qualquer uma; a frase honesta NEGA):
  • Sincronização com Airbnb, Booking ou iCal (Onda 3) e channel manager (3.5).
  • Pagamento online / checkout automático no site (Onda 4).
  • Avaliações, tarifa de recorrente, vitrine reunindo vários condomínios (5 e 6).
  • "Porta = verdade" (4.5): o checkout que dispara a limpeza NÃO é lido da porta.
  • Concorrente pelo nome, "ninguém tem", prova social
    inventada ("X condomínios"), número não verificado.
  • Preço: só a tabela aprovada pelo Rodrigo em 02/10/2026 (ver PRECO_NOTA). Nada além dela.
"""
from pathlib import Path

WA = "https://wa.me/" + (Path(__file__).parent.parent / ".whatsapp").read_text().strip()
WA_TXT = "?text=Ol%C3%A1%21%20Vi%20o%20livreto%20do%20reservarhospedagem%20e%20quero%20conhecer."
SITE = "https://www.reservarhospedagem.app"

HERO = {
    "eyebrow": "Livreto",
    "h1": "Reserva direta, hóspede com acesso liberado e limpeza avisada.",
    "sub": "Preço por tipo de acomodação, pedido de reserva no seu site, acerto com o proprietário, "
           "entrada do prédio com reconhecimento facial e limpeza avisada no horário do checkout. "
           "Convive com o Airbnb: a reserva que vem de lá você lança no balcão. Para condomínios que "
           "operam temporada, flats, pousadas e hotéis pequenos — tudo no mesmo sistema da portaria.",
}

CREDO = ('A comissão da plataforma e o cadastro do hóspede deixam de ser o seu preço de entrada. '
         'O que você vende, a quem e por quanto fica <span class="g">no seu sistema</span>, '
         'e o hóspede chega por um site que é seu.')

# (chave, capítulo-cor, título, [(cena, título, legenda)])
BOARDS = {
    "reserva": ("terra", "Do pedido ao hóspede dentro do apartamento", [
        ("calendario", "O hóspede pede",       "Escolhe as noites no site e envia o pedido com documento e foto."),
        ("balcao",     "A recepção confirma",  "Atribui a unidade e confirma. O pedido vira reserva."),
        ("face",       "O acesso nasce",       "Confirmada a reserva, o facial libera a entrada do prédio durante a estadia."),
        ("porta",      "Entra no prédio e no quarto", "Facial na entrada; no quarto, a senha da fechadura ou a chave com o porteiro."),
        ("vassoura",   "No checkout, a limpeza dispara", "No horário registrado, a tarefa vai para a camareira."),
        ("chave",      "Unidade pronta",       "Vistoriada, volta para a venda."),
    ]),
    "acerto": ("petroleo", "Do dinheiro que entrou ao PIX do proprietário", [
        ("lista",   "Reservas do período", "Todas as estadias que saíram no mês, por unidade."),
        ("vassoura","Limpeza à parte",     "A taxa de limpeza sai antes: é serviço do condomínio."),
        ("percent", "Retenção do condomínio", "O percentual é você que define, por proprietário."),
        ("moeda",   "Líquido a repassar",  "Com a chave PIX do proprietário na própria folha."),
        ("pdf",     "PDF para conferir",   "O documento que acompanha o PIX e responde a dúvida."),
    ]),
    "limpeza": ("ambar", "Do checkout à unidade pronta", [
        ("porta",   "Chega o horário do checkout", "O sistema abre a tarefa de limpeza sozinho."),
        ("vassoura","A camareira limpa",   "Recebe a tarefa e roda o checklist no celular."),
        ("foto",    "Foto por etapa",      "A evidência fica registrada com data e hora."),
        ("lupa",    "A vistoria à distância", "O gestor confere pelas fotos, sem ir ao local."),
        ("chave",   "Pronta para vender",  "O status da unidade muda no quadro."),
    ]),
}

PRECO_CARDS = [
    ("Preço por tipo de acomodação",
     "Você vende o tipo — estúdio, dois quartos, chalé —, e a unidade é atribuída depois. Tipo com "
     "uma única unidade funciona do mesmo jeito.", ""),
    ("Tarifa base, temporada e fim de semana",
     "A tarifa de maior prioridade vigente em cada noite vence. A alta temporada cobre o Carnaval "
     "sem apagar a tarifa padrão.", ""),
    ("Estadia mínima e hóspede adicional",
     "A regra de estadia mínima e o valor por hóspede além da capacidade entram no cálculo, "
     "noite por noite.", ""),
    ("Taxa de limpeza por estadia",
     "Uma por estadia, não por noite. Aparece decomposta no orçamento, em vez de embutida na diária.", ""),
    ("O total vem decomposto",
     "Quem confere vê diárias, adicionais e limpeza separados — nunca só um número que ninguém "
     "consegue explicar depois.", ""),
    ("Bloqueio por período",
     "Manutenção ou uso do proprietário tiram a unidade, ou o tipo inteiro, de venda por um "
     "período — e a disponibilidade já os considera.", ""),
]

RESERVA_CARDS = [
    ("Reserva no balcão",
     "A recepção cria a reserva, atribui a unidade e confirma. O orçamento fica congelado: a "
     "tarifa pode mudar depois sem alterar o que foi vendido.", ""),
    ("Estadia que não se sobrepõe",
     "O sistema recusa duas estadias na mesma unidade ao mesmo tempo, e quem sai no dia 12 libera "
     "a noite do 12 para venda.", ""),
    ("Política de cancelamento",
     "A reserva tem estados claros — pré-reserva, confirmada, cancelada — e a política de "
     "cancelamento fica registrada nela.", ""),
    ("Hóspede que volta",
     "Se o CPF já está cadastrado, a confirmação reaproveita o cadastro, e não trava justamente no "
     "cliente que volta todo ano.", ""),
    ("Reserva vira estadia",
     "Confirmar a reserva gera a liberação de acesso, o voucher e o lugar no quadro, sem digitar "
     "a mesma estadia duas vezes.", ""),
    ("Quem opera, não mexe no preço",
     "A recepção opera as reservas sem poder alterar acomodações e tarifas. São permissões "
     "separadas.", ""),
]

SITE_CARDS = [
    ("Um site de reservas seu",
     "Uma página no endereço do seu condomínio, com a faixa de noites, a ficha de cada tipo, a "
     "política, o FAQ e o mapa.", "piloto"),
    ("Escrito para o Google ler",
     "O conteúdo vem no HTML, não montado no navegador: título, descrição, dados estruturados e "
     "o preço real. Quem ainda não tem foto, descrição e tarifa não é indexado.", "piloto"),
    ("Pedido em três passos",
     "Datas e acomodação, dados do hóspede com documento e foto, confirmação. O preço é recalculado "
     "no servidor e a disponibilidade é conferida de novo no envio.", "piloto"),
    ("Fecha como pré-reserva",
     "O pedido chega como pré-reserva e a recepção confirma no ERP. Ninguém recebe confirmação "
     "automática de uma unidade que já foi fechada no balcão.", "piloto"),
    ("O hóspede volta pelo link",
     "A reserva tem um link próprio, só dele, para acompanhar o pedido.", "piloto"),
    ("Você controla o que aparece",
     "Ligar, desligar, textos, horários, política, regras e FAQ saem de uma tela do sistema. O "
     "site nasce desligado e só entra no ar quando você decide.", ""),
]

ESTADIA_CARDS = [
    ("Entrada do prédio só durante a estadia",
     "A liberação facial do hóspede vale para a estadia, no equipamento de controle de acesso do "
     "condomínio, na entrada do prédio. Passou do prazo, deixa de abrir.", ""),
    ("Porta do quarto: senha ou chave",
     "O sistema envia a senha da fechadura ao hóspede. Se o prédio tem porteiro, é o porteiro "
     "quem entrega a chave do quarto.", ""),
    ("Cadastro antes de chegar",
     "O hóspede preenche documento e foto por um link, antes de chegar. Na chegada, ele entra com "
     "o rosto na portaria, sem passar pela recepção.", ""),
    ("Voucher em PDF",
     "A estadia tem voucher com os dados da reserva e da unidade, para quem precisa de um papel.", ""),
    ("Tudo no mesmo sistema da portaria",
     "Quem já administra os acessos do condomínio não abre um segundo painel: a estadia e a "
     "portaria são o mesmo cadastro.", ""),
]

LIMPEZA_CARDS = [
    ("O checkout abre a tarefa",
     "No fim da estadia a tarefa de limpeza nasce sozinha, sem ninguém lembrar de criar.", ""),
    ("Checklist com foto",
     "A camareira roda o checklist da unidade no celular e anexa fotos com data e hora por etapa.", ""),
    ("Vistoria à distância",
     "O gestor confere pelas fotos, sem ir ao local, e marca a unidade como pronta.", ""),
    ("Status da unidade",
     "Suja, limpa, vistoriada, fora de serviço: o estado de cada unidade aparece no quadro, ao "
     "lado das reservas.", ""),
    ("Quem está atrasado",
     "O quadro mostra o que ficou sem arrumação e há quantas horas, em vez de você descobrir "
     "quando o próximo hóspede chega.", ""),
]

ACERTO_CARDS = [
    ("Acerto por proprietário e período",
     "Por unidade e por período: reservas, receita bruta, taxa de limpeza, retenção do condomínio "
     "e líquido a repassar.", "piloto"),
    ("Corte pelo check-out",
     "Entra no período a estadia que saiu nele, que é quando o serviço foi prestado.", "piloto"),
    ("A retenção é sua",
     "O percentual é um parâmetro na tela, definido por proprietário. O sistema não chuta quanto "
     "o condomínio fica.", "piloto"),
    ("O PIX sai com a chave na folha",
     "A chave PIX do proprietário aparece no relatório. Quando falta, o relatório avisa, em vez de "
     "deixar passar.", "piloto"),
    ("O que foi vendido, não o que está na tarifa hoje",
     "O acerto lê o orçamento congelado de cada reserva. Mudar a tarifa depois não altera o "
     "repasse de meses atrás.", "piloto"),
    ("PDF com a memória de cálculo",
     "Uma folha com o cabeçalho do condomínio e a conta aberta, para o proprietário conferir.", "piloto"),
]

QUADRO_CARDS = [
    ("Quadro de hospedagem",
     "Quem dorme onde, quem chega, quem sai hoje e o que ficou para trás, numa tela só.", ""),
    ("Mapa de reservas",
     "Linha por unidade, barra por estadia, bloqueio como período, e o popover com o que dá para "
     "fazer em cada reserva.", ""),
    ("Números de ocupação",
     "Ocupação e o estado das unidades no mesmo nível dos números do dia, não numa aba escondida.", ""),
    ("Ações em lote",
     "Marcar várias unidades de uma vez, para a governança que atende o andar inteiro.", ""),
    ("Dois eixos, sem confusão",
     "A cor diz se a unidade está ocupada; a etiqueta diz se está limpa. Lê de longe, que é como o "
     "gerente usa.", ""),
]

SETORES = [
    ("Condomínio com temporada", "Apartamentos alugados por temporada, onde o condomínio já controla a "
                                 "portaria e quer controlar também a reserva e o acerto."),
    ("Flat e condo-hotel",       "Proprietário investidor, operador no meio e a pergunta de sempre: "
                                 "quanto entrou, quanto fica, quanto vai pra quem."),
    ("Pousada pequena",          "Poucos quartos, planilha e WhatsApp, e a hora em que a planilha "
                                 "para de dar conta."),
    ("Clube com chalés",         "Chalé, unidade de lazer ou multipropriedade que precisa de preço, "
                                 "reserva e acesso na mesma mão."),
]

DORES = [
    "A reserva chega pelo WhatsApp, a data é fechada na planilha e alguém esquece de atualizar a outra aba.",
    "O proprietário pergunta quanto ficou no mês e a resposta depende de somar três planilhas.",
    "O hóspede chega às 22h e não tem quem entregue a chave.",
    "O hóspede pediu mais dois dias e, na manhã seguinte, o acesso dele já venceu.",
    "O apartamento foi liberado sujo porque ninguém viu que o checkout já tinha acontecido.",
    "A comissão da plataforma come uma fatia de cada diária, e o cadastro do hóspede fica com ela.",
]

PRECO_NOTA = [
    ("As 2 primeiras unidades são grátis",
     "A cobrança é por unidade ativa, por mês. Quem opera pouco começa sem pagar nada."),
    ("Preço por faixa de unidades",
     "R$&nbsp;4,90 por unidade da 3ª à 10ª, R$&nbsp;2,90 da 11ª à 30ª e R$&nbsp;1,90 da 31ª em diante. "
     "Quanto mais unidades, menos cada uma custa."),
    ("Sem implantação, sem fidelidade, sem comissão",
     "Não há taxa de implantação, nem contrato de fidelidade, nem percentual sobre as reservas do "
     "seu site. O objetivo do produto é tirar a comissão do caminho."),
    ("O que é unidade ativa",
     "A unidade ligada a um tipo de acomodação publicado no site e à venda em pelo menos um dia do "
     "mês. Apartamento cadastrado que não está à venda não paga."),
    ("Exemplos de mensalidade",
     "6 unidades ativas: R$&nbsp;19,60 por mês. 10 unidades: R$&nbsp;39,20. 30 unidades: R$&nbsp;97,20."),
    ("Piloto de verdade",
     "Há um condomínio operando temporada sobre o módulo. Conte o seu caso e a gente mostra o "
     "que já roda, sem prometer o que ainda não existe."),
]

NAO_FAZ = [
    ("Não há sincronização com Airbnb e Booking",
     "Se você vende por uma plataforma, ela continua separada do seu calendário. Não existe "
     "sincronização automática de datas: você bloqueia na mão a unidade que foi vendida lá fora. "
     "Quem opera nas duas pontas precisa conviver com esse risco de reserva duplicada.", ""),
    ("Não distribui preço para outros canais",
     "O sistema não é um gestor de canais. Ele não publica tarifa nem disponibilidade em outras "
     "plataformas — o seu preço vive no seu site.", ""),
    ("Não existe pagamento online no site",
     "O hóspede envia o pedido, a recepção confirma e a cobrança segue o fluxo que o condomínio já "
     "tem. Não há checkout com PIX ou cartão fechando a reserva sozinho.", ""),
    ("A reserva do site é uma pré-reserva",
     "Ela só vira reserva quando alguém confirma. É de propósito: a unidade pode ter sido fechada "
     "no balcão entre o hóspede ver a página e enviar o pedido.", ""),
    ("O checkout não é lido pela porta",
     "A tarefa de limpeza nasce da reserva e do horário de saída registrado no sistema. A leitura "
     "do acesso real do hóspede na saída ainda não dispara a limpeza.", ""),
    ("Não paga o proprietário por você",
     "O acerto é um relatório com a chave PIX. Quem transfere é o condomínio, e o tratamento "
     "contábil e tributário do repasse é conversa com o seu contador.", ""),
    ("Não existe vitrine com vários condomínios",
     "O site é o do seu condomínio. Não há busca reunindo várias propriedades, nem avaliações de "
     "hóspedes, nem cupom de retorno.", ""),
    ("Não decide se a convenção permite temporada",
     "Há condomínios cuja convenção proíbe locação por temporada, e isso é jurídico, não de "
     "software. O sistema serve a quem opera — e não deve ser contratado por quem não pode.", ""),
]

LEI = [
    ("A convenção do condomínio manda",
     "O STJ admite que a convenção proíba a locação por curta temporada. Só faz sentido contratar "
     "onde ela permite, ou onde a operação é hoteleira desde o projeto.", ""),
    ("O rosto do hóspede é dado sensível",
     "A liberação facial vale para a estadia. O texto de consentimento e a "
     "regra de retenção da foto você valida com o jurídico do condomínio antes de operar.", ""),
    ("O acerto é evidência, não parecer",
     "O relatório mostra a conta aberta que sustenta o PIX ao proprietário. Ele não substitui a "
     "orientação do contador sobre o tratamento do repasse.", ""),
]

TILES = [
    ("Preço por tipo",      "Tarifa base, temporada, fim de semana e estadia mínima.",     "terra",    ""),
    ("Reserva no balcão",   "Orçamento congelado e unidade atribuída na confirmação.",    "terra",    ""),
    ("Site de reservas",    "Faixa de noites, ficha por tipo e pedido em três passos.",   "terra",    "piloto"),
    ("Acesso por estadia",  "Facial na entrada do prédio; senha da fechadura ou chave no quarto.", "petroleo", ""),
    ("Limpeza no checkout", "Tarefa, checklist com foto e vistoria à distância.",         "ambar",    ""),
    ("Quadro e mapa",       "Ocupação, estado das unidades e reservas no mesmo lugar.",   "petroleo", ""),
    ("Acerto com o dono",   "Bruto, limpeza, retenção e líquido, com PDF e chave PIX.",   "ambar",    "piloto"),
    ("Voucher",             "O papel da estadia com os dados da reserva.",                "petroleo", ""),
    ("Permissões separadas","A recepção opera, quem define o preço é outro papel.",       "terra",    ""),
]

CTA = ("Vamos ver o seu calendário no sistema.",
       "Conte quantas unidades você opera e como as reservas chegam hoje. A gente mostra o que já "
       "roda — e o que ainda não roda.")
