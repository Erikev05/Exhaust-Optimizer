"""
Blair (1999) exhaust runner length formula
"""


import numpy as np


def primary_length(RPM: float, T0: float) -> float:
    """
    Calculate optimal exhaust primary length using Blair's formula.

    Args:
        RPM:  Engine speed (rev/min)
        T0:   Exhaust gas temperature at port (K)

    Returns:
        Primary pipe length (m)
    """

    return 2.058e5 * np.sqrt(T0) / RPM / 1000