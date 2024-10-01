import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import os
import shutil
import subprocess
import numpy as np
import re
from pathlib import Path
from config import *

# ========== Preparar job.ini ===================

ordered_tr_dict = {k : tr_dict[k] for k in sorted(tr_dict, reverse=True)}
tr_dict = ordered_tr_dict

current_directory = Path.cwd()
dir_route = current_directory / "Input2"
job_route = dir_route / "job.ini"
current_file_path = Path(__file__).resolve()

with open(job_route, 'r') as f:
    lines = f.readlines()

with open(job_route, 'w') as f:
    for line in lines:
        if '#' in line or ('poes' not in line):
            f.write(line)
        else:
            f.write('poes = ')

            for v in tr_dict.keys():
                f.write(str(v) + ' ')

            f.write('\n')

# ========== Ejecución del modelo y obtención de output ==========

#subprocess.run('oq dbserver stop', shell=True)
#subprocess.run('oq dbserver start', shell=True)

oq_run_query = 'oq engine --run ' + str(job_route)
os.system(oq_run_query)
#subprocess.run(oq_run_query, shell=True)

lhc = subprocess.getoutput('oq engine --lhc').split('\n')
last_hc = re.split(r'\s+', lhc[-1])
calculation_id = int(last_hc[1])

output_route = current_directory / "Output"
coords_route = output_route / "Coordenadas"
oq_output_route = output_route / "Openquake"
tr_route = output_route / "Tiempo de retorno"

if os.path.exists(output_route):
    shutil.rmtree(output_route)

os.mkdir(output_route)
os.mkdir(coords_route)
os.mkdir(oq_output_route)
os.mkdir(tr_route)

oq_export_query = 'oq engine --export-outputs ' + str(calculation_id) + ' ' + str(oq_output_route)
subprocess.run(oq_export_query, shell=True)

hazard_curve_mean_files = os.listdir(oq_output_route)
hazard_curve_mean_csvs = []

ts_list = list(ts_dict.keys())
ts_values = list(ts_dict.values())

for ts in ts_list:
    for csv_file in hazard_curve_mean_files:
        if csv_file.startswith('hazard_curve-mean-' + ts):
            hazard_curve_mean_csvs.append(csv_file)

hazard_uhs_mean_csv = ''

for csv_file in hazard_curve_mean_files:
    if csv_file.startswith('hazard_uhs-mean'):
        hazard_uhs_mean_csv = csv_file

hazard_uhs_mean_csv = oq_output_route / hazard_uhs_mean_csv
# print(hazard_uhs_mean_csv)

hazard_uhs_mean_df = pd.read_csv(hazard_uhs_mean_csv, header=1)
hazard_only_sa_columns = [column for column in hazard_uhs_mean_df.columns if '~' in column]
# columns_to_drop = [column for column in hazard_uhs_mean_df.columns if '~' not in column]
# hazard_uhs_mean_df = hazard_uhs_mean_df.drop(columns=columns_to_drop, errors='ignore')

# Number of coordinates
n_coord = len(hazard_uhs_mean_df)

# periods
periods: list[float] = []
poes = []

for column in hazard_only_sa_columns:
    poe, period = column.split('~')

    poes.append(float(poe))

    if period == 'PGA': period = 0.01
    else: period = float(period[period.index('(')+1 : -1])

    periods.append(period)

periods = sorted(list(set(periods)))
n_periods = len(periods)

poes = sorted(list(set(poes)), reverse=True)
n_poes = len(poes)

poes_header = ['poe=' + str(poe) + ' - Tr= ' + str(tr_dict[poe]) + ' años' for i, poe in enumerate(poes)]
dir_point_routes = [coords_route / f"Coordenada {hazard_uhs_mean_df.loc[i, 'custom_site_id']}" for i in range(n_coord)]

for i in range(n_coord):
    os.mkdir(dir_point_routes[i])

# ================================================
# CURVA DE POE (TABLAS)
# ================================================

curves_df = []

for coord in range(n_coord):
    curve_df = pd.DataFrame()

    for i, csv_file in enumerate(hazard_curve_mean_csvs):
        curve = pd.read_csv(oq_output_route / csv_file, header=1)
        columns_to_drop = [column for column in curve.columns if not column.startswith('poe')]
        curve = curve.drop(columns=columns_to_drop, errors='ignore')

        curve = curve.iloc[coord, :].transpose().reset_index()

        curve_df['g (Ts= ' + str(ts_values[i]) + ')'] = curve['index'].apply(lambda x : float(x[4:]))
        curve_df['r% (Ts= ' + str(ts_values[i]) + ')'] = curve[coord]
        curve_df['1/tr (Ts= ' + str(ts_values[i]) + ')'] = -np.log(1 - curve[coord] + 1e-20) / 50

        curve_df.to_excel(dir_point_routes[coord] / "Hazard Curve Mean.xlsx", index=False)

    curves_df.append(curve_df)

# ================================================
# CURVA DE POE (GRAFICAS)
# ================================================

