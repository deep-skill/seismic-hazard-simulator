import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from openquake.hmtk.seismicity.catalogue import Catalogue
from openquake.hmtk.seismicity.completeness.comp_stepp_1971 import Stepp1971
from openquake.hmtk.seismicity.max_magnitude.cumulative_moment_release import CumulativeMoment
from openquake.hmtk.seismicity.occurrence.weichert import Weichert


def generate_catalogue(file_path, m_min):
    data = pd.read_csv(file_path, delimiter=';')
    """ data = data[(data['longitude'] >= -77) &
                                              (data['longitude'] <= -74) &
                                              (data['latitude'] >= -12) &
                                              (data['latitude'] <= -9)] """

    data['eventID'] = data['eventID'].astype(str)
    data = data[data['magnitude'] >= m_min]

    data_dict = dict()

    for key in data.columns:
        data_dict[key] = np.array(data[key])

    return Catalogue.make_from_dict(data_dict)


def import_completeness_table(file_path):
    data = pd.read_csv(file_path)
    return data.iloc[1:].to_numpy()


def generate_completeness_table_stepp(catalogue):
    stepp = Stepp1971()
    config = {'magnitude_bin' : 0.1,
              'time_bin' : 1,
              'increment_lock' : True,
              }

    return stepp.completeness(catalogue, config)


def compute_m_max(catalogue):
    config = {'number_bootstraps' : 1}
    m_max, std_m_max = CumulativeMoment().get_mmax(catalogue, config)

    return m_max, std_m_max


def compute_weichert_values(catalogue_file_name, completeness_file_name, comp_option, m_min, mag_interval):
    catalogue = generate_catalogue(catalogue_file_name, m_min)
    completeness_table = None

    if comp_option == 'import':
        completeness_table = import_completeness_table(completeness_file_name)
    elif comp_option == 'generate':
        completeness_table = generate_completeness_table_stepp(catalogue)

    config = {'magnitude_interval' : mag_interval}
    weichert = Weichert()
    b_val, sigma_b, rate, sigma_rate, agr, agr_sigma = weichert._calculate(catalogue, config, completeness=completeness_table)

    m_max, std_m_max = compute_m_max(catalogue)

    magnitudes = catalogue.data['magnitude']
    print(magnitudes)
    bins = np.arange(min(magnitudes), max(magnitudes) + mag_interval, mag_interval)

    frequencies, bin_edges = np.histogram(magnitudes, bins=bins)
    frequencies_cum = np.cumsum(frequencies[::-1])[::-1]  # Suma acumulativa desde el mayor al menor

    N_total = len(magnitudes)
    M_values = np.linspace(m_min, m_max, 10000)

    def truncated_gr(M, M_min, M_max, b_value, N_total):
        beta = b_value * np.log(10)
        numerator = np.exp(-beta * (M-M_min)) - np.exp(-beta * (M_max - M_min))
        denominator = 1 - np.exp(-beta * (M_max - M_min))
        return N_total * numerator / denominator

    frecuencies2 = truncated_gr(M_values, m_min, m_max, b_val, N_total)
    print(frecuencies2)


    plt.figure(figsize=(10, 6))

    # Frecuencia acumulativa
    plt.plot(bin_edges[:-1], frequencies_cum, marker='o', color='red', label='Frecuencia acumulada')
    plt.plot(M_values, frecuencies2, color='orange', label='Truncated')

    plt.yscale('log')

    # Personalización del gráfico
    plt.xlabel('Magnitud', fontsize=12)
    plt.ylabel('Frecuencia', fontsize=12)
    plt.title('Magnitud vs Frecuencia', fontsize=14)
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.show()

    return b_val, sigma_b, rate, sigma_rate, agr, agr_sigma


