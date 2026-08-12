"""
icon_utils.py
Dibuja el ícono de bandeja (ojo abierto/cerrado + punto de estado).
Compartido entre NoZzz.py (ícono en vivo) y NoZzz_icon.py (generación del .ico).
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
