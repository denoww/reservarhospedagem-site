#!/usr/bin/env python3
"""Gera candidatos de foto (gpt-image-1) para o site reservarhospedagem.

Uso: python3 tools/gen_fotos.py [vaga ...]      (sem args = todas, 3 candidatos por vaga)
Chave: OPENAI_API_KEY no ambiente ou em ~/workspace/foundry/projeto/.env.
Saída: fotos/candidatos/<vaga>_<n>.png (gitignored). Só a escolhida vira JPEG em assets/.

Doutrina (a mesma do baterponto-site): foto = gerador, UI = HTML/CSS. Nunca texto, logo ou
tela legível na imagem — o gerador alucina ortografia. Pedido do Rodrigo para ESTE site:
pessoas brancas de aparência europeia; tom de cor do baterponto (fundo de estúdio saturado
na cor da marca, luz suave, pele realista), aqui em teal #0F766E.
"""
import base64, concurrent.futures as cf, json, os, pathlib, sys, urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "fotos" / "candidatos"
ENV = pathlib.Path.home() / "workspace" / "foundry" / "projeto" / ".env"
N = int(os.environ.get("N", "3"))

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
    "hero": ("1536x1024", ESTUDIO,
        f"A woman in her early 40s, {EURO}, light brown hair in a loose low bun, wearing a charcoal blazer "
        "over a plain white t-shirt, a friendly confident property host. She holds out a single brass "
        "apartment key toward the camera with her right hand, slight welcoming smile, looking into the lens. "
        "Composition: she occupies the right 45% of the frame, waist-up; the left half is empty seamless "
        "teal backdrop."),
    "rosto": ("1536x1024", CENA,
        f"A modern bright apartment-building corridor with light wood door and neutral walls. A man around 35, "
        f"{EURO}, short blond hair, casual linen jacket, pulls a small cabin suitcase and stands facing his "
        "apartment door, smiling, looking at a small discreet black camera-reader mounted at the door frame "
        "at head height. Warm daylight from a window at the end of the corridor, subtle teal accent on "
        "the walls. Wide shot, his face clearly visible, no phone in hands."),
    "limpeza": ("1536x1024", CENA,
        f"A bright minimalist hotel-style bedroom. A housekeeper in her 30s, {EURO}, hair tied back, wearing "
        "a plain dark teal tunic uniform without any logo, smoothing crisp white bed linen with both hands, "
        "calm focused expression, folded white towels and a teal throw blanket on the bed, large window "
        "with sheer curtains and soft daylight. Candid, mid-shot from the side."),
    "condominio": ("1024x1536", ESTUDIO,
        f"A building manager, a man in his 50s, {EURO}, short grey hair and light stubble, wearing a navy "
        "overcoat-style jacket over a pale shirt, holding a ring with several apartment keys in one hand "
        "at chest height, calm trustworthy expression, looking into the lens. Vertical portrait, waist-up, "
        "teal backdrop."),
    "pousada": ("1024x1536", ESTUDIO.replace("saturated deep teal (#0F766E) with a gentle gradient to darker teal",
                                              "saturated warm burnt amber (#B45309) with a gentle gradient to darker amber")
                                   .replace("subtle teal rim light", "subtle warm rim light"),
        f"The owner of a small inn, a woman in her mid 50s, {EURO}, silver-blonde hair, wearing a cream knit "
        "cardigan over a white blouse, holding a plain white ceramic coffee cup in both hands, warm "
        "welcoming smile, looking into the lens. Vertical portrait, waist-up."),
    "hotel": ("1024x1536", ESTUDIO.replace("saturated deep teal (#0F766E) with a gentle gradient to darker teal",
                                            "saturated deep slate-green (#1F4D47) with a gentle gradient to darker green"),
        f"A hotel front-desk receptionist, a man in his early 30s, {EURO}, neat dark-blond hair, wearing a "
        "dark charcoal vest over a white shirt with a plain dark tie, hands relaxed in front, professional "
        "friendly expression, looking into the lens. Vertical portrait, waist-up."),
}


def chave():
    if os.environ.get("OPENAI_API_KEY"):
        return os.environ["OPENAI_API_KEY"]
    for l in ENV.read_text().splitlines():
        if l.strip().startswith("OPENAI_API_KEY"):
            return l.split("=", 1)[1].strip().strip("\"'")
    sys.exit("OPENAI_API_KEY não encontrada")


def gerar(key, size, prompt):
    body = json.dumps({"model": "gpt-image-1", "prompt": prompt, "size": size,
                       "quality": os.environ.get("QUALITY", "high"), "n": 1}).encode()
    req = urllib.request.Request("https://api.openai.com/v1/images/generations", data=body,
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=900) as r:
        return base64.b64decode(json.loads(r.read())["data"][0]["b64_json"])


def uma(args):
    key, vaga, i = args
    size, estilo, texto = VAGAS[vaga]
    dest = OUT / f"{vaga}_{i}.png"
    if dest.exists():
        return f"{dest.name} (já existe)"
    try:
        dest.write_bytes(gerar(key, size, texto + estilo + NEG))
        return f"{dest.name} ok"
    except Exception as e:  # noqa
        return f"{dest.name} ERRO {str(e)[:160]}"


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    vagas = sys.argv[1:] or list(VAGAS)
    key = chave()
    tarefas = [(key, v, i) for v in vagas for i in range(1, N + 1)]
    with cf.ThreadPoolExecutor(max_workers=4) as ex:
        for r in ex.map(uma, tarefas):
            print(r, flush=True)
