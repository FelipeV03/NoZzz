"""
NoZzz - Evita que Windows suspenda el PC.
Corre en la bandeja del sistema (system tray).
Usa la API oficial de Windows: SetThreadExecutionState
"""

import ctypes
import ctypes.wintypes
import logging
import threading
import time
import tkinter as tk
import webbrowser
import pystray
from PIL import ImageTk

from icon_utils import draw_icon

logging.basicConfig(level=logging.WARNING, format="%(asctime)s NoZzz [%(levelname)s] %(message)s")
logger = logging.getLogger("NoZzz")

ES_CONTINUOUS      = 0x80000000
ES_SYSTEM_REQUIRED = 0x00000001

INPUT_MOUSE       = 0
MOUSEEVENTF_MOVE  = 0x0001

active = True
lock = threading.Lock()

# Referencia a la ventana de control abierta (None si está cerrada). Permite
# evitar abrir dos instancias y deshabilitar el menú de bandeja mientras está abierta.
_window_ref = {"root": None}


def _window_is_open(item=None):
    return _window_ref["root"] is not None

PORTFOLIO_URL = "https://felipe-el-dev.vercel.app"
AUTHOR_NAME = "Felipe Vargas"

# Paleta tomada del propio ícono (icon_utils.draw_icon)
COLOR_BG          = "#1e1e2e"  # fondo del ícono
COLOR_BG_FOOTER   = "#15151f"
COLOR_ACCENT      = "#5078c8"  # iris del ojo
COLOR_ACCENT_HOVER = "#6a8ed6"
COLOR_TEXT        = "#e8e8f0"
COLOR_TEXT_MUTED  = "#8a8aa0"
COLOR_ACTIVE      = "#22c55e"  # punto verde
COLOR_INACTIVE    = "#ef4444"  # punto rojo
COLOR_BORDER      = "#32324a"
COLOR_BTN_SECONDARY       = "#2a2a3d"
COLOR_BTN_SECONDARY_HOVER = "#38384f"


def open_portfolio(icon=None, item=None):
    """Abre el portafolio del autor en el navegador predeterminado (acción explícita del usuario)."""
    webbrowser.open(PORTFOLIO_URL)


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

    sent = ctypes.windll.user32.SendInput(1, ctypes.byref(inp_move), ctypes.sizeof(INPUT))
    if sent != 1:
        logger.warning("SendInput no pudo inyectar el movimiento de mouse (return=%s).", sent)
        return
    time.sleep(0.05)
    sent = ctypes.windll.user32.SendInput(1, ctypes.byref(inp_back), ctypes.sizeof(INPUT))
    if sent != 1:
        logger.warning("SendInput no pudo revertir el movimiento de mouse (return=%s).", sent)


def apply_execution_state(is_active):
    """Aplica el estado a Windows vía SetThreadExecutionState y loguea si falla."""
    flags = (ES_CONTINUOUS | ES_SYSTEM_REQUIRED) if is_active else ES_CONTINUOUS
    result = ctypes.windll.kernel32.SetThreadExecutionState(flags)
    if result == 0:
        logger.warning("SetThreadExecutionState falló (return=0) al aplicar estado activo=%s.", is_active)


def keep_awake_loop():
    while True:
        try:
            with lock:
                is_active = active
            apply_execution_state(is_active)
            if is_active:
                simulate_activity()
        except Exception:
            logger.exception("Error inesperado en keep_awake_loop; se reintentará en el próximo ciclo.")
        time.sleep(50)  # Cada 50s — seguro para políticas de bloqueo desde 1 minuto


def toggle_active(icon):
    """Alterna el estado activo/inactivo, aplica el cambio en Windows y sincroniza el ícono. Devuelve el nuevo estado."""
    global active
    with lock:
        active = not active
        is_active = active

    apply_execution_state(is_active)

    if icon is not None:
        icon.icon = draw_icon(64, is_active)
        icon.title = "NoZzz - Activo" if is_active else "NoZzz - Inactivo"
        icon.update_menu()

    return is_active


def quit_app(icon):
    """Libera el estado de Windows y detiene el ícono de bandeja."""
    apply_execution_state(False)
    if icon is not None:
        icon.stop()


def on_toggle(icon, item):
    toggle_active(icon)


def on_quit(icon, item):
    quit_app(icon)


def _make_flat_button(parent, text, bg, hover_bg, command):
    """Botón plano con efecto hover, siguiendo la paleta oscura del ícono."""
    btn = tk.Button(
        parent, text=text, command=command,
        font=("Segoe UI", 10), fg=COLOR_TEXT, bg=bg,
        activeforeground=COLOR_TEXT, activebackground=hover_bg,
        relief="flat", bd=0, cursor="hand2", width=24, pady=8,
        highlightthickness=0,
    )
    btn.bind("<Enter>", lambda e: btn.config(bg=hover_bg))
    btn.bind("<Leave>", lambda e: btn.config(bg=bg))
    return btn


