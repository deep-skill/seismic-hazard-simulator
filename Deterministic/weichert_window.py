from weichert import compute_weichert_values
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QFileDialog, QMessageBox, QRadioButton, QButtonGroup, QLineEdit, QLayout, QDialog
from PyQt6.QtCore import Qt


CATALOGUE = 1
COMPLETENESS = 2

class WeichertWindow(QDialog):
    def __init__(self):
        super().__init__()

        self.setGeometry(100, 100, 500, 300)

        # File Path
        self.catalogue_file_name = None
        self.completeness_file_name = None

        self.comp_option = None

        # Widgets
        self.radio_import = QRadioButton("Import from computer")
        self.radio_generate = QRadioButton("Generate (Stepp1971)")
        self.radio_none = QRadioButton("Do not import or generate")

        self.m_min_input = QLineEdit()
        self.mag_interval_input = QLineEdit()

        self.setWindowTitle("Truncated GR Weichert from Weichert")
        self.build_main_panel()


    def build_main_panel(self):
        layout = QVBoxLayout()

        self.build_data_entry_panel(layout)
        generate_button = QPushButton('Generate plot and results')
        generate_button.clicked.connect(self.solve)

        layout.addWidget(generate_button)

        self.setLayout(layout)

    def build_data_entry_panel(self, parent_layout: QLayout):
        data_entry_panel = QWidget()
        layout = QHBoxLayout()

        self.build_catalogue_panel(layout)
        self.build_completeness_panel(layout)
        self.build_settings_panel(layout)

        data_entry_panel.setLayout(layout)
        parent_layout.addWidget(data_entry_panel)

    def build_catalogue_panel(self, parent_layout: QLayout):
        catalogue_panel = QWidget()
        layout = QVBoxLayout()

        label = QLabel('Catalogue')
        select_file_button = QPushButton('Select catalogue')
        select_file_button.clicked.connect(lambda: self.open_file_dialog(CATALOGUE))

        layout.addWidget(label)
        layout.addWidget(select_file_button)

        layout.setAlignment(label, Qt.AlignmentFlag.AlignTop)

        catalogue_panel.setLayout(layout)
        parent_layout.addWidget(catalogue_panel)

    def build_completeness_panel(self, parent_layout: QLayout):
        completeness_panel = QWidget()
        layout = QVBoxLayout()

        label = QLabel('Completeness')


        button_group = QButtonGroup()
        button_group.addButton(self.radio_import)
        button_group.addButton(self.radio_generate)
        button_group.addButton(self.radio_none)

        select_file_button = QPushButton('Select completeness')
        select_file_button.clicked.connect(lambda: self.open_file_dialog(COMPLETENESS))

        self.radio_import.toggled.connect(lambda: self.update_radio_buttons(select_file_button))
        self.radio_generate.toggled.connect(lambda: self.update_radio_buttons(select_file_button))
        self.radio_none.toggled.connect(lambda: self.update_radio_buttons(select_file_button))

        self.radio_none.setChecked(True)

        layout.addWidget(label)
        layout.addWidget(self.radio_import)
        layout.addWidget(select_file_button)
        layout.addWidget(self.radio_generate)
        layout.addWidget(self.radio_none)

        layout.setAlignment(label, Qt.AlignmentFlag.AlignTop)

        completeness_panel.setLayout(layout)
        parent_layout.addWidget(completeness_panel)

    def update_radio_buttons(self, import_file_button: QPushButton):
        if self.radio_import.isChecked():
            import_file_button.setEnabled(True)
            self.comp_option = 'import'
        elif self.radio_generate.isChecked():
            import_file_button.setEnabled(False)
            self.comp_option = 'generate'
        else:
            import_file_button.setEnabled(False)
            self.comp_option = 'none'

    def build_settings_panel(self, parent_layout: QLayout):
        settings_panel = QWidget()
        layout = QVBoxLayout()

        label = QLabel('Settings')

        m_min_label = QLabel('M min: ')

        mag_interval_label = QLabel('Magnitude interval: ')

        layout.addWidget(label)
        layout.addWidget(m_min_label)
        layout.addWidget(self.m_min_input)
        layout.addWidget(mag_interval_label)
        layout.addWidget(self.mag_interval_input)

        layout.setAlignment(label, Qt.AlignmentFlag.AlignTop)

        settings_panel.setLayout(layout)
        parent_layout.addWidget(settings_panel)

    def show_popup(self, title, message, icon):
        # General function to show a popup
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setIcon(icon)
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.exec()

    def open_file_dialog(self, file_type):
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            'Open File',
            '',
            'CSV Files (*.csv)'
        )

        if file_name:
            if file_type == CATALOGUE:
                self.catalogue_file_name = file_name
            elif file_type == COMPLETENESS:
                self.completeness_file_name = file_name

            self.show_popup('Success', 'File selected successfully!', QMessageBox.Icon.Information)
        else:
            if file_type == CATALOGUE:
                self.catalogue_file_name = None
            elif file_type == COMPLETENESS:
                self.completeness_file_name = None

                self.show_popup('Error', 'No file was selected.', QMessageBox.Icon.Warning)

    def solve(self):
        m_min = float(self.m_min_input.text())
        mag_interval = float(self.mag_interval_input.text())

        b_val, sigma_b, rate, sigma_rate, agr, agr_sigma = compute_weichert_values(self.catalogue_file_name,
                                                                                   self.completeness_file_name,
                                                                                   self.comp_option,
                                                                                   m_min,
                                                                                   mag_interval)

        print(f'b_val: {b_val}')
        print(f'sigma_b: {sigma_b}')
        print(f'rate: {rate}')
        print(f'sigma_rate: {sigma_rate}')
        print(f'agr: {agr}')
        print(f'agr_sigma: {agr_sigma}')