for coord in range(n_coord):
    fig, ax = plt.subplots()

    ax.set_title('CURVA DE PROBABILIDAD DE EXCEDENCIA PARA ACELERACIÓN\nESPECTRAL EN 50 AÑOS DE EXPOSICIÓN SÍSMICA (PUNTO ' + str(coord+1) + ')')

    ax.set_xscale('log')
    ax.set_xlim(hazard_curve_x_lim[0], hazard_curve_x_lim[1])
    #ax.set_xlim(0.01, 10.00)
    ax.set_xticks(hazard_curve_x_ticks)
    #ax.set_xticks([0.01, 1.00, 10.00])
    ax.set_xlabel('Aceleración espectral (g)')

    ax.set_yscale('log')
    ax.set_ylim(hazard_curve_y_lim[0], hazard_curve_y_lim[1])
    #ax.set_ylim(0.0001, 1)
    ax.set_yticks(hazard_curve_y_ticks)
    #ax.set_yticks([0.0001, 0.001, 0.01, 0.1, 1])
    ax.set_ylabel('PROBABILIDAD DE EXCEDENCIA (r%) EN 50 AÑOS')

    ax.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
    ax.get_yaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())

    for i in range(len(ts_values)):
        ax.plot(curves_df[coord].iloc[:, 3 * i], curves_df[coord].iloc[:, 3 * i + 1], label='Ts= ' + str(ts_values[i]) + ' s')

    ax.legend(loc='best')
    plt.grid(True)

    plt.savefig(dir_point_routes[coord] / 'Hazard Curve Mean (50 años).png')
    plt.close(fig)


for coord in range(n_coord):
    fig, ax = plt.subplots()

    ax.set_title('CURVA DE PROBABILIDAD ANUAL DE EXCEDENCIA PARA\nACELERACIÓN ESPECTRAL (PUNTO ' + str(coord+1) + ')')

    ax.set_xscale('log')
    ax.set_xlim(hazard_curve_x_lim[0], hazard_curve_x_lim[1])
    #ax.set_xlim(0.01, 10.00)
    ax.set_xticks(hazard_curve_x_ticks)
    #ax.set_xticks([0.01, 1.00, 10.00])
    ax.set_xlabel('Aceleración espectral (g)')

    ax.set_yscale('log')
    ax.set_ylim(hazard_curve_y_lim[0], hazard_curve_y_lim[1])
    #ax.set_ylim(0.0001, 1)
    ax.set_yticks(hazard_curve_y_ticks)
    #ax.set_yticks([0.0001, 0.001, 0.01, 0.1, 1])
    ax.set_ylabel('PROBABILIDAD ANUAL DE EXCEDENCIA (1/tr)')

    ax.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
    ax.get_yaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())

    for i in range(len(ts_values)):
        ax.plot(curves_df[coord].iloc[:, 3 * i], curves_df[coord].iloc[:, 3 * i + 2], label='Ts= ' + str(ts_values[i]) + ' s')

    ax.legend(loc='best')
    plt.grid(True)

    plt.savefig(dir_point_routes[coord] / 'Hazard Curve Mean (anual).png')
    plt.close(fig)

# ================================================
# ESPECTROS DE PELIGRO UNIFORME (TABLAS)
# ================================================

uhs_tables = []
tr_tables = []

for i in range(len(poes)):
    tr_table = pd.DataFrame()
    tr_tables.append(tr_table)

for coord in range(n_coord):
    uhs_table = pd.DataFrame()
    uhs_table['period'] = pd.Series(periods)

    for i, poe in enumerate(poes_header):
        data = hazard_uhs_mean_df[hazard_only_sa_columns].iloc[coord, i * n_periods : (i+1) * n_periods].reset_index(drop=True)
        uhs_table[poe] = data

        site_id = hazard_uhs_mean_df.loc[coord, 'custom_site_id']
        tr_tables[i][site_id] = data
        # tr_tables[i].loc[len(tr_tables[i])] = tr_row

    uhs_table.to_excel(dir_point_routes[coord] / 'Hazard UHS Mean.xlsx', index=False)

    uhs_tables.append(uhs_table)

for i, poe in enumerate(poes):
    tr_tables[i] = tr_tables[i].T
    tr_tables[i].columns = periods
    tr_tables[i] = tr_tables[i].reset_index()
    tr_tables[i] = tr_tables[i].rename(columns={'index' : 'custom_site_id'})

    file_name = "Tr " + str(tr_dict[poe]) + " años.xlsx"
    tr_tables[i].to_excel(tr_route / file_name, index=False)

# ================================================
# ESPECTROS DE PELIGRO UNIFORME (GRAFICAS)
# ================================================

for coord in range(n_coord):
    fig, ax = plt.subplots()

    ax.set_title('Espectros de Peligro Uniforme (PUNTO ' + str(coord+1) + ')')

    ax.set_xscale('log')
    ax.set_xlim(uhs_x_lim[0], uhs_x_lim[1])
    #ax.set_xlim(0.01, 10.00)
    ax.set_xticks(uhs_x_ticks)
    #ax.set_xticks([0.01, 0.10, 1.00, 10.00])
    ax.set_xlabel('Periodo (s)')

    #ax.set_ylim(0.0001, 1)
    #ax.set_yticks([0.0001, 0.001, 0.01, 0.1, 1])
    ax.set_ylabel('Aceleración espectral (g)')

    ax.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
    ax.get_yaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())

    for i, poe in enumerate(reversed(poes_header)):
        ax.plot(uhs_tables[coord]['period'], uhs_tables[coord][poe], label=tr_dict[poes[-i-1]])

    ax.legend(loc='best')
    plt.grid(True)

    plt.savefig(dir_point_routes[coord] / 'Hazard UHS Mean.png')
    plt.close(fig)

# ================================================
# GENERAR REPORTE 
# ================================================



