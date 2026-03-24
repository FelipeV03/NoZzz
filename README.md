# Keep Awake

Evita que Windows suspenda el PC mientras el programa está en ejecución.
Usa la API oficial de Windows (`SetThreadExecutionState`). Sin malware, código 100% visible.

## ¿Cómo funciona?

Llama directamente a la API de Windows para indicarle al sistema que hay actividad en curso.
No simula movimiento del mouse ni teclas. No requiere permisos de administrador.

## Requisitos

- Windows
- Python 3.x

## Uso (script Python)

```bash
python keep_awake.py
```

Elige entre:
1. Solo evitar suspensión del sistema (ideal para bots/procesos en segundo plano)
2. Evitar suspensión + mantener pantalla encendida

Presiona `Ctrl+C` para salir y restaurar el comportamiento normal.

## Compilar a .exe

Instala PyInstaller si no lo tienes:

```bash
pip install pyinstaller
```

Compila:

```bash
pyinstaller --onefile --noconsole keep_awake.py
```

El `.exe` quedará en la carpeta `dist/`.

> Nota: `--noconsole` oculta la ventana de terminal. Quítalo si prefieres ver la consola.

## ¿Por qué es seguro?

- El código fuente es completamente visible
- Solo usa `ctypes` (librería estándar de Python) y `time`
- No hace conexiones de red
- No escribe en el registro de Windows
- No accede a archivos del sistema
