"""Compõe a foto da seção 'Entrada do prédio sem recepção'.

Cena `entrada_t2` (portaria de prédio, sem aparelho utilizável) + aparelho `terminal_u4` (desenho de terminal
facial atual) + TELA desenhada aqui (vívida, com o retrato `tela_retrato_*`). Tudo local, sem custo de geração.
Parâmetros no topo. Rodar: python3 tools/compor_entrada.py  -> fotos/candidatos/entrada_final2.jpg
"""
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageChops

ESCALA = 0.80                      # pedido do Rodrigo: aparelho 20% menor que a 1ª composição (altura 477 px)
ALTURA_ANTERIOR = 477
CENTRO = (631, 500)               # onde o aparelho fica na cena 896x1088
RETRATO = "fotos/candidatos/tela_retrato_2.jpg"
FONTE = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONTE_L = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

def coefs(dst, src):
    """Coeficientes de Image.PERSPECTIVE (mapeia dst -> src) por eliminação de Gauss, sem numpy."""
    A = []
    for (x, y), (u, v) in zip(dst, src):
        A.append([x, y, 1, 0, 0, 0, -u * x, -u * y, u]); A.append([0, 0, 0, x, y, 1, -v * x, -v * y, v])
    n = 8
    for i in range(n):
        p = max(range(i, n), key=lambda r: abs(A[r][i])); A[i], A[p] = A[p], A[i]
        A[i] = [v / A[i][i] for v in A[i]]
        for r in range(n):
            if r != i: A[r] = [vr - A[r][i] * vi for vr, vi in zip(A[r], A[i])]
    return [A[i][n] for i in range(n)]

