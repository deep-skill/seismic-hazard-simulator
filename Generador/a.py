import os
from pathlib import Path

current_directory = Path.cwd()

file_path = current_directory / 'archivo.txt'

with open(file_path, 'r') as f:
    lines = f.readlines()

tr_dict = {0.4 : 'Tr= 100 años',
           0.1 : 'Tr= 475 años',
           0.05 : 'Tr= 1000 años',
           0.02 : 'Tr= 2475 años',
           0.01 : 'Tr= 5000 años',
           0.005 : 'Tr= 10000 años'
           }

with open(file_path, 'w') as f:
    for line in lines:
        if 'poes' in line:
            f.write('poes = ')

            for v in tr_dict.keys():
                f.write(str(v) + ' ')

            f.write('\n')
        else:
            f.write(line)

