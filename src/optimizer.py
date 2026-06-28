import numpy as np
from config.loader import config
from src.models import blair, bell, evanschitzky

def _compute_theta(cfg: dict) -> float:
    vt = cfg["valve_timing"]
    true_EVO = 180 - vt["EVO"]
    true_IVO = 360 - vt["IVO"]
    return true_IVO - true_EVO - vt["wave_delay"]

def run(cfg: dict = config) -> dict:
    th = cfg["thermodynamics"]
    vt = cfg["valve_timing"]
    es = cfg["engine_specs"]
    ss = cfg["solver_settings"]

    RPM = np.arange(ss["min_RPM"], ss["max_RPM"], ss["stepsize_RPM"])
    theta = _compute_theta(cfg)

    results = {
        "RPM": RPM,
        "Blair":                [blair.primary_length(r, th["T0"]) for r in RPM],
        "Bell":                 [bell.primary_length(r, th["T0"], vt["EVO"]) for r in RPM],
        "Evanschitzky":         [evanschitzky.primary_length_isothermal(r, th["T0"], theta) for r in RPM],
        "Evanschitzky_Thermal": [evanschitzky.primary_length_thermal(r, th["T0"], th["T_env"], theta, cfg["geometry"]["D"], es["vol"], es["n_cyl"], th["rho"], ss["epsilon"]) for r in RPM],
    }
    return results