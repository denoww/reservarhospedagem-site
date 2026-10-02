# Pendências do site — o que só o Rodrigo sabe

Escrito em 02/10/2026, depois da reestruturação da home pelo veredito do juiz (nota 4/10 vendável).
O que está no ar só afirma o que o livreto/roadmap confirma. Cada item abaixo é uma lacuna que o juiz
apontou e que **não foi preenchida de propósito**, para não inventar fato.

## P0 — sem isso o site ainda não fecha contrato sozinho

1. **Piloto: quem é.** Nome (ou ao menos a cidade), quantas unidades e desde quando opera. Hoje a home diz só
   "há um condomínio operando temporada sobre o módulo". ⚠️ Antes de citar, conferir no ERP o que roda de verdade
   no cliente 6296: estadia/porta/limpeza são reais; o **site de reservas do piloto ainda tinha conteúdo de
   demonstração** (preços e fotos inventados, `ROADMAP_site_reservas_hospedagem.md` §resumo).
2. **Depoimento** de 1 frase do síndico/gestor do piloto, com autorização para publicar.
3. **Prazo de implantação.** "Em quanto tempo o site de reservas fica no ar com as minhas acomodações?" Está **fora**
   do FAQ por falta de fonte. Quando souber, entra em "Como começar" e no FAQ.
4. **Equipamento facial: fornecemos ou indicamos?** A home diz que a entrada pelo rosto depende de controle de acesso
   facial no mesmo sistema da portaria. Falta dizer, para a pousada que não é cliente, se vendemos/indicamos o
   equipamento e quanto custa. Falta também confirmar se **o resto funciona sem o equipamento** — a frase atual
   ("as demais peças ... são as que pousada pequena e flat usam") se apoia só no que o FAQ antigo já afirmava.

## P1

5. **LGPD da foto do hóspede:** prazo de apagamento e texto do termo de consentimento. A home usa o texto honesto do
   livreto ("validar com o jurídico do condomínio"); o ideal é trocar por "a foto é apagada em X dias".
6. **Demonstração/teste grátis:** existe demo de 20 minutos? X dias grátis? Hoje o CTA é "ver funcionando no WhatsApp".
7. **Cobrança do preço publicado.** A tabela aprovada em 02/10/2026 está no ar (2 grátis · R$ 4,90 · R$ 2,90 · R$ 1,90,
   por unidade ativa/mês). **A medição de "unidade ativa" e a cobrança ainda não existem no código do ERP**
   (`ROADMAP_site_reservas_hospedagem.md` §9.x) — hoje seria cobrança manual. Decidir se isso muda o texto.
8. **Horário e SLA da resposta no WhatsApp** ("respondemos em até X horas"). A seção final diz só "você fala com uma pessoa".

## P2

9. **Prints reais do sistema** (quadro, PDF do acerto, checklist da camareira) com dados fictícios, no lugar das
   fotos geradas. O síndico quer ver a tela que vai usar.
10. **Preço do channel manager/iCal** quando virarem produto (hoje a home diz, honestamente, que não existem).
11. **Prova com número**, só quando houver número verificado (o guard `seo.py` reprova prova social inventada).
