import sys
from PyQt6.QtWidgets import QDialog, QMainWindow, QApplication, QWidget, QHBoxLayout, QPushButton, QVBoxLayout
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

