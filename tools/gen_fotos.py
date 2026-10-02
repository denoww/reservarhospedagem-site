#!/usr/bin/env python3
"""Gera candidatos de foto (AWS Bedrock, Stability) para o site reservarhospedagem.

Uso: python3 tools/gen_fotos.py [vaga ...]      (sem args = todas, N=3 candidatos por vaga)
Credencial: a da AWS CLI (perfil padrão). Região FIXA us-west-2 — em us-east-1 não há text-to-image.
Modelos: ULTRA (hero e 'rosto', ~US$ 0,14) e CORE (demais, ~US$ 0,04). OpenAI/Gemini estavam sem
crédito/cota em 02/10/2026; Nova Canvas está LEGACY e Titan morreu (ver app/services/auto/CLAUDE.md
do ERP). Saída: fotos/candidatos/<vaga>_<n>.jpg (fora do deploy). Só a escolhida vai para assets/.
Custo: cada chamada é anotada em fotos/CUSTO.log.

Doutrina (a mesma do baterponto-site): foto = gerador, UI = HTML/CSS. Nunca texto, logo ou
tela legível na imagem — o gerador alucina ortografia. Pedido do Rodrigo para ESTE site:
pessoas brancas de aparência europeia; tom de cor do baterponto (fundo de estúdio saturado
na cor da marca, luz suave, pele realista), aqui em teal #0F766E.
"""
import base64, concurrent.futures as cf, json, os, pathlib, subprocess, sys, tempfile, time

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "fotos" / "candidatos"
LOG = ROOT / "fotos" / "CUSTO.log"
N = int(os.environ.get("N", "3"))
START = int(os.environ.get("START", "1"))
REGIAO = "us-west-2"
MODELOS = {"ultra": ("stability.stable-image-ultra-v1:1", 0.14),
           "core": ("stability.stable-image-core-v1:1", 0.04)}
NEGATIVO = ("text, letters, words, numbers, signage, watermark, logo, brand, screen, display, monitor, "
            "phone screen, cartoon, illustration, painting, 3d render, plastic skin, extra fingers, "
            "deformed hands, stock photo, oversaturated")

NEG = (" No text, no lettering, no numbers, no signage, no logos, no watermarks anywhere in the frame. "
       "Any smartphone or tablet screen is turned away from the camera or dark and blank — never show a "
       "readable or glowing screen. Natural skin texture, candid and unposed, not stock-photo, not "
       "cartoon, no plastic skin, correct hands with five fingers.")

ESTUDIO = (" Editorial portrait photograph shot on a full-frame camera with an 85mm lens, shallow depth of "
           "field, soft studio key light with a subtle teal rim light, realistic skin texture. Seamless "
           "studio backdrop in saturated deep teal (#0F766E) with a gentle gradient to darker teal at the "
           "edges, cinematic color grading, same look as a premium product campaign.")

CENA = (" Editorial documentary photograph, natural available light, full-frame camera, 35mm lens, shallow "
        "depth of field, realistic textures, cinematic color grading with deep teal and warm neutral "
        "tones, calm premium hospitality mood.")

EURO = "fair skin, Northern European appearance"

