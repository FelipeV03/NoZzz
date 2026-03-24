# NoZzz

Evita que Windows suspenda el PC mientras el programa está en ejecución.
Corre en la bandeja del sistema (system tray). Sin malware, código 100% visible.

## ¿Cómo funciona?

Usa la API oficial de Windows (`SetThreadExecutionState`) para indicarle al sistema que hay actividad en curso.
No simula movimiento del mouse ni teclas. No requiere permisos de administrador.

## Ícono en bandeja del sistema

| Ícono | Significado |
|---|---|
| Ojo abierto + punto verde | **Activo** — el PC no se suspenderá |
| Ojo cerrado + punto rojo | **Inactivo** — suspensión normal |

Click derecho sobre el ícono para **Activar / Desactivar / Salir**.

## Requisitos

- Windows 10 / 11
- Python 3.x
- Dependencias:

```bash
pip install pystray pillow
```

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
python -m nuitka --onefile --windows-console-mode=disable --windows-icon-from-ico=nozzz.ico --include-package=pystray --include-package=PIL --output-filename=NoZzz.exe NoZzz.py
```

El `.exe` quedará en la misma carpeta del proyecto.

> Se recomienda Nuitka sobre PyInstaller ya que genera ejecutables con menos falsos positivos en antivirus.

## ¿Por qué es seguro?

- Código fuente completamente visible
- Solo usa `ctypes`, `pystray` y `Pillow`
- No hace conexiones de red
- No escribe en el registro de Windows
- No accede a archivos del sistema
- Compilado con Nuitka (no PyInstaller) para evitar falsos positivos en antivirus
