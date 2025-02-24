import sys
import os

def resource_path(relative_path):
    """Obtiene la ruta del recurso cuando el ejecutable está empaquetado"""
    try:
        # Si está en el entorno de PyInstaller, _MEIPASS tiene la ruta
        base_path = getattr(sys, '_MEIPASS', os.path.abspath('.'))
    except AttributeError:
        base_path = os.path.abspath('.')
    
    # Si se ejecuta localmente, busca en la carpeta .env
    if not os.path.exists(os.path.join(base_path, relative_path)):
        base_path = os.path.join(base_path, '.env', 'Lib', 'site-packages')
    
    return os.path.join(base_path, relative_path)

# Cargar el archivo de configuración
config_path = resource_path('openquake/engine/openquake.cfg')
print(f"Buscando configuración en: {config_path}")  # Imprime la ruta completa

if os.path.exists(config_path):
    try:
        with open(config_path, 'r') as config_file:
            config = config_file.read()
            print("Configuración cargada correctamente")
    except PermissionError as e:
        print(f"Error de permisos: {e}")
else:
    print(f"Error: no se encontró el archivo {config_path}")

# Resto del código del archivo main_window.py
from PyQt6.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QVBoxLayout
from qt_material import apply_stylesheet

from weichert_window import WeichertWindow
from seismic_window import SeismicWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setGeometry(100, 100, 600, 400)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.build_main_panel()

    def build_main_panel(self):
        layout = QVBoxLayout(self.central_widget)

        weichert_button = QPushButton('Weichert algorithm')
        weichert_button.clicked.connect(self.open_weichert_window)

        seismic_button = QPushButton('Seismic Hazard')
        seismic_button.clicked.connect(self.open_seismic_window)

        layout.addWidget(weichert_button)
        layout.addWidget(seismic_button)

    def open_weichert_window(self):
        self.close()

        weichert_window = WeichertWindow()
        weichert_window.exec()

    def open_seismic_window(self):
        self.close()

        seismic_window = SeismicWindow()
        seismic_window.exec()

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    apply_stylesheet(app, theme='dark_blue.xml')

    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()