# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_data_files
import sys
import os

# Función para obtener la ruta del recurso
def resource_path(relative_path):
    """Obtiene la ruta del recurso cuando el ejecutable está empaquetado"""
    try:
        # Si está en el entorno de PyInstaller, _MEIPASS tiene la ruta
        base_path = getattr(sys, '_MEIPASS', os.path.abspath('.'))
    except AttributeError:
        base_path = os.path.abspath('.')
    
    return os.path.join(base_path, relative_path)

# Especifica las rutas necesarias
a = Analysis(
    ['main_window.py'],  # Archivo principal de tu aplicación
    pathex=['C:\\Users\\mandu\\Projects\\seismic-hazard-simulator\\Deterministic\\src'],  # Ruta del proyecto
    binaries=[],
    datas=[
        # Incluye el archivo openquake.cfg
        ('C:\\Users\\mandu\\Projects\\seismic-hazard-simulator\\Deterministic\\src\\.env\\Lib\\site-packages\\openquake\\engine\\openquake.cfg', 'openquake/engine'),
        # Incluye la carpeta openquake/hazardlib/scalerel
        ('C:\\Users\\mandu\\Projects\\seismic-hazard-simulator\\.env\\Lib\\site-packages\\openquake\\hazardlib\\scalerel', 'openquake/hazardlib/scalerel'),
        # Incluye la carpeta openquake/hazardlib/gsim
        ('C:\\Users\\mandu\\Projects\\seismic-hazard-simulator\\.env\\Lib\\site-packages\\openquake\\hazardlib\\gsim', 'openquake/hazardlib/gsim'),
    ],
    hiddenimports=[
        'openquake.hazardlib.scalerel',  # Asegúrate de que este módulo esté incluido
        'openquake.hazardlib.gsim',      # Incluye el módulo GSIM
        'openquake.hazardlib.gsim.abrahamson_2014',  # Incluye el modelo específico
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='main_window',  # Nombre del archivo .exe
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,  # Desactiva UPX para evitar problemas
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # Muestra la consola para ver los mensajes de depuración
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)