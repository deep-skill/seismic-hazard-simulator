import pandas as pd
import numpy as np
from openquake.hmtk.seismicity.catalogue import Catalogue
from openquake.hmtk.seismicity.completeness.comp_stepp_1971 import Stepp1971
from openquake.hmtk.seismicity.occurrence.weichert import Weichert
from openquake.hmtk.seismicity.occurrence.utils import get_completeness_counts, generate_trunc_gr_magnitudes
from openquake.hmtk.seismicity.max_magnitude.cumulative_moment_release import CumulativeMoment
import matplotlib.pyplot as plt

data = pd.read_csv('data.csv', delimiter=';')
# data = data[(data['longitude'] >= -77) & (data['longitude'] <= -74) & (data['latitude'] >= -12) & (data['latitude'] <= -9)]


data['eventID'] = data['eventID'].astype(str)
data_dict = dict()
m_min = 4.5
m_max = max(data['magnitude'])
data = data[data['magnitude'] >= m_min]

for key in data.columns:
    data_dict[key] = np.array(data[key])

catalogue = Catalogue.make_from_dict(data_dict)
# print(catalogue)

config = {'number_bootstraps' : 1}
m_max, std_m_max = CumulativeMoment().get_mmax(catalogue, config)

# print(m_max)

step = Stepp1971()

magnitude_interval = 0.5

config = {'magnitude_bin' : 0.5,
                          'time_bin' : 5,
                          'increment_lock' : True,
                          'magnitude_interval' : magnitude_interval,
                          # 'reference_magnitude' : m_min,
                          }
step.completeness(catalogue, config)
completeness_table = step.completeness_table

completeness_table = np.array([[1964, 5.0],
                      [1960, 6.0],
                      [1954, 7.0],
                      [1906, 8.0],
                      [1555, 10]])
completeness_table = step.completeness_table

# print(completeness_table)

weichert = Weichert()
b_val, sigma_b, rate, sigma_rate, agr, agr_sigma = weichert._calculate(catalogue, config, completeness=completeness_table)
print(b_val, sigma_b, rate, sigma_rate, agr, agr_sigma)


magnitudes = data['magnitude']
bins = np.arange(min(magnitudes), max(magnitudes) + magnitude_interval, magnitude_interval)

frequencies, bin_edges = np.histogram(magnitudes, bins=bins)
frequencies_cum = np.cumsum(frequencies[::-1])[::-1]  # Suma acumulativa desde el mayor al menor

N_total = len(data)
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


