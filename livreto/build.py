#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gera o livreto do reservarhospedagem → livreto/index.html (rota /livreto/).

    python3 livreto/build.py

Molde: livreto/ do acompanhaobra-site (ver `livreto/CLAUDE.md` daqui e de lá).
  - Edita-se `content.py` (95% das mudanças) ou este arquivo; NUNCA o HTML gerado.
  - O PDF é espelho automático: o CI (`livreto.yml`) gera por Chromium, mede página em
    branco e commita. Não rode build_pdf.sh na mão para publicar.

PEGADINHAS DO PRINT (quebram em silêncio — ver o CSS, bloco @media print):
  - `.rev{opacity:1}` — senão o PDF sai EM BRANCO.
  - `print-color-adjust:exact` — senão hero/CTA saem sem cor.
  - `break-inside:avoid` só nas unidades atômicas, nunca por capítulo.
  - `@page{size:A4}` — senão o Chrome imprime em Letter.
"""
import pathlib, importlib.util, datetime, hashlib

ROOT = pathlib.Path(__file__).resolve().parent
REPO = ROOT.parent
OUT  = REPO / "livreto" / "index.html"

sp = importlib.util.spec_from_file_location("content", str(ROOT / "content.py"))
C = importlib.util.module_from_spec(sp); sp.loader.exec_module(C)

WA = C.WA + C.WA_TXT

# --------------------------------------------------------------------- cenas
# Line-art dos storyboards (viewBox 56x44). `stroke="currentColor"` + `fill="none"` vêm do
# `scene()` no <g> — NÃO usar classe utilitária aqui (no molde `.s`/`.w` zeravam o traço).
# As chaves casam 1:1 com as cenas citadas em `content.py > BOARDS`.
SCENES = {
 "calendario": '<rect x="12" y="11" width="32" height="26" rx="3"/><path d="M12 19h32M20 8v6M36 8v6"/>'
               '<path d="M19 26h4M26 26h4M33 26h4M19 31h4M26 31h4"/>',
 "balcao":     '<path d="M10 33h36"/><path d="M14 33V22h28v11"/><circle cx="28" cy="14" r="4"/>'
               '<path d="M23 22c0-3 2-4 5-4s5 1 5 4"/>',
 "face":       '<path d="M14 18v-5a3 3 0 0 1 3-3h5M34 10h5a3 3 0 0 1 3 3v5M42 30v5a3 3 0 0 1-3 3h-5M22 38h-5a3 3 0 0 1-3-3v-5"/>'
               '<circle cx="28" cy="22" r="6"/><path d="M25.5 23.5c1.4 1.6 3.6 1.6 5 0"/>',
 "porta":      '<rect x="16" y="8" width="24" height="30" rx="2"/><path d="M16 38h24"/>'
               '<circle cx="34" cy="24" r="1.6"/><path d="M12 38h32"/>',
 "vassoura":   '<path d="M36 8L24 26"/><path d="M20 26l10 6-4 8-12-4z"/><path d="M18 31l6 3M16 35l6 3"/>',
 "chave":      '<circle cx="19" cy="22" r="7"/><circle cx="19" cy="22" r="2"/><path d="M26 22h18M38 22v6M43 22v4"/>',
 "lista":      '<rect x="14" y="8" width="28" height="30" rx="2"/><path d="M20 16h16M20 22h16M20 28h10"/>',
 "percent":    '<circle cx="19" cy="15" r="4"/><circle cx="37" cy="29" r="4"/><path d="M38 12L18 32"/>',
 "moeda":      '<circle cx="28" cy="22" r="13"/><path d="M33 17c-1-2-3-3-5-3-3 0-5 1.600-5 4 0 6 10 3 10 9 0 2.500-2 4-5 4-2 0-4-1-5-3"/><path d="M28 11v3M28 32v3"/>',
 "pdf":        '<path d="M16 7h17l8 8v22H16z"/><path d="M33 7v8h8"/><path d="M21 24h14M21 29h14"/>',
 "foto":       '<rect x="11" y="15" width="34" height="22" rx="3"/><circle cx="28" cy="26" r="7"/>'
               '<path d="M22 15l2.500-4h7l2.500 4"/>',
 "lupa":       '<circle cx="25" cy="21" r="10"/><path d="M33 29l9 9"/><path d="M21 21l3 3 5-6"/>',
}
def scene(n):
    return ('<svg class="scene" viewBox="0 0 56 44" aria-hidden="true">'
            f'<g fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" '
            f'stroke-linejoin="round">{SCENES[n]}</g></svg>')

# ---------------------------------------------------------------- componentes
_CHAP = [0]
def chapter(cid, eyebrow, h2, lead, *blocks):
    bg = "nevoa" if _CHAP[0] % 2 else ""   # alterna sozinho — não passe bg
    _CHAP[0] += 1
    return f'''<section class="cap {bg}" id="{cid}" aria-label="{eyebrow}">
  <div class="cap-in">
    <div class="cap-head rev"><span class="eyebrow">{eyebrow}</span><h2>{h2}</h2>
      {f'<p class="lead">{lead}</p>' if lead else ''}</div>
    {"".join(blocks)}
  </div>
</section>'''

def tag(t):
    return f'<span class="tg">{t}</span>' if t else ''

def cards(items, cor):
    cs = "".join(f'<article class="fc"><span class="fc-mk"></span><h3>{t}{tag(g)}</h3><p>{d}</p></article>'
                 for t, d, g in items)
    return f'<div class="fgrid c-{cor} rev">{cs}</div>'

def board(key):
    cor, titulo, panels = C.BOARDS[key]
    cells = []
    for i, (sc, h, cap) in enumerate(panels):
        cells.append(f'<li class="bp"><span class="bp-n">{i+1}</span>'
                     f'<span class="bp-art">{scene(sc)}</span><b>{h}</b><i>{cap}</i></li>')
        if i < len(panels) - 1:
            cells.append('<li class="bp-arr" aria-hidden="true">→</li>')
    return (f'<figure class="board c-{cor} rev"><figcaption class="board-cap">'
            f'<span class="eyebrow">Como funciona</span><b>{titulo}</b></figcaption>'
            f'<ol class="board-strip">{"".join(cells)}</ol></figure>')

def foto(slug, alt, extra=""):
    return (f'<figure class="shot{extra}"><img src="/assets/{slug}.jpg" alt="{alt}" '
            f'loading="lazy" decoding="async"></figure>')

def mrow(media, h, p, flip=False):
    return (f'<div class="mrow{" flip" if flip else ""} rev"><div class="m-media">{media}</div>'
            f'<div class="m-copy"><h3>{h}</h3><p>{p}</p></div></div>')

def lista(items):
    return ('<ul class="check rev">' +
            "".join(f'<li><span class="ck"></span>{t}</li>' for t in items) + '</ul>')

# ---------------------------------------------------------------------- CSS
CSS = """
:root{
  --branco:#fff;--nevoa:#f5f5f7;--preto:#000;
  --tinta:#1d1d1f;--tinta-2:#6e6e73;--claro:#f5f5f7;--claro-2:#a1a1a6;
  --terra:#0F766E;--terra-vivo:#2DD4BF;--terra-esc:#115E59;--terra-leve:#E0F2F1;
  --petroleo:#1E3A5F;--ciano:#0891B2;--ambar:#B45309;
  --linha:rgba(0,0,0,.12);--maxw:1120px;
  --sec:var(--terra);
  --ease:cubic-bezier(.45,0,.55,1);
}
.c-terra{--sec:#0F766E;--soft:#E0F2F1}
.c-petroleo{--sec:#1E3A5F;--soft:#E6EDF5}
.c-ciano{--sec:#0891B2;--soft:#E0F3F7}
.c-ambar{--sec:#B45309;--soft:#FBF0E2}
*{box-sizing:border-box}
html{scroll-behavior:smooth;-webkit-text-size-adjust:100%}
body{margin:0;background:var(--branco);color:var(--tinta);
  font-family:-apple-system,BlinkMacSystemFont,'SF Pro Text','Inter',system-ui,sans-serif;
  font-size:17px;line-height:1.4705882353;letter-spacing:-.022em;-webkit-font-smoothing:antialiased}
h1,h2,h3{margin:0;font-weight:600;line-height:1.06;letter-spacing:-.015em;text-wrap:balance}
p{margin:0}ul,ol{margin:0;padding:0;list-style:none}
a{color:var(--terra);text-decoration:none}
img{display:block;max-width:100%}
:focus-visible{outline:3px solid var(--terra-vivo);outline-offset:3px;border-radius:6px}
.eyebrow{display:block;font-size:21px;font-weight:600;letter-spacing:.011em;color:var(--sec);margin-bottom:8px}
.lead{font-size:21px;line-height:1.381;letter-spacing:.011em;color:var(--tinta-2);margin-top:14px}

.nav{position:sticky;top:0;z-index:50;height:52px;display:flex;align-items:center;justify-content:space-between;
  padding:0 clamp(20px,4vw,40px);background:rgba(255,255,255,.72);
  backdrop-filter:saturate(180%) blur(20px);-webkit-backdrop-filter:saturate(180%) blur(20px);
  border-bottom:1px solid rgba(0,0,0,.08)}
.nav .brand{display:flex;align-items:center;gap:8px;font-weight:600;font-size:17px;color:var(--tinta);letter-spacing:-.02em}
.nav .brand img{width:24px;height:24px;border-radius:6px}
.nav .brand .tld{color:var(--terra)}
.nav-r{display:flex;align-items:center;gap:clamp(14px,3vw,26px);font-size:13px}
/* os <a> vivem DENTRO de .nav-links — sem display:flex aqui eles saem colados
   ("A batidaA prova"), porque o gap do .nav-r só separa os filhos diretos. */
.nav-links{display:inline-flex;align-items:center;gap:clamp(14px,2.2vw,24px)}
.nav-r a{color:var(--tinta);opacity:.85}
.nav-r a:hover{opacity:1;color:var(--terra)}
.nav-cta{background:var(--terra);color:#fff!important;padding:6px 14px;border-radius:980px;font-weight:500}
@media(max-width:760px){.nav-links{display:none}.nav{padding:0 16px}.nav .brand{font-size:14px;gap:6px;white-space:nowrap}.nav .brand .tld{display:none}.nav-r{gap:8px}.nav-cta{white-space:nowrap;padding:6px 12px;font-size:12px}.nav-cta .mais{display:none}}

.btn{display:inline-flex;align-items:center;justify-content:center;gap:8px;background:var(--terra);color:#fff;
  padding:12px 22px;border-radius:980px;font-weight:400;font-size:17px;letter-spacing:-.022em;
  transition:background-color .1s linear}
.btn:hover{background:var(--terra-esc)}
.btn-branco{background:#fff;color:var(--tinta)}
.btns{display:flex;flex-wrap:wrap;gap:12px;justify-content:center;margin-top:32px}

/* hero */
.hero{background:var(--preto);color:var(--claro);text-align:center;padding:clamp(64px,9vh,104px) 24px 0;overflow:hidden;
  background-image:radial-gradient(900px 500px at 50% -10%,rgba(15,118,110,.55),transparent 62%)}
.hero .eyebrow{color:var(--terra-vivo)}
.hero h1{font-size:clamp(40px,4.4vw+14px,76px);color:#fff;max-width:16ch;margin:0 auto}
.hero .sub{margin:22px auto 0;max-width:56ch;font-size:21px;line-height:1.4;color:var(--claro-2);letter-spacing:.011em}
.hero-stage{margin:56px auto 0;max-width:900px}
/* banner: a foto sobe do hero e é cortada pelo fim da seção (o corte é de propósito).
   Sem aspect-ratio ela entra inteira e o corte cai em lugar aleatório. */
.hero-stage img{width:100%;aspect-ratio:16/8;object-fit:cover;object-position:60% 16%;
  border-radius:24px 24px 0 0;box-shadow:0 -10px 60px rgba(15,118,110,.3)}

.credo{max-width:960px;margin:0 auto;padding:clamp(80px,10vw,130px) 24px;text-align:center}
.credo h2{font-size:clamp(30px,3.4vw+10px,52px);letter-spacing:-.02em}
.credo .g{color:var(--terra)}

/* capítulos */
.cap{padding:clamp(72px,9vw,120px) 0}
.cap.nevoa{background:var(--nevoa)}
.cap-in{max-width:var(--maxw);margin:0 auto;padding:0 24px}
.cap-head{max-width:760px}
.cap-head h2{font-size:clamp(30px,2.4vw+14px,48px);letter-spacing:-.01em;margin-top:2px}

.fgrid{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:20px;margin-top:44px}
.fc{background:var(--branco);border:1px solid var(--linha);border-radius:20px;padding:26px 24px;break-inside:avoid}
.cap.nevoa .fc{background:#fff;border-color:rgba(0,0,0,.06)}
.fc-mk{display:block;width:26px;height:3px;border-radius:3px;background:var(--sec);margin-bottom:16px}
.fc h3{font-size:20px;letter-spacing:-.01em}
.fc p{margin-top:8px;color:var(--tinta-2);font-size:16px;line-height:1.5}
.tg{display:inline-block;margin-left:8px;font-size:11px;font-weight:700;letter-spacing:.05em;text-transform:uppercase;
  color:var(--sec);background:var(--soft);padding:3px 8px;border-radius:980px;vertical-align:middle}

/* storyboard */
.board{margin:48px 0 0;padding:30px;border-radius:24px;background:var(--soft);break-inside:avoid}
.board-cap{margin-bottom:22px}
.board-cap b{display:block;font-size:22px;font-weight:600;letter-spacing:-.01em}
.board-strip{display:flex;align-items:stretch;gap:10px;flex-wrap:wrap}
.bp{flex:1 1 180px;background:#fff;border-radius:16px;padding:20px 18px;position:relative;break-inside:avoid}
.bp-n{position:absolute;top:14px;right:16px;font-size:12px;font-weight:700;color:var(--sec)}
.bp-art{display:block;color:var(--sec)}
.scene{width:56px;height:44px}
.bp b{display:block;margin-top:12px;font-size:17px;font-weight:600;letter-spacing:-.01em}
.bp i{display:block;margin-top:6px;font-style:normal;font-size:14.5px;line-height:1.45;color:var(--tinta-2)}
.bp-arr{display:flex;align-items:center;color:var(--sec);font-size:20px;opacity:.55}
@media(max-width:860px){.bp-arr{display:none}}

/* media row */
.mrow{display:grid;grid-template-columns:1.05fr .95fr;gap:44px;align-items:center;margin-top:48px}
.mrow.flip .m-media{order:2}
@media(max-width:860px){.mrow{grid-template-columns:1fr}.mrow.flip .m-media{order:0}}
.m-copy h3{font-size:26px;letter-spacing:-.012em}
.m-copy p{margin-top:12px;color:var(--tinta-2);font-size:17px;line-height:1.5}
.shot img{width:100%;border-radius:20px}

/* checklist */
.check{margin-top:36px;display:grid;gap:14px}
.check li{display:flex;gap:12px;align-items:flex-start;font-size:17px;line-height:1.45;break-inside:avoid}
.ck{flex:0 0 auto;width:20px;height:20px;margin-top:2px;border-radius:50%;background:var(--terra-leve);position:relative}
.ck::after{content:"";position:absolute;left:6px;top:5px;width:5px;height:9px;border:2px solid var(--terra-esc);
  border-top:0;border-left:0;transform:rotate(42deg)}

/* setores */
.setores{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-top:44px}
@media(max-width:860px){.setores{grid-template-columns:repeat(2,1fr)}}
.setor{break-inside:avoid}
.setor img{width:100%;aspect-ratio:2/3;object-fit:cover;border-radius:18px}
.setor b{display:block;margin-top:12px;font-size:18px;font-weight:600;letter-spacing:-.01em}
.setor span{display:block;margin-top:4px;font-size:14.5px;line-height:1.45;color:var(--tinta-2)}

/* preço */
.planos{display:grid;grid-template-columns:repeat(3,1fr);gap:20px;margin-top:44px}
@media(max-width:860px){.planos{grid-template-columns:1fr}}
.plano{border:1px solid var(--linha);border-radius:24px;padding:30px 26px;background:#fff;break-inside:avoid}
.plano .nome{font-size:13px;font-weight:600;letter-spacing:.06em;text-transform:uppercase;color:var(--tinta-2)}
.plano .v{margin-top:14px;font-size:46px;font-weight:600;letter-spacing:-.03em;line-height:1}
.plano .u{margin-top:6px;font-size:14px;color:var(--tinta-2)}
.plano p{margin-top:14px;font-size:15.5px;line-height:1.5;color:var(--tinta-2)}
.plano.hi{background:var(--preto);border-color:var(--preto);color:var(--claro)}
.plano.hi .nome{color:var(--terra-vivo)}
.plano.hi .v{color:#fff}
.plano.hi .u,.plano.hi p{color:var(--claro-2)}
.naos{display:grid;grid-template-columns:repeat(3,1fr);gap:20px;margin-top:20px}
@media(max-width:860px){.naos{grid-template-columns:1fr}}
.nao{border-radius:20px;padding:24px;background:#fff;border:1px solid var(--linha);break-inside:avoid}
.nao h4{margin:0;font-size:18px;font-weight:600;letter-spacing:-.01em}
.nao p{margin-top:8px;font-size:15.5px;line-height:1.5;color:var(--tinta-2)}

/* lineup */
.lineup{background:var(--preto);color:var(--claro);padding:clamp(80px,10vw,130px) 0}
.lineup-in{max-width:var(--maxw);margin:0 auto;padding:0 24px}
.lineup h2{font-size:clamp(30px,2.4vw+14px,48px);color:#fff}
.lineup .lead{color:var(--claro-2)}
.tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:16px;margin-top:44px}
.tile{background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.12);border-radius:20px;padding:24px;break-inside:avoid}
.tile h3{font-size:18px;color:#fff}
.tile p{margin-top:8px;font-size:15px;line-height:1.5;color:var(--claro-2)}
.tile-mk{display:block;width:26px;height:3px;border-radius:3px;background:var(--sec);margin-bottom:14px}

/* cta / download / rodapé */
.cta{text-align:center;padding:clamp(88px,11vw,140px) 24px;background:
  radial-gradient(1100px 560px at 50% 0%,rgba(15,118,110,.55),transparent 65%),#0b0a0e;color:var(--claro)}
.cta h2{font-size:clamp(30px,3vw+12px,52px);color:#fff;max-width:18ch;margin:0 auto}
.cta p{margin:20px auto 0;max-width:52ch;font-size:19px;line-height:1.5;color:var(--claro-2)}
.dl{text-align:center;padding:clamp(64px,8vw,96px) 24px;background:var(--nevoa)}
.dl h2{font-size:30px}
.dl p{margin-top:12px;color:var(--tinta-2)}
.foot{border-top:1px solid var(--linha);padding:36px 24px;background:var(--nevoa)}
.foot-in{max-width:var(--maxw);margin:0 auto;display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap;
  color:var(--tinta-2);font-size:13px}

/* reveal */
.rev{opacity:0;transform:translateY(30px);transition:opacity .9s var(--ease),transform .9s var(--ease)}
.rev.vis{opacity:1;transform:none}
@media(prefers-reduced-motion:reduce){.rev{opacity:1;transform:none}html{scroll-behavior:auto}}


/* hero: faixa de noites (ilustrativa, estática) */
.stage{margin:56px auto 0;max-width:760px;padding:26px 26px 30px;border-radius:24px 24px 0 0;
  background:rgba(255,255,255,.07);border:1px solid rgba(255,255,255,.14);border-bottom:0;text-align:left}
.stage-t{font-size:13px;letter-spacing:.06em;text-transform:uppercase;color:var(--terra-vivo);font-weight:600}
.noites{display:grid;grid-template-columns:repeat(7,1fr);gap:8px;margin-top:16px}
.noite{border-radius:12px;padding:12px 6px;text-align:center;background:rgba(255,255,255,.08);color:var(--claro-2);font-size:13px}
.noite b{display:block;font-size:20px;color:#fff;font-weight:600}
.noite.on{background:var(--terra);color:#fff}
.noite.on b{color:#fff}
.stage-l{margin-top:16px;display:flex;flex-wrap:wrap;gap:8px 22px;font-size:14px;color:var(--claro-2)}
.stage-l span::before{content:"";display:inline-block;width:8px;height:8px;border-radius:50%;background:var(--terra-vivo);margin-right:8px}
.stage-i{margin-top:14px;font-size:12px;color:var(--claro-2);opacity:.8}

/* ======================= IMPRESSÃO / PDF =======================
   As três travas do playbook. Mexer aqui quebra o PDF em silêncio. */
@media print{
  /* 1. sem isto o PDF sai EM BRANCO (o reveal nunca dispara sem scroll) */
  .rev{opacity:1!important;transform:none!important}
  /* 2. sem isto hero/CTA/fotos saem sem cor */
  *{-webkit-print-color-adjust:exact!important;print-color-adjust:exact!important}
  /* 3. só nas unidades atômicas — NUNCA por capítulo (gera página quase vazia) */
  .fc,.bp,.plano,.nao,.tile,.setor,.board,.check li,.stage{break-inside:avoid}
  .nav,.dl,.btns{display:none!important}
  .cap{padding:28px 0}
  .hero{padding-top:36px}
  .credo{padding:44px 24px}
  body{font-size:11.5pt}
  a{color:inherit;text-decoration:none}
  /* sem isto o Chrome imprime em Letter (padrão americano) — no Brasil é A4 */
  @page{size:A4;margin:14mm}
}
"""

SCRIPT = """<script>
(function(){
  if(matchMedia("(prefers-reduced-motion: reduce)").matches){
    document.querySelectorAll(".rev").forEach(function(e){e.classList.add("vis")});return;}
  var io=new IntersectionObserver(function(es){es.forEach(function(e){
    if(e.isIntersecting){e.target.classList.add("vis");io.unobserve(e.target)}})},
    {threshold:0,rootMargin:"0px 0px -12% 0px"});
  document.querySelectorAll(".rev").forEach(function(e){io.observe(e)});
})();
</script>"""

# --------------------------------------------------------------------- montagem
def build():
    _CHAP[0] = 0
    wa_svg = ('<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" style="width:18px;height:18px">'
              '<path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm0 18.2c-1.6 0-3.1-.4-4.4-1.2'
              'l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2Z"/></svg>')

    nav = f'''<nav class="nav">
  <a class="brand" href="/"><img src="/assets/brand-mark.png" width="24" height="24" alt="">
    <span>reservarhospedagem<span class="tld">.app</span></span></a>
  <span class="nav-r"><span class="nav-links">
    <a href="#valor">Quanto custa</a><a href="#reserva">Reserva</a>
    <a href="#acerto">Acerto</a><a href="#limites">O que não faz</a></span>
  <a class="nav-cta" href="{WA}">Falar<span class="mais"> no</span> WhatsApp</a></span>
</nav>'''

    dias = [("seg", "12"), ("ter", "13"), ("qua", "14"), ("qui", "15"), ("sex", "16"), ("sáb", "17"), ("dom", "18")]
    noites = "".join(f'<div class="noite{" on" if 1 <= i <= 3 else ""}">{d}<b>{n}</b></div>'
                     for i, (d, n) in enumerate(dias))
    hero = f'''<header class="hero">
  <span class="eyebrow">{C.HERO["eyebrow"]}</span>
  <h1>{C.HERO["h1"]}</h1>
  <p class="sub">{C.HERO["sub"]}</p>
  <div class="btns"><a class="btn btn-branco" href="{WA}">{wa_svg} Falar no WhatsApp</a></div>
  <div class="stage rev">
    <div class="stage-t">Faixa de noites</div>
    <div class="noites">{noites}</div>
    <div class="stage-l"><span>3 noites escolhidas</span><span>unidade atribuída na confirmação</span>
      <span>acesso válido só na estadia</span></div>
    <div class="stage-i">Exemplo ilustrativo, sem dados reais.</div>
  </div>
</header>'''

    credo = f'<section class="credo rev"><h2>{C.CREDO}</h2></section>'

    cap_preco = chapter("preco-tarifa", "A tarifa", "Cada noite com a tarifa certa.",
        "Você vende por tipo de acomodação. A tarifa vigente de maior prioridade vence em cada noite, "
        "e o total chega decomposto — diárias, adicionais e limpeza —, nunca só um número.",
        cards(C.PRECO_CARDS, "terra"))

    cap_reserva = chapter("reserva", "A reserva", "Do pedido ao hóspede dentro do apartamento.",
        "A reserva é o contrato comercial; a liberação de acesso nasce dela, na confirmação. É o que "
        "liga quem vende a quem opera a portaria, sem digitar a estadia duas vezes.",
        board("reserva"), cards(C.RESERVA_CARDS, "terra"))

    cap_site = chapter("site", "O site", "Um canal direto, e que o Google consegue ler.",
        "O site de reservas é uma página do seu condomínio. Ele mostra o preço e a disponibilidade "
        "reais e fecha o pedido como pré-reserva, que a recepção confirma.",
        cards(C.SITE_CARDS, "petroleo"))

    cap_estadia = chapter("estadia", "A estadia", "O hóspede entra com o rosto.",
        "Onde o condomínio tem controle de acesso facial, a credencial do hóspede vale entre o check-in "
        "e o check-out, no mesmo sistema da portaria.",
        cards(C.ESTADIA_CARDS, "petroleo"))

    cap_limpeza = chapter("limpeza", "A limpeza", "O checkout abre a tarefa.",
        "A camareira recebe a tarefa, roda o checklist com foto, e o gestor vistoria à distância. A "
        "unidade só volta para a venda quando está pronta.",
        board("limpeza"), cards(C.LIMPEZA_CARDS, "ambar"))

    cap_acerto = chapter("acerto", "O acerto", "Quanto entrou, quanto fica, quanto vai pra quem.",
        "O condomínio recebe e depois repassa ao proprietário por PIX. O relatório de acerto é a conta "
        "aberta que sustenta esse repasse.",
        board("acerto"), cards(C.ACERTO_CARDS, "ambar"))

    cap_quadro = chapter("quadro", "O quadro", "A operação do dia numa tela só.",
        "Reservas, estado das unidades e ocupação no mesmo lugar, para quem gerencia ver o dia de longe.",
        cards(C.QUADRO_CARDS, "terra"))

    setores = "".join(f'<div class="nao rev"><h4>{r}</h4><p>{d}</p></div>' for r, d in C.SETORES)
    cap_quem = chapter("quem", "Para quem é", "Se você opera hospedagem, serve.",
        "Condomínio, flat, pousada pequena e clube com chalés. O alvo é quem já tem a unidade e a "
        "portaria — e quer o canal direto e o acerto no mesmo sistema.",
        f'<div class="naos rev" style="grid-template-columns:repeat(auto-fit,minmax(240px,1fr))">{setores}</div>')

    cap_dor = chapter("dor", "O que dói hoje", "Se isso é a sua semana, é com você que a gente fala.",
        "Situações do dia a dia de quem hospeda, e o que o sistema faz com cada uma.",
        lista(C.DORES))

    naos = "".join(f'<div class="nao"><h4>{t}</h4><p>{d}</p></div>' for t, d in C.PRECO_NOTA)
    cap_valor = chapter("valor", "Quanto custa", "Você paga por unidade ativa. As duas primeiras são grátis.",
        "Cobrança por unidade ativa, por mês, com preço que cai nas faixas maiores. Sem taxa de "
        "implantação e sem fidelidade.",
        f'<div class="naos rev">{naos}</div>')

    cap_limites = chapter("limites", "Honestidade", "O que o reservarhospedagem não faz.",
        "Um livreto que só lista virtude não ajuda ninguém a decidir. Isto aqui é o que ele "
        "<b>não</b> resolve — para você não descobrir depois de assinar.",
        cards(C.NAO_FAZ, "ambar"))

    cap_lei = chapter("lei", "Antes de operar", "Três coisas que não são de software.",
        "O sistema entrega a operação. Convenção, dado sensível e tributação do repasse têm dono "
        "fora dele.",
        cards(C.LEI, "petroleo"))

    tiles = "".join(f'<article class="tile c-{c}"><span class="tile-mk"></span>'
                    f'<h3>{n}{tag(g)}</h3><p>{d}</p></article>' for n, d, c, g in C.TILES)
    lineup = f'''<section class="lineup" id="modulos">
  <div class="lineup-in">
    <h2 class="rev">Tudo o que ele faz.</h2>
    <p class="lead rev">O que roda hoje, com o selo de piloto onde a operação ainda é de um cliente só.</p>
    <div class="tiles rev">{tiles}</div>
  </div>
</section>'''

    h2, p = C.CTA
    cta = f'''<section class="cta">
  <h2 class="rev">{h2}</h2>
  <p class="rev">{p}</p>
  <div class="btns rev"><a class="btn btn-branco" href="{WA}">{wa_svg} Falar no WhatsApp</a></div>
</section>'''

    dl = '''<section class="dl">
  <h2>Leve o livreto com você.</h2>
  <p>Baixe o PDF para apresentar offline ou mandar por e-mail.</p>
  <div class="btns"><a class="btn" href="/livreto.pdf" download="livreto-reservarhospedagem.pdf">
    Baixar o livreto (PDF)</a></div>
</section>'''

    body = "\n".join([nav, hero, credo, cap_dor, cap_valor, cap_preco, cap_reserva, cap_site, cap_estadia, cap_limpeza,
                      cap_acerto, cap_quadro, cap_quem, cap_limites, cap_lei,
                      lineup, cta, dl])

    hoje = datetime.date.today().strftime("%d/%m/%Y")
    sha = hashlib.sha1(body.encode()).hexdigest()[:7]
    foot = (f'<footer class="foot"><div class="foot-in">'
            f'<span>reservarhospedagem · parte da família Seu Condomínio · '
            f'<a href="{C.SITE}/privacidade">Privacidade</a></span>'
            f'<span>Livreto v{hoje} · {sha}</span></div></footer>')

    desc = ("Livreto do reservarhospedagem: preço por tipo de acomodação, site de reservas, acerto com "
            "o proprietário, credencial facial por estadia e limpeza no checkout, para condomínios com "
            "temporada, flats, pousadas e hotéis pequenos.")
    url = f"{C.SITE}/livreto/"
    head = f'''<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Livreto do reservarhospedagem — reserva direta, acerto e limpeza</title>
<meta name="description" content="{desc}">
<meta name="robots" content="index,follow,max-image-preview:large">
<link rel="canonical" href="{url}">
<link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon-32.png">
<meta property="og:type" content="website">
<meta property="og:site_name" content="reservarhospedagem">
<meta property="og:locale" content="pt_BR">
<meta property="og:url" content="{url}">
<meta property="og:title" content="Livreto do reservarhospedagem">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{C.SITE}/assets/og.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,400;14..32,500;14..32,600&display=swap" rel="stylesheet">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"SoftwareApplication",
"name":"reservarhospedagem","applicationCategory":"BusinessApplication","operatingSystem":"Web",
"url":"{url}","inLanguage":"pt-BR","description":"{desc}",
"featureList":["Preço por tipo de acomodação com tarifa de temporada e fim de semana",
"Reserva no balcão com orçamento congelado",
"Site de reservas com pedido em três passos",
"Credencial facial válida entre o check-in e o check-out",
"Tarefa de limpeza aberta no checkout, com checklist e foto",
"Acerto com o proprietário por unidade e período, com PDF",
"Quadro de hospedagem com mapa de reservas"]}}</script>
<style>{CSS}</style>
</head>
<body>
'''
    doc = head + body + "\n" + foot + "\n" + SCRIPT + "\n</body>\n</html>\n"
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(doc)
    print(f"[livreto] {OUT} — {len(doc)//1024} KB · v{hoje} · {sha}")

build()