def show_window(icon, item):
    """Abre una pequeña ventana con controles (clic izquierdo del ícono de bandeja).
    Si ya hay una abierta, la trae al frente en vez de crear una segunda."""
    existing = _window_ref["root"]
    if existing is not None:
        try:
            existing.deiconify()
            existing.lift()
            existing.focus_force()
        except tk.TclError:
            _window_ref["root"] = None
        else:
            return

    root = tk.Tk()
    _window_ref["root"] = root
    if icon is not None:
        icon.update_menu()
    root.title("NoZzz")
    root.configure(bg=COLOR_BG)
    root.resizable(False, False)
    root.attributes("-topmost", True)

    window_icon = ImageTk.PhotoImage(draw_icon(64, active))
    root.iconphoto(True, window_icon)

    header = tk.Frame(root, bg=COLOR_BG)
    header.pack(fill="x", padx=24, pady=(20, 4))

    header_icon = ImageTk.PhotoImage(draw_icon(32, active))
    icon_label = tk.Label(header, image=header_icon, bg=COLOR_BG)
    icon_label.pack(side="left", padx=(0, 8))

    tk.Label(header, text="NoZzz", font=("Segoe UI", 14, "bold"), fg=COLOR_TEXT, bg=COLOR_BG).pack(side="left")

    status_var = tk.StringVar(value="● Activo" if active else "● Inactivo")
    status_label = tk.Label(
        root, textvariable=status_var, font=("Segoe UI", 10, "bold"),
        fg=COLOR_ACTIVE if active else COLOR_INACTIVE, bg=COLOR_BG,
    )
    status_label.pack(pady=(0, 16))

    def handle_toggle():
        is_active = toggle_active(icon)
        status_var.set("● Activo" if is_active else "● Inactivo")
        status_label.config(fg=COLOR_ACTIVE if is_active else COLOR_INACTIVE)
        toggle_btn.config(text="Desactivar" if is_active else "Activar")

        new_header_icon = ImageTk.PhotoImage(draw_icon(32, is_active))
        icon_label.config(image=new_header_icon)
        icon_label.image = new_header_icon

        new_window_icon = ImageTk.PhotoImage(draw_icon(64, is_active))
        root.iconphoto(True, new_window_icon)
        root.image = new_window_icon

    toggle_btn = _make_flat_button(
        root, "Desactivar" if active else "Activar",
        COLOR_ACCENT, COLOR_ACCENT_HOVER, handle_toggle,
    )
    toggle_btn.pack(padx=24, pady=4)

    def handle_quit():
        quit_app(icon)
        root.destroy()

    quit_btn = _make_flat_button(root, "Salir", COLOR_BTN_SECONDARY, COLOR_BTN_SECONDARY_HOVER, handle_quit)
    quit_btn.pack(padx=24, pady=(4, 20))

    footer = tk.Frame(root, bg=COLOR_BG_FOOTER)
    footer.pack(fill="x", side="bottom")
    tk.Frame(footer, bg=COLOR_BORDER, height=1).pack(fill="x")

    tk.Label(
        footer, text="Desarrollado por", font=("Segoe UI", 7),
        fg=COLOR_TEXT_MUTED, bg=COLOR_BG_FOOTER,
    ).pack(pady=(8, 0))

    author = tk.Label(
        footer, text=AUTHOR_NAME, font=("Segoe UI", 9, "bold"),
        fg=COLOR_TEXT_MUTED, bg=COLOR_BG_FOOTER, cursor="hand2",
    )
    author.pack(pady=(0, 10))
    author.bind("<Button-1>", lambda event: open_portfolio())
    author.bind("<Enter>", lambda e: author.config(fg=COLOR_ACCENT))
    author.bind("<Leave>", lambda e: author.config(fg=COLOR_TEXT_MUTED))

    root.mainloop()
    _window_ref["root"] = None
    if icon is not None:
        icon.update_menu()


def main():
    t = threading.Thread(target=keep_awake_loop, daemon=True)
    t.start()

    icon = pystray.Icon("NoZzz")
    icon.icon = draw_icon(64, True)
    icon.title = "NoZzz - Activo"
    icon.menu = pystray.Menu(
        pystray.MenuItem("Abrir panel", show_window, default=True, visible=False),
        pystray.MenuItem(
            lambda item: "NoZzz - Activo" if active else "NoZzz - Inactivo",
            None,
            enabled=False,
        ),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem(
            lambda item: "Desactivar" if active else "Activar",
            on_toggle,
            enabled=lambda item: not _window_is_open(),
        ),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem("Salir", on_quit, enabled=lambda item: not _window_is_open()),
    )
    icon.run()


if __name__ == "__main__":
    main()
