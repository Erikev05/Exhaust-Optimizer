import numpy as np
import inputs as inp
from library.constants import Constants as const
import solver.preparation as prep

L_Blair = []
L_Bell = []
L_Evanschitzky = []
L_Evanschitzky_Temp = []

def perform_solving():
    for i in range(len(prep.RPM)):
        blair_val = 2.058 * 10**5 * np.sqrt(inp.T0) / prep.RPM[i] / 1000
        L_Blair.append(blair_val)
        
        bell_val = ((inp.T0 * (360 - inp.EVO) / prep.RPM[i]) - 3) * 25.4 / 1000
        L_Bell.append(bell_val)
        
        evans_val = np.sqrt(const.gamma * const.R_gas * inp.T0) * prep.theta / (prep.RPM[i] * 12)
        L_Evanschitzky.append(evans_val)

        evans_temp_val = solve_Evanschitzky_Temp(i)
        L_Evanschitzky_Temp.append(evans_temp_val)


    return L_Blair, L_Bell, L_Evanschitzky, L_Evanschitzky_Temp


def solve_Evanschitzky_Temp(i):
    L_guess = 0.5
    L_new = 10
    while inp.epsilon < abs(L_new - L_guess):
        L_guess = L_new
        m_dot = inp.vol * 10**-6 / inp.n_cyl * prep.RPM[i] * inp.rho / 120
        T_end = inp.T_env + (inp.T0 - inp.T_env)*np.e**(-(const.h * np.pi * inp.D * L_guess)/(m_dot * const.cp))

        L_new = np.sqrt(const.gamma_ex * const.R_gas * (inp.T0 + T_end)/2) * prep.theta / (prep.RPM[i] * 12)
    
    return L_new