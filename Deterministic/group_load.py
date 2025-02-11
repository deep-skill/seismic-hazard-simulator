import os
import pandas as pd
import numpy as np
import shutil
from PyQt6.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QDialog, QTableWidget, \
    QFileDialog, QTableWidgetItem, QMessageBox
from openquake.hazardlib.valid import gsim
from openquake.hazardlib.contexts import SitesContext, RuptureContext, DistancesContext
from openquake.hazardlib.imt import SA
from openquake.hazardlib import const
from seismic_utils import import_gmpes_weights
import matplotlib.pyplot as plt


class GroupLoad(QDialog):
    def __init__(self, group_name, parent_window: QDialog=None):
        super().__init__()

        self.parent_window = parent_window

        screen = QApplication.primaryScreen()
        available_geometry = screen.availableGeometry()  # Without taskbar, etc.

        available_width = available_geometry.width()
        available_height = available_geometry.height()

        self.setGeometry(0, 0, available_width, available_height)

        self.group_name = group_name
        self.gmpes, self.weights = import_gmpes_weights(group_name)

        self.gsims = []
        self.required_sites_parameters = []
        self.required_distances_parameters = []
        self.required_rupture_parameters = []

        for gmpe in self.gmpes:
            equation = gsim('['+gmpe+']')
            self.required_sites_parameters += list(equation.REQUIRES_SITES_PARAMETERS)
            self.required_distances_parameters += list(equation.REQUIRES_DISTANCES)
            self.required_rupture_parameters += list(equation.REQUIRES_RUPTURE_PARAMETERS)

            self.gsims.append(equation)

        self.required_sites_parameters = list(set(self.required_sites_parameters))
        self.required_distances_parameters = list(set(self.required_distances_parameters))
        self.required_rupture_parameters = list(set(self.required_rupture_parameters))

        self.columns = ['custom_site_id', 'lon', 'lat']
        self.columns += self.required_sites_parameters
        self.columns += self.required_distances_parameters
        self.columns += self.required_rupture_parameters

        self.missing_cols = self.columns
        self.site_df = None

        # Table Widget
        self.table_widget = QTableWidget(self)

        self.build_main_panel()

    def build_main_panel(self):
        layout = QVBoxLayout()

        self.update_table_widget()
        layout.addWidget(self.table_widget)

        self.build_button_panel(layout)

        self.setLayout(layout)

    def build_button_panel(self, parent_layout):
        button_panel = QWidget()
        layout = QHBoxLayout()

        return_button = QPushButton('Volver')
        return_button.clicked.connect(self.return_window)
        layout.addWidget(return_button)

        load_button = QPushButton('Cargar datos')
        load_button.clicked.connect(self.open_file_dialog)
        layout.addWidget(load_button)

        save_button = QPushButton('Guardar resultados')
        save_button.clicked.connect(self.select_folder)
        layout.addWidget(save_button)

        button_panel.setLayout(layout)
        parent_layout.addWidget(button_panel)

    def update_table_widget(self):
        self.table_widget.setColumnCount(len(self.columns))
        self.table_widget.setHorizontalHeaderLabels(self.columns)
        self.table_widget.setRowCount(0)

        if self.site_df is not None:
            self.table_widget.setRowCount(len(self.site_df.index))
            self.missing_cols = []

            for index_col, col in enumerate(self.columns):
                if col not in self.site_df:
                    self.missing_cols.append(col)
                else:
                    for index_row, value in enumerate(self.site_df[col]):
                        self.table_widget.setItem(index_row, index_col, QTableWidgetItem(str(value)))

            if len(self.missing_cols) > 0:
                QMessageBox.critical(self, "Error", f"Columnas faltantes: {self.missing_cols}", QMessageBox.StandardButton.Ok)

        self.table_widget.resizeColumnsToContents()
        self.table_widget.resizeRowsToContents()

    def save_results(self, folder):
        folder = os.path.join(folder, 'Output' + self.group_name)

        if os.path.exists(folder) and os.path.isdir(folder):
            shutil.rmtree(folder)

        os.mkdir(folder)

        for _, row in self.site_df.iterrows():
            site_ctx = SitesContext()
            rup_ctx = RuptureContext()
            dist_ctx = DistancesContext()

            for param in self.required_sites_parameters:
                if param in row:
                    setattr(site_ctx, param, np.array([row[param]]))

            for param in self.required_distances_parameters:
                if param in row:
                    setattr(dist_ctx, param, np.array([row[param]]))

            for param in self.required_rupture_parameters:
                if param in row:
                    setattr(rup_ctx, param, np.array([row[param]]))

            if 'custom_site_id' in row:
                site_ctx.sids = np.array([row['custom_site_id']])

            periods = np.logspace(-2, 1, 100)
            imts = [SA(period) for period in periods]
            stddev_types = [const.StdDev.TOTAL]

            results = self.calculate_ground_motions(self.gsims, imts, site_ctx, rup_ctx, dist_ctx, stddev_types)

            name = 'Coordenada ' + str(int(row['custom_site_id']))
            row_folder = os.path.join(folder, name)

            if os.path.exists(row_folder) and os.path.isdir(row_folder):
                shutil.rmtree(row_folder)

            os.mkdir(row_folder)

            self.generate_report_from_results(results, periods, row_folder, 'mean')
            self.generate_report_from_results(results, periods, row_folder, 'mean_plus_1sd')

        QMessageBox.information(self, "Información", "Los resultados fueron guardados con exito!", QMessageBox.StandardButton.Ok)

    def generate_report_from_results(self, results, periods, row_folder, column_name):
        df_spectrums_mean = pd.Series(periods, name='periods')
        mean_gsim = pd.Series(np.zeros(len(df_spectrums_mean)), name='mean')

        for equation, weight in zip(self.gsims, self.weights):
            actual_spectrum = pd.Series(results[str(equation)][column_name],
                                        name=str(equation)+ ' - ' + str(weight) + '%')

            df_spectrums_mean = pd.concat([df_spectrums_mean, actual_spectrum], axis=1)
            mean_gsim += weight / 100 * actual_spectrum

        df_spectrums_mean = pd.concat([df_spectrums_mean, mean_gsim], axis=1)
        df_spectrums_mean.to_excel(os.path.join(row_folder, column_name + '.xlsx'), index=False)

        plt.clf()

        for equation in self.gsims:
            plt.semilogx(periods, results[str(equation)][column_name], label=str(equation))

        plt.xlabel('periodo')
        plt.ylabel('aceleracion')
        plt.title('Espectros')
        plt.grid()
        plt.legend()
        plt.savefig(os.path.join(row_folder, column_name+'_gmpes.png'))

        plt.semilogx(periods, mean_gsim, label='mean', ls='dashed', color='purple')
        plt.legend()
        plt.savefig(os.path.join(row_folder, column_name+'_gmpes_and_mean.png'))

    def select_folder(self):
        if self.site_df is None:
            QMessageBox.critical(self, "Error", "Archivo aun no cargado", QMessageBox.StandardButton.Ok)
            return

        if len(self.missing_cols) > 0:
            QMessageBox.critical(self, "Error", f"Columnas faltantes: {self.missing_cols}", QMessageBox.StandardButton.Ok)
            return

        folder = QFileDialog.getExistingDirectory(self, "Seleccionar Carpeta")
        if folder:
            self.save_results(folder)
        else:
            QMessageBox.critical(self, "Error", "Carpeta no seleccionada", QMessageBox.StandardButton.Ok)

    def open_file_dialog(self):
        file_name, _ = QFileDialog.getOpenFileName(self,
                                                   "Seleccionar archivo CSV", "",
                                                   "Archivos CSV (*.csv);;Todos los archivos (*)",
                                                   )

        if not file_name:
            QMessageBox.critical(self, "Error", "Archivo no seleccionado", QMessageBox.StandardButton.Ok)
            return

        self.site_df = pd.read_csv(file_name)
        self.update_table_widget()

    def return_window(self):
        self.close()
        self.parent_window.show()

    def calculate_ground_motions(self, gmpes, imts, sctx, rctx, dctx, stddev_types):
        """
        Calculates the expected ground motion and uncertainty, organised by GMPE
        and intensity measure type (i.e. PGA, SA etc.), for a given rupture-site configuration
        """
        results = {}
        nper = len(imts)
        for gmpe in gmpes:
            print("Running GMPE %s" % str(gmpe))
            results[str(gmpe)] = {"mean": np.zeros(nper),
                                  "stddevs": np.zeros(nper),
                                  "mean_plus_1sd": np.zeros(nper),
                                  "mean_minus_1sd": np.zeros(nper)}
            for i, imt in enumerate(imts):
                try:
                    mean, [stddev] = gmpe.get_mean_and_stddevs(
                        sctx, rctx, dctx, imt, stddev_types)
                    results[str(gmpe)]["mean"][i] = np.exp(mean) # e^ln(Sa)
                    results[str(gmpe)]["stddevs"][i] = stddev # sd
                    results[str(gmpe)]["mean_plus_1sd"][i] = np.exp(mean + stddev) # e^(ln(Sa) + sd) - P84
                    results[str(gmpe)]["mean_minus_1sd"][i] = np.exp(mean - stddev) # e^(ln(Sa) - sd) - P16
                except KeyError:
                    results[str(gmpe)]["mean"][i] = np.nan
                    results[str(gmpe)]["stddevs"][i] = np.nan
                    results[str(gmpe)]["mean_plus_1sd"][i] = np.nan
                    results[str(gmpe)]["mean_minus_1sd"][i] = np.nan

        return results