VAGAS = {
    # hero: sujeito à direita, campo teal vazio à esquerda (o texto do hero fica ali no desktop)
    "hero": ("ultra", "16:9", ESTUDIO,
        f"A woman in her early 40s, {EURO}, light brown hair in a loose low bun, wearing a charcoal blazer "
        "over a plain white t-shirt, a friendly confident property host. She holds out a single brass "
        "apartment key toward the camera with her right hand, slight welcoming smile, looking into the lens. "
        "Composition: she occupies the right 45% of the frame, waist-up; the left half is empty seamless "
        "teal backdrop."),
    "rosto": ("ultra", "16:9", CENA,
        f"A modern bright apartment-building corridor with light wood door and neutral walls. A man around 35, "
        f"{EURO}, short blond hair, casual linen jacket, pulls a small cabin suitcase and stands facing his "
        "apartment door, smiling, looking at a small discreet black camera-reader mounted at the door frame "
        "at head height. Warm daylight from a window at the end of the corridor, subtle teal accent on "
        "the walls. Wide shot, his face clearly visible, no phone in hands."),
    "limpeza": ("core", "3:2", CENA,
        f"A bright minimalist hotel-style bedroom. A housekeeper in her 30s, {EURO}, hair tied back, wearing "
        "a plain dark teal tunic uniform without any logo, smoothing crisp white bed linen with both hands, "
        "calm focused expression, folded white towels and a teal throw blanket on the bed, large window "
        "with sheer curtains and soft daylight. Candid, mid-shot from the side."),
    "condominio": ("core", "2:3", ESTUDIO,
        f"A building manager, a man in his 50s, {EURO}, short grey hair and light stubble, wearing a navy "
        "overcoat-style jacket over a pale shirt, holding a ring with several apartment keys in one hand "
        "at chest height, calm trustworthy expression, looking into the lens. Vertical portrait, waist-up, "
        "teal backdrop."),
    "pousada": ("core", "2:3", ESTUDIO.replace("saturated deep teal (#0F766E) with a gentle gradient to darker teal",
                                              "saturated warm burnt amber (#B45309) with a gentle gradient to darker amber")
                                   .replace("subtle teal rim light", "subtle warm rim light"),
        f"The owner of a small inn, a woman in her mid 50s, {EURO}, silver-blonde hair, wearing a cream knit "
        "cardigan over a white blouse, holding a plain white ceramic coffee cup in both hands, warm "
        "welcoming smile, looking into the lens. Vertical portrait, waist-up."),
    "hotel": ("core", "2:3", ESTUDIO.replace("saturated deep teal (#0F766E) with a gentle gradient to darker teal",
                                            "saturated deep slate-green (#1F4D47) with a gentle gradient to darker green"),
        f"A hotel front-desk receptionist, a man in his early 30s, {EURO}, neat dark-blond hair, wearing a "
        "dark charcoal vest over a white shirt with a plain dark tie, hands relaxed in front, professional "
        "friendly expression, looking into the lens. Vertical portrait, waist-up."),
}


def gerar(modelo, aspecto, prompt, seed):
    mid, _ = MODELOS[modelo]
    corpo = {"prompt": prompt[:9500], "aspect_ratio": aspecto, "output_format": "jpeg",
             "negative_prompt": NEGATIVO, "seed": seed}
    with tempfile.TemporaryDirectory() as t:
        b, o = pathlib.Path(t, "b.json"), pathlib.Path(t, "o.json")
        b.write_text(json.dumps(corpo))
        r = subprocess.run(["aws", "bedrock-runtime", "invoke-model", "--region", REGIAO, "--model-id", mid,
                            "--body", f"fileb://{b}", "--cli-binary-format", "raw-in-base64-out", str(o)],
                           capture_output=True, text=True, timeout=300)
        if r.returncode:
            raise RuntimeError(r.stderr.strip()[-200:])
        d = json.loads(o.read_text())
        if d.get("finish_reasons", [None])[0]:
            raise RuntimeError(f"filtrada: {d['finish_reasons']}")
        return base64.b64decode(d["images"][0])


def uma(args):
    vaga, i = args
    modelo, aspecto, estilo, texto = VAGAS[vaga]
    dest = OUT / f"{vaga}_{i}.jpg"
    if dest.exists():
        return f"{dest.name} (já existe)"
    try:
        dest.write_bytes(gerar(modelo, aspecto, texto + estilo + NEG, 1000 + i * 7919 + len(vaga)))
        with LOG.open("a") as f:
            f.write(f"{time.strftime('%F %T')} {vaga}_{i} {modelo} {MODELOS[modelo][1]}\n")
        return f"{dest.name} ok ({modelo})"
    except Exception as e:  # noqa
        return f"{dest.name} ERRO {str(e)[:200]}"


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    vagas = sys.argv[1:] or list(VAGAS)
    tarefas = [(v, i) for v in vagas for i in range(START, START + N)]
    with cf.ThreadPoolExecutor(max_workers=3) as ex:
        for r in ex.map(uma, tarefas):
            print(r, flush=True)
