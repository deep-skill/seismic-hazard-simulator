import os
from PyQt6.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, \
    QMessageBox, QLineEdit, QDialog, QSpacerItem, QSizePolicy, \
    QLineEdit, QComboBox
from openquake.hazardlib.gsim import get_available_gsims
from seismic_utils import import_gmpes_weights

from settings import PROJECT_FOLDER


class GroupManager(QDialog):
    def __init__(self, group_name: str | None = None, parent_window: QDialog = None):
        super().__init__()
        self.group_name_initial = group_name
        self.gmpes, self.weights = import_gmpes_weights(group_name)

        self.parent_window = parent_window

        # QLineEdit
        self.group_name_input = QLineEdit()
        self.group_name_input.setText(self.group_name_initial)

        # GMPE layout
        self.gmpe_layout = QVBoxLayout()

        screen = QApplication.primaryScreen()
        available_geometry = screen.availableGeometry()  # Without taskbar, etc.

        available_width = available_geometry.width()
        available_height = available_geometry.height()

        self.setGeometry(0, 0, available_width // 2, available_height * 4 // 5)

        self.build_main_panel()

    def build_main_panel(self):
        layout = QVBoxLayout()

        layout.addWidget(self.group_name_input)

        self.build_gmpe_comboboxes(layout)

        spacer = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        layout.addItem(spacer)

        save_group_button = QPushButton('Guardar grupo')
        save_group_button.clicked.connect(self.save_group)

        layout.addWidget(save_group_button)

        self.setLayout(layout)

    def build_gmpe_comboboxes(self, parent_layout):
        gmpe_panel = QWidget()

        self.update_gmpe_comboboxes()

        gmpe_panel.setLayout(self.gmpe_layout)
        parent_layout.addWidget(gmpe_panel)

    def update_gmpe_comboboxes(self):
        self._clear_layout()
        for i, gmpe in enumerate(self.gmpes):
            current_gmpe_panel = QWidget()
            current_layout = QHBoxLayout()

            combo = QComboBox()
            combo.setEditable(True)
            combo.addItems(get_available_gsims())

            combo.setCurrentText(gmpe)
            combo.currentTextChanged.connect(lambda text, index=i: self.gmpe_combobox_changed(text, index))

            # combo.setStyleSheet(""" QComboBox { color = white; } """)

            weight_input = QLineEdit()
            weight_input.setText(str(self.weights[i]))
            weight_input.textChanged.connect(lambda text, index=i: self.weight_input_changed(text, index))

            delete_button = QPushButton('Borrar')
            delete_button.clicked.connect(lambda checked, index=i: self.delete_gmpe_from_list(index))

            current_layout.addWidget(combo)
            current_layout.addWidget(weight_input)
            current_layout.addWidget(delete_button)
            current_layout.setContentsMargins(0, 0, 0, 0)

            current_gmpe_panel.setLayout(current_layout)

            self.gmpe_layout.addWidget(current_gmpe_panel)

        add_gmpe_button = QPushButton('Añadir GMPE')
        add_gmpe_button.setStyleSheet("""
            QPushButton {
                border: 2px dashed #1c8cff; /* Línea cortada negra */
            }
        """)

        add_gmpe_button.clicked.connect(self.add_gmpe)
        self.gmpe_layout.addWidget(add_gmpe_button)

    def add_gmpe(self):
        self.gmpes.append(list(get_available_gsims().keys())[0])
        self.weights.append(0)
        self.update_gmpe_comboboxes()

    def gmpe_combobox_changed(self, text, index):
        self.gmpes[index] = text

    def weight_input_changed(self, text, index):
        if not text.isdigit():
            self.weights[index] = 0
            return

        self.weights[index] = int(text)

    def delete_gmpe_from_list(self, index):
        self.gmpes.pop(index)
        self.weights.pop(index)
        self.update_gmpe_comboboxes()

    def _clear_layout(self):
        for i in reversed(range(self.gmpe_layout.count())):
            widget = self.gmpe_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

    def save_group(self):
        if not os.path.exists(PROJECT_FOLDER):
            os.mkdir(PROJECT_FOLDER)

        if self.group_name_input.text().strip() == '':
            QMessageBox.critical(self,
                                 "Error",
                                 "Nombre de grupo faltante",
                                 QMessageBox.StandardButton.Ok)
            return

        self.close()

        if self.group_name_initial is not None:
            group_path = os.path.join(PROJECT_FOLDER, self.group_name_initial + '.txt')

            if os.path.exists(group_path) and os.path.isfile(group_path):
                os.remove(group_path)

        group_name = self.group_name_input.text().strip()
        group_path = os.path.join(PROJECT_FOLDER, group_name + '.txt')

        if os.path.exists(group_path) and os.path.isfile(group_path):
            os.remove(group_path)

        with open(group_path, 'w') as f:
            assert(len(self.gmpes) == len(self.weights))

            for i in range(len(self.gmpes)):
                f.write(self.gmpes[i] + ' ' + str(self.weights[i]) + '\n')

        self.parent_window.show()
        self.parent_window.update_group_list()

