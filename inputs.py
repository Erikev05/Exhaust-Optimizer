import numpy as np

T0 = 850
T_env = 300
D = 0.035   #diameter of the exhaust runner pipe


EVO = 64
EVC = 24
IVO = 39
IVC = 65

wave_delay = 40 #time for wave to form in crank degrees ref Heywood

vol = 599   #volume of the engine
n_cyl = 4
rho = 1.225 #density

min_RPM = 3000
max_RPM = 14000
stepsize_RPM = 500

epsilon = 0.001