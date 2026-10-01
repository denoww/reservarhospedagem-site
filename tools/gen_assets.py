#!/usr/bin/env python3
"""Gera os ícones e o og.jpg do reservarhospedagem (desenho paramétrico, Pillow).

Símbolo: calendário com a noite marcada e um visto — a "faixa de noites" do produto.
Tile teal #0F766E com gradiente vertical, símbolo branco. Roda na máquina do dev
(`tools/` não é publicado pelo Pages — ver _config.yml).
"""
from PIL import Image, ImageDraw, ImageFont
import os
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = os.path.join(R, 'assets')
TEAL, TEAL_ESC, CLARO = (15, 118, 110), (17, 94, 89), (45, 212, 191)
SS = 8

def tile(px):
    n = px * SS
    im = Image.new('RGBA', (n, n), (0, 0, 0, 0))
    g = Image.new('RGBA', (n, n))
    d = ImageDraw.Draw(g)
    for y in range(n):
        t = y / n
        d.line([(0, y), (n, y)], fill=tuple(int(TEAL[i] + (TEAL_ESC[i] - TEAL[i]) * t) for i in range(3)) + (255,))
    m = Image.new('L', (n, n), 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, n - 1, n - 1], radius=int(n * .22), fill=255)
    im.paste(g, (0, 0), m)
    d = ImageDraw.Draw(im)
    W = (255, 255, 255, 255)
    # calendário
    x0, y0, x1, y1 = [int(n * v) for v in (.22, .27, .78, .76)]
    w = max(2, int(n * .05))
    d.rounded_rectangle([x0, y0, x1, y1], radius=int(n * .06), outline=W, width=w)
    d.rectangle([x0, y0, x1, y0 + int(n * .12)], fill=W)
    for cx in (.36, .64):
        d.rounded_rectangle([int(n * cx) - w, int(n * .20), int(n * cx) + w, int(n * .33)], radius=w, fill=W)
    # visto
    pts = [(.36, .56), (.46, .66), (.65, .45)]
    d.line([(int(n * a), int(n * b)) for a, b in pts], fill=W, width=int(n * .06), joint='curve')
    return im.resize((px, px), Image.LANCZOS)

for nome, px in (('brand-mark.png', 128), ('favicon-32.png', 32), ('apple-touch-icon.png', 180)):
    tile(px).save(os.path.join(A, nome))

# og.jpg 1200x630
W_, H_ = 1200, 630
og = Image.new('RGB', (W_, H_))
d = ImageDraw.Draw(og)
for y in range(H_):
    t = y / H_
    d.line([(0, y), (W_, y)], fill=tuple(int(TEAL[i] + (TEAL_ESC[i] - TEAL[i]) * t) for i in range(3)))
def fonte(tam, bold=True):
    for p in ('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf' if bold else '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
              '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf'):
        if os.path.exists(p):
            return ImageFont.truetype(p, tam)
    return ImageFont.load_default()
og.paste(tile(120), (80, 80), tile(120))
d.text((220, 105), 'reservarhospedagem', font=fonte(54), fill='white')
d.text((220 + d.textlength('reservarhospedagem', font=fonte(54)), 105), '.app', font=fonte(54), fill=CLARO)
d.text((80, 300), 'Receba reservas', font=fonte(86), fill='white')
d.text((80, 405), 'no seu canal direto', font=fonte(86), fill='white')
d.text((80, 540), 'Sistema para condomínios com Airbnb, hotéis e pousadas', font=fonte(30, False), fill=(204, 251, 241))
og.save(os.path.join(A, 'og.jpg'), quality=88, optimize=True, progressive=True)
print('ok')
