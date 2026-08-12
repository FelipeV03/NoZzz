"""
NoZzz_icon.py
Genera el archivo nozzz.ico con diseño de ojo.
- Activo  : ojo abierto + punto verde arriba
- Inactivo: ojo cerrado + punto rojo arriba
"""

from PIL import Image, ImageDraw

from icon_utils import draw_icon


def draw_exe_icon(size):
    """
    Icono visual para el .exe: fondo azul noche con ZZZ flotantes en cascada
    estilo caricatura, con estrellas pequeñas y luna creciente.
    """
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    s = size / 256

    # Fondo cuadrado redondeado azul noche
    r = int(48 * s)
    draw.rounded_rectangle([0, 0, size - 1, size - 1], radius=r, fill=(18, 18, 40))

    # --- Luna creciente (abajo izquierda) ---
    moon_x = int(30 * s)
    moon_y = int(160 * s)
    moon_r = int(38 * s)
    draw.ellipse(
        [moon_x, moon_y, moon_x + moon_r * 2, moon_y + moon_r * 2],
        fill=(255, 220, 100),
    )
    # Recorte para crear el creciente
    draw.ellipse(
        [moon_x + int(14 * s), moon_y - int(10 * s),
         moon_x + moon_r * 2 + int(14 * s), moon_y - int(10 * s) + moon_r * 2],
        fill=(18, 18, 40),
    )

    # --- Estrellas pequeñas ---
    stars = [
        (int(200 * s), int(30 * s),  int(5 * s)),
        (int(40 * s),  int(50 * s),  int(4 * s)),
        (int(220 * s), int(150 * s), int(4 * s)),
        (int(160 * s), int(20 * s),  int(3 * s)),
        (int(80 * s),  int(110 * s), int(3 * s)),
    ]
    for sx, sy, sr in stars:
        draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(255, 255, 200))

    # --- ZZZ en cascada estilo caricatura ---
    try:
        from PIL import ImageFont
        font_lg = ImageFont.truetype("arialbd.ttf", int(90 * s))
        font_md = ImageFont.truetype("arialbd.ttf", int(64 * s))
        font_sm = ImageFont.truetype("arialbd.ttf", int(44 * s))
    except Exception:
        from PIL import ImageFont
        font_lg = font_md = font_sm = ImageFont.load_default()

    letters = [
        ("Z", font_sm, int(90 * s),  int(130 * s), int(4 * s)),   # pequeña, abajo
        ("Z", font_md, int(120 * s), int(80 * s),  int(3 * s)),   # mediana, centro
        ("Z", font_lg, int(148 * s), int(20 * s),  int(2 * s)),   # grande, arriba
    ]

    for letter, font, lx, ly, glow in letters:
        # Sombra/glow azul claro
        for dx in range(-glow, glow + 1):
            for dy in range(-glow, glow + 1):
                if dx != 0 or dy != 0:
                    draw.text((lx + dx, ly + dy), letter, font=font, fill=(100, 160, 255, 120))
        # Letra blanca principal
        draw.text((lx, ly), letter, font=font, fill=(255, 255, 255))

    return img


def generate_ico():
    # Icono del .exe: ZZZ visual
    sizes = [16, 32, 48, 64, 128, 256]
    frames = [draw_exe_icon(s) for s in sizes]
    frames[0].save(
        "nozzz.ico",
        format="ICO",
        sizes=[(s, s) for s in sizes],
        append_images=frames[1:],
    )
    print("nozzz.ico generado correctamente.")


if __name__ == "__main__":
    generate_ico()
