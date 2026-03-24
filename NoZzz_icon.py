"""
NoZzz_icon.py
Genera el archivo nozzz.ico con diseño de ojo.
- Activo  : ojo abierto + punto verde arriba
- Inactivo: ojo cerrado + punto rojo arriba
"""

from PIL import Image, ImageDraw


def draw_icon(size, is_active=True):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    s = size / 64
    cx, cy = size / 2, size / 2

    # Fondo circular oscuro
    draw.ellipse([2, 2, size - 2, size - 2], fill=(30, 30, 46))

    eye_w = size * 0.60
    eye_h = size * 0.30
    eye_x0 = cx - eye_w / 2
    eye_y0 = cy - eye_h / 2
    eye_x1 = cx + eye_w / 2
    eye_y1 = cy + eye_h / 2

    if is_active:
        # === OJO ABIERTO ===
        draw.ellipse([eye_x0, eye_y0, eye_x1, eye_y1], fill=(220, 220, 220))

        # Iris
        iris_r = eye_h * 0.40
        draw.ellipse(
            [cx - iris_r, cy - iris_r, cx + iris_r, cy + iris_r],
            fill=(80, 120, 200),
        )

        # Pupila
        pupil_r = iris_r * 0.50
        draw.ellipse(
            [cx - pupil_r, cy - pupil_r, cx + pupil_r, cy + pupil_r],
            fill=(10, 10, 10),
        )

        # Reflejo
        ref_r = pupil_r * 0.38
        draw.ellipse(
            [cx - pupil_r * 0.45, cy - pupil_r * 0.65,
             cx - pupil_r * 0.45 + ref_r, cy - pupil_r * 0.65 + ref_r],
            fill=(255, 255, 255),
        )

        # Borde del ojo
        lw_eye = max(1, int(2 * s))
        draw.ellipse([eye_x0, eye_y0, eye_x1, eye_y1], outline=(160, 160, 160), width=lw_eye)

    else:
        # === OJO CERRADO (linea curva) ===
        lw_lid = max(2, int(3 * s))
        # Parpado superior como arco
        draw.arc(
            [eye_x0, eye_y0, eye_x1, eye_y1],
            start=200, end=340,
            fill=(200, 200, 200),
            width=lw_lid,
        )
        # Pestañas inferiores sutiles
        lash_y = cy + eye_h * 0.10
        lash_len = eye_h * 0.30
        for offset in [-eye_w * 0.25, 0, eye_w * 0.25]:
            draw.line(
                [cx + offset, lash_y, cx + offset, lash_y + lash_len],
                fill=(180, 180, 180),
                width=max(1, int(1.5 * s)),
            )

    # === PUNTO DE ESTADO (arriba a la derecha) ===
    dot_color = (34, 197, 94) if is_active else (239, 68, 68)
    dot_r = size * 0.13
    dot_cx = cx + size * 0.22
    dot_cy = cy - size * 0.26
    draw.ellipse(
        [dot_cx - dot_r, dot_cy - dot_r, dot_cx + dot_r, dot_cy + dot_r],
        fill=dot_color,
    )

    return img


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
