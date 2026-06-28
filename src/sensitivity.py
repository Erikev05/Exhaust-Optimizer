"""
Sensitivity analysis for all exhaust runner length models.
Computes normalised sensitivy coefficient based on S(p) = (dL/L) / (dp/p) using central difference over an RPM sweep.
Investigates the effect of a 1% change in a parameter on the percentage change of L.
"""

import numpy as np
import pandas as pd
from typing import Callable
from library.constants import Constants as const


def _central_diff(fn: Callable, p_val: float, h: float = 0.01) -> float:
    """Return dL/dp * (p/L) via central difference at ±h*p.

    Args:
        fn (Callable): Formula that is being analysed
        p_val (float): Parameter value
        h (float, optional): Percentage change used to perform sensitivity analysis. Defaults to 0.01.

    Returns:
        float: Returns normalised sensitivity coefficient.
    """
    
    L_high = fn(p_val * (1 + h))
    L_low = fn(p_val * (1 - h))
    L_0  = fn(p_val)
    dLdp = (L_high - L_low) / (2 * h * p_val)
    return dLdp * (p_val / L_0)
    
    

def compute(cfg: dict, RPM_array: np.ndarray) -> pd.DataFrame:
    """Compute sensitivity coefficients for all methods and parameters across the RPM sweep.

    Returns a DataFrame indexed by RPM with MultiIndex columns: (method, parameter)

    Args:
        cfg (dict): Configuration of the engine and input paramters
        RPM_array (np.ndarray): range of RPM for sweep

    Returns:
        pd.DataFrame: Outputs a dataframe 
    """
    
    from src.models import blair, bell, evanschitzky
    
    th = cfg["thermodynamics"]
    vt = cfg["valve_timing"]
    es = cfg["engine_specs"]
    ss = cfg["solver_settings"]
    geo = cfg["geometry"]

    T0    = th["T0"]
    T_env = th["T_env"]
    rho   = th["rho"]
    EVO   = vt["EVO"]
    D     = geo["D"]
    vol   = es["vol"]
    n_cyl = es["n_cyl"]
    eps   = ss["epsilon"]

    true_EVO   = 180 - EVO
    true_IVO   = 360 - vt["IVO"]
    theta      = true_IVO - true_EVO - vt["wave_delay"]
    
    
    records = []
    for RPM in RPM_array:

        # --- Blair: L = f(T0)
        blair_T0 = _central_diff(
            lambda t: blair.primary_length(RPM, t), T0)

        # --- Bell: L = f(T0, EVO)
        bell_T0  = _central_diff(
            lambda t: bell.primary_length(RPM, t, EVO), T0)
        bell_EVO = _central_diff(
            lambda e: bell.primary_length(RPM, T0, e), EVO)

        # --- Evanschitzky isothermal: L = f(T0, theta)
        ev_T0    = _central_diff(
            lambda t: evanschitzky.primary_length_isothermal(RPM, t, theta), T0)
        ev_theta = _central_diff(
            lambda th_: evanschitzky.primary_length_isothermal(RPM, T0, th_), theta)
        ev_gamma = _central_diff(
            lambda g: evanschitzky.primary_length_isothermal(RPM, T0, theta, g), const.gamma_ex)

        # --- Evanschitzky thermal: L = f(T0, T_env, theta, D)
        evt_T0   = _central_diff(
            lambda t: evanschitzky.primary_length_thermal(RPM, t, T_env, theta, D, vol, n_cyl, rho, eps), T0)
        evt_Tenv = _central_diff(
            lambda t: evanschitzky.primary_length_thermal(RPM, T0, t, theta, D, vol, n_cyl, rho, eps), T_env)
        evt_theta= _central_diff(
            lambda th_: evanschitzky.primary_length_thermal(RPM, T0, T_env, th_, D, vol, n_cyl, rho, eps), theta)
        evt_D    = _central_diff(
            lambda d: evanschitzky.primary_length_thermal(RPM, T0, T_env, theta, d, vol, n_cyl, rho, eps), D)
        evt_rho    = _central_diff(
            lambda r: evanschitzky.primary_length_thermal(RPM, T0, T_env, theta, D, vol, n_cyl, r, eps), rho)
        evt_gamma= _central_diff(
            lambda g: evanschitzky.primary_length_thermal(RPM, T0, T_env, theta, D, vol, n_cyl, rho, eps, g), const.gamma_ex)
        evt_h = _central_diff(
            lambda h_: evanschitzky.primary_length_thermal(RPM, T0, T_env, theta, D, vol, n_cyl, rho, eps, h=h_), const.h)
        evt_cp = _central_diff(
            lambda cp: evanschitzky.primary_length_thermal(RPM, T0, T_env, theta, D, vol, n_cyl, rho, eps, cp=cp), const.cp)

        records.append({
            "RPM": RPM,
            ("Blair",               "T0"):    blair_T0,
            ("Bell",                "T0"):    bell_T0,
            ("Bell",                "EVO"):   bell_EVO,
            ("Evanschitzky",        "T0"):    ev_T0,
            ("Evanschitzky",        "theta"): ev_theta,
            ("Evanschitzky",        "gamma"): ev_gamma,
            ("Evanschitzky_Thermal","T0"):    evt_T0,
            ("Evanschitzky_Thermal","T_env"): evt_Tenv,
            ("Evanschitzky_Thermal","theta"): evt_theta,
            ("Evanschitzky_Thermal","D"):     evt_D,
            ("Evanschitzky_Thermal","rho"):   evt_rho,
            ("Evanschitzky_Thermal","gamma"): evt_gamma,
            ("Evanschitzky_Thermal","h"):     evt_h,
            ("Evanschitzky_Thermal","cp"):    evt_cp,
        })

    df = pd.DataFrame(records).set_index("RPM")
    df.columns = pd.MultiIndex.from_tuples(df.columns)
    return df