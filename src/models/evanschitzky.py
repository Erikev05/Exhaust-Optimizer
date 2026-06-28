"""
Evanschitzky exhaust tuning length formula.
Uses acoustic wave travel time over the tuning window (theta).
Two variants:
  - Isothermal: constant speed of sound at T0
  - Thermal:    iterative, accounts for temperature drop along runner

Reference: Evanschitzky (derived from first principles, wave mechanics)
"""

import numpy as np
from library.constants import Constants as const


def _speed_of_sound(T: float, gamma: float, R: float) -> float:
    return np.sqrt(gamma * R * T)


def primary_length_isothermal(RPM: float, T0: float, theta: float) -> float:
    """
    Isothermal variant — single speed of sound at exhaust port temperature.

    Args:
        RPM:    Engine speed (rev/min)
        T0:     Exhaust gas temperature at port (K)
        theta:  Tuning window in crank degrees (IVO - EVO - wave_delay)

    Returns:
        Primary pipe length (m)
    """
    c = _speed_of_sound(T0, const.gamma_ex, const.R_gas)
    return c * theta / (RPM * 12)


def primary_length_thermal(
    RPM: float,
    T0: float,
    T_env: float,
    theta: float,
    D: float,
    vol: float,
    n_cyl: int,
    rho: float,
    epsilon: float,
) -> float:
    """
    Thermal variant — iterates until pipe length converges.
    Accounts for exhaust gas cooling along the runner length.

    Args:
        RPM:     Engine speed (rev/min)
        T0:      Exhaust gas temperature at port (K)
        T_env:   Ambient temperature (K)
        theta:   Tuning window in crank degrees
        D:       Runner pipe diameter (m)
        vol:     Engine displacement (cc)
        n_cyl:   Number of cylinders
        rho:     Air density (kg/m^3)
        epsilon: Convergence tolerance (m)

    Returns:
        Primary pipe length (m)
    """
    m_dot = (vol * 1e-6 / n_cyl) * (RPM / 120) * rho

    L = primary_length_isothermal(RPM, T0, theta)  # physical initial guess

    for _ in range(500):  
        T_end = T_env + (T0 - T_env) * np.exp(
            -(const.h * np.pi * D * L) / (m_dot * const.cp)
        )
        T_avg = (T0 + T_end) / 2
        L_new = _speed_of_sound(T_avg, const.gamma_ex, const.R_gas) * theta / (RPM * 12)

        if abs(L_new - L) < epsilon:
            return L_new
        L = L_new

    raise RuntimeError(f"Evanschitzky thermal solver did not converge at {RPM} RPM")