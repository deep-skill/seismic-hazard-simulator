import os
from PyQt6.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QDialog
from PyQt6.QtCore import Qt

from group_manager import GroupManager
from settings import PROJECT_FOLDER
from group_load import GroupLoad


class SeismicWindow(QDialog):
    def __init__(self):
        super().__init__()

        self.groups = []

        screen = QApplication.primaryScreen()
        available_geometry = screen.availableGeometry()  # Without taskbar, etc.

        available_width = available_geometry.width()
        available_height = available_geometry.height()
        self.setGeometry(0, 0, available_width, available_height)

        self.group_layout = QVBoxLayout()
        self.build_main_panel()

    def build_main_panel(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        title_label = QLabel('Seismic Hazard')
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet(
            """
                    QLabel {
                        font-size: 26px;
                        font-weight: bold;
                        margin-bottom: 150px;
                    }
                """
        )
        layout.addWidget(title_label)

        self.build_group_buttons_panel(layout)

        self.setLayout(layout)

    def build_group_buttons_panel(self, parent_layout):
        group_buttons_panel = QWidget()

        self.update_group_list()

        group_buttons_panel.setLayout(self.group_layout)
        parent_layout.addWidget(group_buttons_panel)

    def update_group_list(self):
        self._clear_layout()
        self.group_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        all_files = os.listdir(PROJECT_FOLDER)

        # Filtrar solo los archivos
        self.groups = [os.path.splitext(f)[0] for f in all_files if os.path.isfile(os.path.join(PROJECT_FOLDER, f)) and f.endswith('.txt')]

        for group_name in self.groups:
            current_group_panel = QWidget()
            current_group_layout = QHBoxLayout()

            group_button = QPushButton(group_name)
            group_button.clicked.connect(lambda checked, name=group_name: self.open_group_load(name))

            edit_button = QPushButton('Editar')
            edit_button.clicked.connect(lambda checked, name=group_name: self.edit_group(name))

            current_group_layout.addWidget(group_button)
            current_group_layout.addWidget(edit_button)

            current_group_layout.setStretch(0, 4)
            current_group_layout.setStretch(1, 1)

            current_group_panel.setLayout(current_group_layout)
            self.group_layout.addWidget(current_group_panel)

        create_group_button = QPushButton('Crear grupo')
        create_group_button.setStyleSheet("""
            QPushButton {
                border: 2px dashed #1c8cff; /* Línea cortada negra */
            }
        """)
        create_group_button.clicked.connect(self.create_group)

        self.group_layout.addWidget(create_group_button)
        self.group_layout.setContentsMargins(100, 0, 100, 0)

    def _clear_layout(self):
        for i in reversed(range(self.group_layout.count())):
            widget = self.group_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

    def open_group_load(self, group_name):
        self.hide()

        group_load = GroupLoad(group_name, parent_window=self)
        group_load.exec()

    def create_group(self):
        self.hide()

        group_manager = GroupManager(parent_window=self)
        group_manager.exec()

    def edit_group(self, group_name):
        self.hide()

        group_manager = GroupManager(group_name, parent_window=self)
        group_manager.exec()

