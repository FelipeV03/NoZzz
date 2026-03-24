"""
NoZzz - Evita que Windows suspenda el PC.
Corre en la bandeja del sistema (system tray).
Usa la API oficial de Windows: SetThreadExecutionState
"""

import ctypes
import ctypes.wintypes
import threading
import time
from PIL import Image, ImageDraw
import pystray

ES_CONTINUOUS      = 0x80000000
ES_SYSTEM_REQUIRED = 0x00000001

INPUT_MOUSE       = 0
MOUSEEVENTF_MOVE  = 0x0001

active = True
lock = threading.Lock()


class MOUSEINPUT(ctypes.Structure):
    _fields_ = [
        ("dx",          ctypes.c_long),
        ("dy",          ctypes.c_long),
        ("mouseData",   ctypes.c_ulong),
        ("dwFlags",     ctypes.c_ulong),
        ("time",        ctypes.c_ulong),
        ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong)),
    ]


class INPUT(ctypes.Structure):
    _fields_ = [
        ("type", ctypes.c_ulong),
        ("mi",   MOUSEINPUT),
    ]


def draw_icon(size, is_active):
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

        iris_r = eye_h * 0.40
        draw.ellipse(
            [cx - iris_r, cy - iris_r, cx + iris_r, cy + iris_r],
            fill=(80, 120, 200),
        )

        pupil_r = iris_r * 0.50
        draw.ellipse(
            [cx - pupil_r, cy - pupil_r, cx + pupil_r, cy + pupil_r],
            fill=(10, 10, 10),
        )

        ref_r = pupil_r * 0.38
        draw.ellipse(
            [cx - pupil_r * 0.45, cy - pupil_r * 0.65,
             cx - pupil_r * 0.45 + ref_r, cy - pupil_r * 0.65 + ref_r],
            fill=(255, 255, 255),
        )

        lw_eye = max(1, int(2 * s))
        draw.ellipse([eye_x0, eye_y0, eye_x1, eye_y1], outline=(160, 160, 160), width=lw_eye)

    else:
        # === OJO CERRADO (linea curva) ===
        lw_lid = max(2, int(3 * s))
        draw.arc(
            [eye_x0, eye_y0, eye_x1, eye_y1],
            start=200, end=340,
            fill=(200, 200, 200),
            width=lw_lid,
        )
        lash_y = cy + eye_h * 0.10
        lash_len = eye_h * 0.30
        for offset in [-eye_w * 0.25, 0, eye_w * 0.25]:
            draw.line(
                [cx + offset, lash_y, cx + offset, lash_y + lash_len],
                fill=(180, 180, 180),
                width=max(1, int(1.5 * s)),
            )

    # === PUNTO DE ESTADO ===
    dot_color = (34, 197, 94) if is_active else (239, 68, 68)
    dot_r = size * 0.13
    dot_cx = cx + size * 0.22
    dot_cy = cy - size * 0.26
    draw.ellipse(
        [dot_cx - dot_r, dot_cy - dot_r, dot_cx + dot_r, dot_cy + dot_r],
        fill=dot_color,
    )

    return img


def simulate_activity():
    """Inyecta un micro-movimiento de mouse via SendInput (reconocido por Windows como input real)."""
    inp_move = INPUT()
    inp_move.type = INPUT_MOUSE
    inp_move.mi.dx = 1
    inp_move.mi.dy = 0
    inp_move.mi.dwFlags = MOUSEEVENTF_MOVE

    inp_back = INPUT()
    inp_back.type = INPUT_MOUSE
    inp_back.mi.dx = -1
    inp_back.mi.dy = 0
    inp_back.mi.dwFlags = MOUSEEVENTF_MOVE

    ctypes.windll.user32.SendInput(1, ctypes.byref(inp_move), ctypes.sizeof(INPUT))
    time.sleep(0.05)
    ctypes.windll.user32.SendInput(1, ctypes.byref(inp_back), ctypes.sizeof(INPUT))


def keep_awake_loop():
    while True:
        with lock:
            is_active = active
        flags = (ES_CONTINUOUS | ES_SYSTEM_REQUIRED) if is_active else ES_CONTINUOUS
        ctypes.windll.kernel32.SetThreadExecutionState(flags)
        if is_active:
            simulate_activity()
        time.sleep(50)  # Cada 50s — seguro para políticas de bloqueo desde 1 minuto


def on_toggle(icon, item):
    global active
    with lock:
        active = not active
        is_active = active

    flags = (ES_CONTINUOUS | ES_SYSTEM_REQUIRED) if is_active else ES_CONTINUOUS
    ctypes.windll.kernel32.SetThreadExecutionState(flags)

    icon.icon = draw_icon(64, is_active)
    icon.title = "NoZzz - Activo" if is_active else "NoZzz - Inactivo"
    icon.update_menu()


def on_quit(icon, item):
    ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS)
    icon.stop()


def main():
    global active
    active = True

    t = threading.Thread(target=keep_awake_loop, daemon=True)
    t.start()

    icon = pystray.Icon("NoZzz")
    icon.icon = draw_icon(64, True)
    icon.title = "NoZzz - Activo"
    icon.menu = pystray.Menu(
        pystray.MenuItem(
            lambda item: "NoZzz - Activo" if active else "NoZzz - Inactivo",
            None,
            enabled=False,
        ),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem(lambda item: "Desactivar" if active else "Activar", on_toggle),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem("Salir", on_quit),
    )
    icon.run()


if __name__ == "__main__":
    main()