def tela_ui(W=524, H=1400):
    """Interface vívida: gradiente violeta→azul, retrato com moldura neon, check verde e texto."""
    fundo = Image.new("RGB", (W, H))
    px = fundo.load()
    for y in range(H):
        t = y / H
        c = (int(88 - 60 * t), int(28 + 40 * t), int(200 - 40 * t)) if t < .55 else (int(60 - 50 * (t - .55) / .45), int(50 + 0 * t), int(170 - 120 * (t - .55) / .45))
        for x in range(W): px[x, y] = c
    glow = Image.new("RGB", (W, H), (0, 0, 0)); g = ImageDraw.Draw(glow)
    g.ellipse((-120, 120, 360, 640), fill=(190, 60, 255)); g.ellipse((200, 520, 700, 1000), fill=(0, 200, 255))
    fundo = ImageChops.screen(fundo, glow.filter(ImageFilter.GaussianBlur(120)).point(lambda v: int(v * .55)))
    d = ImageDraw.Draw(fundo)
    f1, f2, f3 = ImageFont.truetype(FONTE, 70), ImageFont.truetype(FONTE, 54), ImageFont.truetype(FONTE_L, 34)
    d.text((W // 2, 80), "Bem-vindo!", font=f1, fill="white", anchor="mm")
    d.text((W // 2, 150), "Reconhecimento facial", font=f3, fill=(210, 225, 255), anchor="mm")
    # retrato em moldura arredondada com anel neon (ciano→magenta)
    r = Image.open(RETRATO).convert("RGB"); bx, by, bw, bh = 52, 215, 420, 580
    r = r.resize((bw, int(r.height * bw / r.width)), Image.LANCZOS).crop((0, 20, bw, 20 + bh))
    m = Image.new("L", (bw, bh), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, bw - 1, bh - 1), 44, fill=255)
    anel = Image.new("RGB", (W, H), (0, 0, 0)); a = ImageDraw.Draw(anel)
    for i, c in enumerate(((0, 230, 255), (160, 80, 255), (255, 70, 200))):
        a.rounded_rectangle((bx - 14 + i * 3, by - 14 + i * 3, bx + bw + 14 - i * 3, by + bh + 14 - i * 3), 58, outline=c, width=7)
    fundo = ImageChops.screen(fundo, anel.filter(ImageFilter.GaussianBlur(18)))
    fundo = ImageChops.screen(fundo, anel)
    fundo.paste(r, (bx, by), m)
    d = ImageDraw.Draw(fundo)
    for (x, y, dx, dy) in ((bx - 6, by - 6, 1, 1), (bx + bw + 6, by - 6, -1, 1), (bx - 6, by + bh + 6, 1, -1), (bx + bw + 6, by + bh + 6, -1, -1)):
        d.line((x, y, x + 70 * dx, y), fill=(60, 255, 150), width=10); d.line((x, y, x, y + 70 * dy), fill=(60, 255, 150), width=10)
    sy = by + int(bh * .86); d.line((bx - 4, sy, bx + bw + 4, sy), fill=(110, 255, 225), width=4)   # linha de varredura (abaixo do rosto)
    # selo verde de acesso liberado
    cx, cy = W // 2, 930
    d.ellipse((cx - 70, cy - 70, cx + 70, cy + 70), fill=(24, 214, 110), outline=(190, 255, 220), width=7)
    d.line((cx - 32, cy + 2, cx - 8, cy + 28, cx + 38, cy - 26), fill="white", width=16, joint="curve")
    d.text((W // 2, 1060), "Acesso liberado", font=f2, fill=(120, 255, 180), anchor="mm")
    d.text((W // 2, 1135), "Seu quarto está pronto", font=f3, fill=(225, 235, 255), anchor="mm")
    d.text((W // 2, 1280), "18:42", font=ImageFont.truetype(FONTE, 96), fill="white", anchor="mm")
    d.text((W // 2, 1345), "sex, 02 out", font=f3, fill=(200, 215, 255), anchor="mm")
    return fundo

# --- aparelho de FRENTE: a foto original está em ângulo 3/4 e a cena é frontal. Alinha o vidro a um retângulo,
# reaproveita a base prateada (alto-falante) e refaz uma moldura simétrica.
term = Image.open("fotos/candidatos/terminal_u4.jpg").convert("RGB")
VIDRO = [(296, 236), (558, 248), (558, 940), (296, 948)]          # vidro preto interno (TL, TR, BR, BL)
R = (300, 240, 556, 946)                                           # onde o vidro fica depois de alinhar
Rq = [(R[0], R[1]), (R[2], R[1]), (R[2], R[3]), (R[0], R[3])]
frontal = term.transform(term.size, Image.PERSPECTIVE, coefs(Rq, VIDRO), Image.BICUBIC)
ui = tela_ui(); W, H = ui.size
tela = ui.resize((R[2] - R[0], R[3] - R[1]), Image.LANCZOS)
M = 13; CH = 78                                                    # moldura e altura da base
rw, rh = R[2] - R[0], R[3] - R[1]
D = Image.new("RGB", (rw + 2 * M, rh + CH + 2 * M), (0, 0, 0)); dd = ImageDraw.Draw(D)
for y in range(D.height):                                           # prata com gradiente vertical
    t = y / D.height; dd.line((0, y, D.width, y), fill=(int(214 - 40 * t), int(219 - 40 * t), int(228 - 38 * t)))
# base prateada desenhada (a do original vinha inclinada): grade do alto-falante + sensor
gx, gy = D.width // 2, M + rh + 30
for r_ in range(3):
    for c_ in range(9): dd.ellipse((gx - 36 + c_ * 9 - 2, gy - 12 + r_ * 9 - 2, gx - 36 + c_ * 9 + 2, gy - 12 + r_ * 9 + 2), fill=(120, 126, 138))
dd.rounded_rectangle((gx - 20, gy + 26, gx + 20, gy + 31), 3, fill=(150, 156, 168))
dd.rectangle((M - 4, M - 4, M + rw + 3, M + rh + 3), fill=(8, 8, 12))   # vidro preto com borda fina
D.paste(tela, (M, M))
refl = Image.new("L", D.size, 0); ImageDraw.Draw(refl).polygon([(M, M), (M + int(rw * .75), M), (M + int(rw * .25), M + int(rh * .55)), (M, M + int(rh * .55))], fill=34)
D = Image.composite(Image.new("RGB", D.size, "white"), D, refl.filter(ImageFilter.GaussianBlur(22)))
rec = Image.new("L", D.size, 0); ImageDraw.Draw(rec).rounded_rectangle((0, 0, D.width - 1, D.height - 1), 16, fill=255)
term_c, rec_c = D, rec.filter(ImageFilter.GaussianBlur(0.7))
h = round(ALTURA_ANTERIOR * ESCALA); w = round(term_c.width * h / term_c.height)
term_c, rec_c = term_c.resize((w, h), Image.LANCZOS), rec_c.resize((w, h), Image.LANCZOS)

# --- cena: apaga o aparelho antigo estendendo uma faixa limpa da pedra (listras horizontais)
cena = Image.open("fotos/candidatos/entrada_t2.jpg").convert("RGB")
x0, x1 = 526, 734; faixa = cena.crop((478, 258, 524, 742)).resize((x1 - x0, 484), Image.LANCZOS)
borda = Image.new("L", faixa.size, 255); ImageDraw.Draw(borda).rectangle((0, 0, faixa.width - 1, faixa.height - 1), outline=0, width=7)
cena.paste(faixa, (x0, 258), borda.filter(ImageFilter.GaussianBlur(6)))
# --- brilho da tela na parede + sombra + aparelho
px0, py0 = CENTRO[0] - w // 2, CENTRO[1] - h // 2
halo = Image.new("RGB", cena.size, (0, 0, 0)); ImageDraw.Draw(halo).rounded_rectangle((px0 - 30, py0 - 20, px0 + w + 30, py0 + h + 20), 40, fill=(120, 70, 255))
cena = ImageChops.screen(cena, halo.filter(ImageFilter.GaussianBlur(70)).point(lambda v: int(v * .36)))
sombra = Image.new("L", cena.size, 0); ImageDraw.Draw(sombra).polygon([(px + 10, py + 12) for px, py in [(px0, py0), (px0 + w, py0), (px0 + w, py0 + h), (px0, py0 + h)]], fill=150)
cena.paste(Image.new("RGB", cena.size, (20, 18, 30)), (0, 0), sombra.filter(ImageFilter.GaussianBlur(10)))
cena.paste(term_c, (px0, py0), rec_c)
cena.save("fotos/candidatos/entrada_final2.jpg", quality=95)
print("ok", (w, h), (px0, py0))
