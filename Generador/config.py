# 1. Aceleraciones espectrales

ts_dict = {'PGA' : 0.01,
           'SA(0.2)' : 0.20,
           'SA(0.5)' : 0.50,
           'SA(1.0)' : 1.00,
           'SA(2.0)' : 2.00
           }

# 2. Probabilidad de excedencias

tr_dict = {0.4 : 'Tr= 100 años',
           0.1 : 'Tr= 475 años',
           0.05 : 'Tr= 1000 años',
           0.02 : 'Tr= 2475 años',
           0.01 : 'Tr= 5000 años',
           0.005 : 'Tr= 10000 años',
           0.0025 : 'Tr= 50000 años'
           }

# 3. Gráficas de las Curvas de Peligro

hazard_curve_x_lim = (0.01, 10.00)
hazard_curve_x_ticks = [0.01, 1.00, 10.00]

hazard_curve_y_lim = (0.0001, 1)
hazard_curve_y_ticks = [0.0001, 0.001, 0.01, 0.1, 1]

# 4. Gráficas de Espectro de Peligro Uniforme

uhs_x_lim = (0.01, 10.00)
uhs_x_ticks = [0.01, 0.10, 1.00, 10.00]



