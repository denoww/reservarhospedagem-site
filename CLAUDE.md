# reservarhospedagem-site — playbook

Site institucional do **reservarhospedagem** (sistema para condomínios que operam Airbnb,
hotéis e pousadas). Estático, sem build. **GitHub Pages** em `https://www.reservarhospedagem.app`.
Molde: `acompanhaobra-site`. Marca no ERP: `Institucional::Marcas` (slug `reservarhospedagem`).

## Nome

**O nome é o que o produto faz** (regra da casa, `ROADMAP_multi_produto.md` §7 Passo −1).
⚠️ "reservar hospedagem" é a ação do *hóspede*; a copy fala sempre ao **gestor** ("receba
reservas no seu canal direto"). Medir no Search Console quais consultas chegam.

## Deploy

`git push` no `main`. Conferir: `diff <(curl -s https://www.reservarhospedagem.app/index.html) index.html`.
⚠️ `.app` tem HSTS preload: sem certificado o navegador recusa. Pages `errored` não emite cert
(`gh api repos/denoww/reservarhospedagem-site/pages`).

## A regra que manda em tudo: só o que roda

Fonte da verdade do que pode ser prometido: `app/services/hospedagem/ROADMAP_site_reservas_hospedagem.md`
no repo do ERP. Em produção: Ondas 0–2 (acomodações, tarifas, reserva no balcão, acerto com
proprietário, site de reservas SSR) + operação (credencial facial por estadia, quadro, limpeza).

⛔ **NUNCA prometer:** sincronização com Airbnb/Booking/iCal (Onda 3) · channel manager (3.5) ·
pagamento online no site (Onda 4) · avaliações/fidelidade (5) · marketplace (6). A copy
honesta NEGA ("ainda não sincroniza"). Não escrever "ninguém tem" (a HMAX demonstra reserva→porta).
Concorrente pelo nome e preço: não (preço ainda a definir). O guard `.github/scripts/seo.py` reprova.

## Estrutura

`index.html` (CSS + HTML + JS num arquivo, com a **demo viva** da faixa de noites), `entrar.html`
(ponte pro login), `privacidade.html`, `404.html`, `assets/`, `tools/gen_assets.py` (ícones e og.jpg,
paramétrico). Contato e login: dotfiles `.whatsapp` e `.login` (fonte única; o `guarda.yml` confere).

## Pendências conhecidas

- Livreto (4b) existe. Fotos (4c) no ar desde 02/10/2026: 6 vagas geradas no **Bedrock us-west-2** (Stability Ultra/Core,
  `tools/gen_fotos.py`, ~US$ 1,32) e julgadas em `fotos/JULGAMENTO.md`. OpenAI e Gemini estavam sem crédito/cota; Nova
  Canvas está LEGACY e Titan morreu. Pessoas brancas de aparência europeia por pedido do Rodrigo. Pendente: o livreto
  (`build.py` `foto()`) ainda não usa as fotos, e o `og.jpg` segue o paramétrico.
- Blog (`blog.reservarhospedagem.app`) depende da classe em `Auto::Marcas` e do cert no ALB.
- Search Console: propriedade de domínio + sitemap.
