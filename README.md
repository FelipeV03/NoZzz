# NoZzz

Evita que Windows suspenda el PC mientras el programa está en ejecución.
Corre en la bandeja del sistema (system tray). Sin malware, código 100% visible.

## ¿Cómo funciona?

Usa la API oficial de Windows (`SetThreadExecutionState`) para indicarle al sistema que hay actividad en curso,
y además simula un micro-movimiento de mouse (1px y vuelta, vía `SendInput`) cada 50 segundos como refuerzo.
No simula teclas. No requiere permisos de administrador.

## Ícono en bandeja del sistema

| Ícono | Significado |
|---|---|
| Ojo abierto + punto verde | **Activo** — el PC no se suspenderá |
| Ojo cerrado + punto rojo | **Inactivo** — suspensión normal |

- **Click izquierdo** sobre el ícono: abre un pequeño panel con botones para Activar/Desactivar, Salir, y el nombre del autor (clickeable, redirige al portafolio) en el pie de la ventana.
- **Click derecho** sobre el ícono: menú con **Activar / Desactivar / Salir**.

> Mientras el panel de click izquierdo esté abierto, el menú de click derecho puede no responder hasta que lo cierres. Esto no afecta la función principal: el hilo que evita la suspensión sigue activo igual.

## Requisitos

- Windows 10 / 11
- Python 3.x
- Dependencias:

```bash
pip install pystray pillow
```

> El panel de click izquierdo usa `tkinter` y el enlace al autor (dentro del panel) usa `webbrowser`, ambos incluidos en la librería estándar de Python — no agregan dependencias nuevas.

## Uso (script Python)

```bash
python NoZzz.py
```

## Compilar a .exe

**1. Genera el ícono:**
```bash
python NoZzz_icon.py
```

**2. Instala Nuitka:**
```bash
pip install nuitka
```

**3. Compila:**
```bash
python -m nuitka --onefile --windows-console-mode=disable --enable-plugin=tk-inter --windows-icon-from-ico=nozzz.ico --include-package=pystray --include-package=PIL --output-filename=NoZzz.exe NoZzz.py
```

> `--enable-plugin=tk-inter` es necesario para empaquetar el runtime de Tcl/Tk que usa el panel de clic izquierdo (`tkinter`). Sin este flag, el `.exe` puede fallar al abrir esa ventana.

El `.exe` quedará en la misma carpeta del proyecto.

> Se recomienda Nuitka sobre PyInstaller ya que genera ejecutables con menos falsos positivos en antivirus.

## ¿Por qué es seguro?

- Código fuente completamente visible
- Solo usa `ctypes`, `pystray`, `Pillow` y librerías estándar de Python (`tkinter`, `webbrowser`)
- El movimiento de mouse que simula es real y mínimo (1px), hecho con la API oficial `SendInput`, no oculto ni con fines distintos a evitar la suspensión
- El programa no hace conexiones de red por sí mismo; el navegador solo se abre si el usuario hace click explícitamente en el enlace del autor
- No escribe en el registro de Windows
- No accede a archivos del sistema
- Compilado con Nuitka (no PyInstaller) para evitar falsos positivos en antivirus

## Autor

Desarrollado por **Felipe Vargas** — [felipe-el-dev.vercel.app](https://felipe-el-dev.vercel.app)
